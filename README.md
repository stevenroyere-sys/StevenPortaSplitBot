# Alerte stock Midea Portasplit / Portasplit Cool

Vérifie automatiquement la disponibilité du climatiseur **Midea PortaSplit**
et **PortaSplit Cool** sur plusieurs sites marchands français, et envoie une
notification Telegram (et email, en option) dès qu'un modèle repasse en
stock.

## 1. Récupérer ton `chat_id` Telegram

1. Ouvre une conversation avec ton bot sur Telegram et envoie-lui n'importe
   quel message (ex : "salut").
2. Ouvre cette URL dans un navigateur (remplace le token si besoin) :
   `https://api.telegram.org/bot<TON_TOKEN>/getUpdates`
3. Dans le JSON retourné, note la valeur `"chat":{"id": ...}` — c'est ton
   `TELEGRAM_CHAT_ID`.

## 2. Configurer les secrets GitHub

Dans le repo GitHub → **Settings → Secrets and variables → Actions → New
repository secret**, ajoute :

| Nom              | Obligatoire | Valeur                                   |
|------------------|-------------|-------------------------------------------|
| `TELEGRAM_TOKEN`   | oui | le token de ton bot (celui donné par @BotFather) |
| `TELEGRAM_CHAT_ID` | oui | récupéré à l'étape 1 |
| `SMTP_SERVER`      | non | ex: `smtp.gmail.com` |
| `SMTP_PORT`        | non | ex: `587` |
| `SMTP_USER`        | non | ton adresse email |
| `SMTP_PASS`        | non | mot de passe d'application (pas ton mot de passe normal) |
| `EMAIL_TO`         | non | adresse qui reçoit les alertes |

Si tu ne renseignes pas les variables SMTP, seul Telegram sera utilisé
(l'email est ignoré silencieusement).

⚠️ Ne mets JAMAIS le token en clair dans le code ou dans un commit — utilise
uniquement les Secrets ci-dessus.

## 3. Renseigner les URLs produits

Ouvre `config.py` et remplace chaque URL marquée `TODO` par l'URL exacte de
la fiche produit (pas une page de recherche). Pour la trouver :
cherche "Midea PortaSplit" (ou "PortaSplit Cool") sur le site du marchand,
ouvre la fiche produit, copie l'URL.

## 4. Pousser sur GitHub

```bash
git add .
git commit -m "Ajout du bot de surveillance de stock Portasplit"
git push
```

Le workflow `.github/workflows/check-stock.yml` tourne ensuite automatiquement
toutes les 10 minutes. Tu peux aussi le lancer manuellement depuis l'onglet
**Actions** du repo (bouton "Run workflow").

## 5. Tester en local (optionnel)

```bash
pip install -r requirements.txt
export TELEGRAM_TOKEN="123:abc"
export TELEGRAM_CHAT_ID="123456789"
python checker.py
```

## Limites importantes à connaître

- **Détection par mots-clés, pas par sélecteur CSS précis.** C'est plus
  robuste aux changements de mise en page, mais ça peut donner de faux
  positifs/négatifs sur certains sites mal formulés. Si un site donné pose
  problème, ouvre `checker.py` et affine `detect_stock_status` pour ce cas.
- **Protections anti-bot.** Darty, Auchan, Leroy Merlin, Cdiscount et
  d'autres utilisent parfois des protections (Datadome, Akamai, Cloudflare)
  qui peuvent bloquer une simple requête `requests` (page vide, mur de
  vérification, code 403). Si `checker.py` affiche souvent
  "statut = unknown" ou "possible blocage anti-bot" pour un site, il faudra
  passer par un navigateur headless (Playwright) pour ce site précis — ça
  change l'architecture (plus lent, plus lourd en CI) donc dis-moi si tu
  veux que je l'ajoute pour des sites spécifiques une fois que tu as vu
  lesquels posent problème.
- **GitHub Actions cron n'est pas garanti à la minute près** : en cas de
  forte charge, l'exécution peut être retardée de quelques minutes.
- Le fichier `state.json` est recommité automatiquement par le workflow pour
  se souvenir du dernier statut connu et ne pas re-notifier à chaque run.
