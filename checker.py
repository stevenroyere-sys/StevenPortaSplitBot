# -*- coding: utf-8 -*-
"""
Vérifie la disponibilité de chaque (produit, marchand) défini dans config.py
et envoie une notification Telegram/email dès qu'un produit passe de
"pas en stock" à "en stock".

Usage :
    python checker.py

Prévu pour tourner en cron (GitHub Actions) toutes les 10-15 minutes.
"""

import json
import os
import random
import time
import unicodedata
from pathlib import Path

import requests

from config import PRODUCTS, OUT_OF_STOCK_KEYWORDS, IN_STOCK_KEYWORDS
from notifier import notify_in_stock

STATE_FILE = Path(__file__).parent / "state.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

REQUEST_TIMEOUT = 20


def strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)
    )


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_page_text(url: str) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        print(f"[checker] Erreur réseau sur {url}: {exc}")
        return None

    if resp.status_code != 200:
        print(f"[checker] Statut HTTP {resp.status_code} sur {url} — possible blocage anti-bot.")
        return None

    return resp.text


def detect_stock_status(html: str) -> str:
    """
    Retourne "in_stock", "out_of_stock" ou "unknown".

    Heuristique volontairement simple : on cherche des mots-clés dans le
    texte brut de la page (sans script/style, cf. extraction rapide ci-dessous).
    Ce n'est pas infaillible : certains sites (Darty, Auchan, Leroy Merlin...)
    utilisent du JS lourd ou des protections anti-bot (Datadome/Akamai) qui
    peuvent renvoyer une page vide ou un mur "vérification en cours" avec
    une simple requête HTTP. Si ça arrive régulièrement pour un site donné,
    il faudra passer par un navigateur headless (voir README, section
    "Limites").
    """
    # Extraction grossière du texte visible (retire script/style) sans
    # dépendance supplémentaire lourde.
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
    except ImportError:
        text = html

    normalized = strip_accents(text).lower()

    for kw in OUT_OF_STOCK_KEYWORDS:
        if strip_accents(kw).lower() in normalized:
            return "out_of_stock"

    for kw in IN_STOCK_KEYWORDS:
        if strip_accents(kw).lower() in normalized:
            return "in_stock"

    return "unknown"


def main() -> None:
    state = load_state()
    changed = False

    for entry in PRODUCTS:
        key = entry["key"]
        product = entry["product"]
        site = entry["site"]
        url = entry["url"]

        if "TODO" in url:
            print(f"[checker] {site} / {product} : URL non renseignée, on saute.")
            continue

        print(f"[checker] Vérification {product} chez {site} ...")
        html = fetch_page_text(url)

        if html is None:
            status = "unknown"
        else:
            status = detect_stock_status(html)

        previous = state.get(key, {}).get("status", "unknown")

        if status == "in_stock" and previous != "in_stock":
            print(f"[checker] 🟢 {product} EN STOCK chez {site} -> notification envoyée.")
            notify_in_stock(product, site, url)
        else:
            print(f"[checker] {product} chez {site} : statut = {status}")

        if state.get(key, {}).get("status") != status:
            changed = True

        state[key] = {"status": status, "url": url}

        # Pause polie entre deux requêtes pour ne pas cogner les serveurs.
        time.sleep(random.uniform(1.5, 3.5))

    if changed:
        save_state(state)


if __name__ == "__main__":
    main()
