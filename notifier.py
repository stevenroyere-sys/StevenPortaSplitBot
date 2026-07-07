# -*- coding: utf-8 -*-
"""
Envoi de notifications (Telegram + email optionnel).

Toutes les valeurs sensibles viennent de variables d'environnement,
JAMAIS écrites en dur ici. En local, tu peux créer un fichier .env
(non commité, voir .gitignore) ou exporter les variables dans ton shell.
En GitHub Actions, elles viennent des "Secrets" du repo.
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText

import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT") or "587")
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
EMAIL_TO = os.environ.get("EMAIL_TO", "")


def send_telegram(message: str) -> None:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[notifier] TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID manquant, notification Telegram ignorée.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        resp = requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
            },
            timeout=15,
        )
        if not resp.ok:
            print(f"[notifier] Erreur Telegram ({resp.status_code}): {resp.text}")
    except requests.RequestException as exc:
        print(f"[notifier] Exception lors de l'envoi Telegram: {exc}")


def send_email(subject: str, message: str) -> None:
    if not (SMTP_SERVER and SMTP_USER and SMTP_PASS and EMAIL_TO):
        # Email non configuré, on ne fait rien silencieusement (Telegram suffit).
        return
    msg = MIMEText(message, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [EMAIL_TO], msg.as_string())
    except Exception as exc:  # noqa: BLE001
        print(f"[notifier] Exception lors de l'envoi email: {exc}")


def notify_in_stock(product: str, site: str, url: str) -> None:
    message = f"🟢 <b>{product}</b> est EN STOCK chez <b>{site}</b> !\n{url}"
    send_telegram(message)
    send_email(f"[Stock] {product} disponible chez {site}", f"{product} est en stock chez {site}\n{url}")
