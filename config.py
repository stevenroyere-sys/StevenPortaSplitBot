# -*- coding: utf-8 -*-
"""
Configuration des produits et des sites à surveiller.

IMPORTANT : remplace les URLs marquées "TODO" par l'URL EXACTE de la fiche
produit (pas une page de recherche/catégorie). Pour la trouver : va sur le
site du marchand, cherche "Midea PortaSplit" (ou "PortaSplit Cool"), ouvre
la fiche produit, copie l'URL de la barre d'adresse.

Chaque entrée = un couple (produit, marchand) surveillé indépendamment.
"""

PRODUCTS = [
    {
        "key": "portasplit_boulanger",
        "product": "Portasplit",
        "site": "Boulanger",
        "url": "https://www.boulanger.com/ref/1216685",
    },
    {
        "key": "portasplit_darty",
        "product": "Portasplit",
        "site": "Darty",
        # TODO: URL exacte de la fiche produit Darty (le lien ci-dessous est
        # une page catégorie Midea, à remplacer par la fiche PortaSplit)
        "url": "https://www.darty.com/nav/achat/gros_electromenager/climatisation/marque__midea__MDEA.html",
    },
    {
        "key": "portasplit_manomano",
        "product": "Portasplit",
        "site": "ManoMano",
        "url": "https://www.manomano.fr/p/midea-climatiseur-split-mobile-reversible-froid-chaud-3500w12000btu-wifi-deshumidificateur-ventilateur-jusqua-40m2-kit-fenetre-inclus-83810402",
    },
    {
        "key": "portasplit_castorama",
        "product": "Portasplit",
        "site": "Castorama",
        "url": "https://www.castorama.fr/climatiseur-portasplit-midea-reversible-3500w/8431312260509_CAFR.prd",
    },
    {
        "key": "portasplit_leroymerlin",
        "product": "Portasplit",
        "site": "Leroy Merlin",
        "url": "https://www.leroymerlin.fr/produits/climatiseur-split-mobile-reversible-portasplit-midea-par-optimea-93857579.html",
    },
    {
        "key": "portasplit_joybuy",
        "product": "Portasplit",
        "site": "Joybuy",
        "url": "https://www.joybuy.fr/dp/midea-portasplit-climatiseur-réversible-froidchaud-35kw/100003175005531",
    },
    {
        "key": "portasplit_rakuten",
        "product": "Portasplit",
        "site": "Rakuten",
        "url": "https://fr.shopping.rakuten.com/offer/buy/13466164647/clim-reversible-optimea-mmcs-12hrn8-qrd0.html",
    },
    {
        "key": "portasplit_fnac",
        "product": "Portasplit",
        "site": "Fnac",
        "url": "https://www.fnac.com/MIDEA-Climatiseur-Split-Mobile-Reversible-Froid-Chaud-3500W-12000BTU-WiFi-deshumidificateur-ventilateur-jusqu-a-40m2-kit-fenetre-inclus/a21457105/w-4",
    },
    {
        "key": "portasplit_auchan",
        "product": "Portasplit",
        "site": "Auchan",
        "url": "https://www.auchan.fr/optimea-clim-reversible-midea-climatiseur-split-mobile/pr-10b80596-1b4d-4ebb-aeba-ad08f0943013",
    },

# Mots-clés qui indiquent une RUPTURE de stock (en minuscules, sans accents
# gérés dans le code). Liste volontairement large car chaque site a son
# propre wording.
OUT_OF_STOCK_KEYWORDS = [
    "rupture de stock",
    "indisponible",
    "actuellement indisponible",
    "non disponible",
    "épuisé",
    "epuise",
    "hors stock",
    "en réapprovisionnement",
    "produit épuisé",
    "temporairement indisponible",
    "sold out",
    "out of stock",
    "unavailable",
    "notify me when available",
    "prévenez-moi",
    "être alerté",
    "me prévenir",
]

# Mots-clés qui indiquent une disponibilité (bouton actif, etc.)
IN_STOCK_KEYWORDS = [
    "ajouter au panier",
    "acheter maintenant",
    "en stock",
    "add to cart",
    "buy now",
    "livraison offerte",
    "disponible en ligne",
]
