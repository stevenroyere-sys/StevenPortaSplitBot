# Alerte stock Midea Portasplit / Portasplit Cool

Vérifie automatiquement la disponibilité du climatiseur **Midea PortaSplit**
sur plusieurs sites marchands français, et envoie une notification Telegram
(et email, en option) dès qu'un modèle repasse en stock.

## Architecture

- `config.py` : liste des couples (produit, marchand) à surveiller, avec pour
  chacun une `"method"` :
  - `"requests"` : simple requête HTTP (rapide, utilisé pour les sites qui
    ne bloquent pas ce type d'accès : Castorama, Rakuten, Amazon, Optimea)
  - `"playwright"` : navigateur headless (plus lent, utilisé pour les sites
    qui bloquent les requêtes simples : Boulanger, Darty, ManoMano,
    Leroy Merlin, Fnac, Joybuy, Auchan)
- `checker.py` : récupère chaque page selon sa méthode, détecte le statut par
  mots-clés, notifie en cas de passage en stock, sauvegarde l'état dans
  `state.json`
- `notifier.py` : envoi Telegram + email optionnel
- `.github/workflows/check-stock.yml` : exécute `checker.py` toutes les 5
  minutes (minimum réellement supporté par GitHub Actions)

## 1. Récupérer ton `chat_id` Telegram

1. Envoie n'importe quel message à ton bot sur Telegram.
2. Ouvre `https://api.telegram.org/bot<TON_TOKEN>/getUpdates` dans un
   navigateur.
3. Note la valeur `"chat":{"id": ...}` — c'est ton `TELEGRAM_CHAT_ID`.

## 2. Secrets GitHub

`Settings → Secrets and variables → Actions → New repository secret` :

| Nom                | Obligatoire | Valeur |
|--------------------|-------------|--------|
| `TELEGRAM_TOKEN`   | oui | token de ton bot |
| `TELEGRAM_CHAT_ID` | oui | récupéré à l'étape 1 |
| `SMTP_SERVER`      | non | ex: `smtp.gmail.com` |
| `SMTP_PORT`        | non | ex: `587` |
| `SMTP_USER`        | non | ton adresse email |
| `SMTP_PASS`        | non | mot de passe d'application |
| `EMAIL_TO`         | non | adresse qui reçoit les alertes |

Ne mets jamais le token en clair dans le code — uniquement dans les Secrets.

## 3. URLs produits

Toutes les URLs de `config.py` sont déjà renseignées avec de vraies fiches
produit. Si un marchand change son URL produit avec le temps, remplace-la
directement dans `config.py`.

## 4. Déployer sur GitHub

Remplace chaque fichier concerné directement dans l'éditeur GitHub (crayon
✏️ → tout sélectionner → coller → Commit changes), en respectant bien le
chemin `.github/workflows/check-stock.yml` pour le workflow.

**Ne remplace pas `state.json` manuellement** une fois le bot en service :
il est mis à jour automatiquement par le workflow et contient le dernier
statut connu de chaque site, ce qui évite les notifications en double.

Le workflow se lance ensuite automatiquement toutes les 5 minutes, ou
manuellement depuis l'onglet **Actions** → **Run workflow**.

## Limites importantes

- **Détection par mots-clés**, pas par sélecteur CSS précis : plus robuste
  aux changements de mise en page, mais peut donner de faux
  positifs/négatifs. Si un site pose problème, ajuste
  `OUT_OF_STOCK_KEYWORDS` / `IN_STOCK_KEYWORDS` dans `config.py`.
- **Playwright contourne les protections basiques** mais pas les protections
  avancées type Datadome/Akamai (souvent utilisées par le groupe
  Fnac-Darty) : ces sites peuvent rester bloqués même avec un navigateur
  headless, car les IP des serveurs GitHub sont elles-mêmes parfois
  repérées.
- **GitHub Actions cron n'est pas garanti à la minute près** : en cas de
  forte charge, l'exécution peut être retardée de quelques minutes. Le
  minimum réel est 5 minutes ; en dessous, GitHub ignore ou retarde
  fortement l'exécution.
- Chaque run avec Playwright prend 2-3 minutes (installation + navigation
  sur plusieurs sites), contre quelques secondes en requests simple.
