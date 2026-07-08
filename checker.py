# -*- coding: utf-8 -*-
"""
Vérifie la disponibilité de chaque (produit, marchand) défini dans config.py
et envoie une notification Telegram/email dès qu'un produit passe de
"pas en stock" à "en stock".

Usage :
    python checker.py

Toutes les vérifications tournent EN PARALLÈLE (requests + Playwright)
pour minimiser le temps total d'exécution — chaque site est interrogé une
seule fois par run, donc paralléliser ne change rien à la charge envoyée
à chaque marchand, juste au temps total du script.
"""

import asyncio
import json
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


def _sync_fetch_with_requests(url: str) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        print(f"[checker] Erreur réseau sur {url}: {exc}")
        return None

    if resp.status_code != 200:
        print(f"[checker] Statut HTTP {resp.status_code} sur {url} — possible blocage anti-bot.")
        return None

    return resp.text


async def fetch_with_requests(url: str) -> str | None:
    # requests est bloquant : on le pousse dans un thread pour ne pas geler
    # les autres vérifications qui tournent en parallèle.
    return await asyncio.to_thread(_sync_fetch_with_requests, url)


async def fetch_with_playwright(browser, url: str) -> str | None:
    try:
        page = await browser.new_page(user_agent=HEADERS["User-Agent"], locale="fr-FR")
        try:
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            # Laisse le temps au JS de charger le prix / bouton panier.
            await page.wait_for_timeout(2500)
            html = await page.content()
        finally:
            await page.close()
        return html
    except Exception as exc:  # noqa: BLE001
        print(f"[checker] Erreur Playwright sur {url}: {exc}")
        return None


def detect_stock_status(html: str) -> str:
    """
    Retourne "in_stock", "out_of_stock" ou "unknown".

    Deux passes :
    1. Détection WooCommerce : classe CSS technique (in-stock/out-of-stock),
       plus fiable que le texte visible car stable même si le libellé
       affiché est personnalisé par la boutique.
    2. Fallback par mots-clés dans le texte visible.
    """
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        stock_elements = soup.select(".stock, [class*='stock']")
        for el in stock_elements:
            classes = " ".join(el.get("class", []))
            if "out-of-stock" in classes:
                return "out_of_stock"
            if "in-stock" in classes:
                return "in_stock"

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


def print_debug_snippet(html: str) -> None:
    try:
        from bs4 import BeautifulSoup

        soup_debug = BeautifulSoup(html, "html.parser")
        for tag in soup_debug(["script", "style", "noscript"]):
            tag.decompose()
        snippet = soup_debug.get_text(separator=" ")
        snippet = " ".join(snippet.split())[:300]
        print(f"[checker] Extrait de la page (statut inconnu) : {snippet}")
    except Exception:  # noqa: BLE001
        pass


async def fetch_entry(entry: dict, browser) -> tuple[str, str | None]:
    url = entry["url"]
    method = entry.get("method", "requests")
    if method == "playwright":
        html = await fetch_with_playwright(browser, url)
    else:
        html = await fetch_with_requests(url)
    return entry["key"], html


async def run_checks() -> dict:
    active_entries = [e for e in PRODUCTS if "TODO" not in e["url"]]
    for e in PRODUCTS:
        if "TODO" in e["url"]:
            print(f"[checker] {e['site']} / {e['product']} : URL non renseignée, on saute.")

    needs_playwright = any(e.get("method") == "playwright" for e in active_entries)

    results: dict[str, str | None] = {}

    if needs_playwright:
        from playwright.async_api import async_playwright

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            try:
                tasks = [
                    fetch_entry(entry, browser if entry.get("method") == "playwright" else None)
                    for entry in active_entries
                ]
                fetched = await asyncio.gather(*tasks)
            finally:
                await browser.close()
    else:
        tasks = [fetch_entry(entry, None) for entry in active_entries]
        fetched = await asyncio.gather(*tasks)

    for key, html in fetched:
        results[key] = html

    return results


def main() -> None:
    state = load_state()
    changed = False

    print("[checker] Récupération de toutes les pages en parallèle ...")
    html_by_key = asyncio.run(run_checks())

    for entry in PRODUCTS:
        key = entry["key"]
        product = entry["product"]
        site = entry["site"]
        url = entry["url"]

        if key not in html_by_key:
            continue

        html = html_by_key[key]
        status = detect_stock_status(html) if html is not None else "unknown"

        if status == "unknown" and html is not None:
            print(f"[checker] {product} chez {site} : statut inconnu, extrait ci-dessous")
            print_debug_snippet(html)

        previous = state.get(key, {}).get("status", "unknown")

        if status == "in_stock" and previous != "in_stock":
            print(f"[checker] 🟢 {product} EN STOCK chez {site} -> notification envoyée.")
            notify_in_stock(product, site, url)
        else:
            print(f"[checker] {product} chez {site} : statut = {status}")

        if state.get(key, {}).get("status") != status:
            changed = True

        state[key] = {"status": status, "url": url}

    if changed:
        save_state(state)


if __name__ == "__main__":
    main()
