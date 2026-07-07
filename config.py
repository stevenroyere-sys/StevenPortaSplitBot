# -*- coding: utf-8 -*-
"""
Configuration des produits et des sites à surveiller.

Chaque entrée = un couple (produit, marchand) surveillé indépendamment.
"method" indique comment récupérer la page :
  - "requests" : simple requête HTTP (rapide, mais bloqué par certains sites)
  - "playwright" : navigateur headless (plus lent, contourne certains blocages
    basiques, mais pas les protections avancées type Datadome/Akamai)
"""

PRODUCTS = [
    {
        "key": "portasplit_boulanger",
        "product": "Portasplit",
        "site": "Boulanger",
        "url": "https://www.boulanger.com/ref/1216685",
        "method": "playwright",
    },
    {
        "key": "portasplit_darty",
        "product": "Portasplit",
        "site": "Darty",
        "url": "https://www.darty.com/nav/achat/gros_electromenager/climatisation/marque__midea__MDEA.html",
        "method": "playwright",
    },
    {
        "key": "portasplit_manomano",
        "product": "Portasplit",
        "site": "ManoMano",
        "url": "https://www.manomano.fr/p/midea-climatiseur-split-mobile-reversible-froid-chaud-3500w12000btu-wifi-deshumidificateur-ventilateur-jusqua-40m2-kit-fenetre-inclus-83810402",
        "method": "playwright",
    },
    {
        "key": "portasplit_castorama",
        "product": "Portasplit",
        "site": "Castorama",
        "url": "https://www.castorama.fr/climatiseur-portasplit-midea-reversible-3500w/8431312260509_CAFR.prd",
        "method": "requests",
    },
    {
        "key": "portasplit_leroymerlin",
        "product": "Portasplit",
        "site": "Leroy Merlin",
        "url": "https://www.leroymerlin.fr/produits/climatiseur-split-mobile-reversible-portasplit-midea-par-optimea-93857579.html",
        "method": "playwright",
    },
    {
        "key": "portasplit_joybuy",
        "product": "Portasplit",
        "site": "Joybuy",
        "url": "https://www.joybuy.fr/dp/midea-portasplit-climatiseur-r\u00e9versible-froidchaud-35kw/100003175005531",
        "method": "playwright",
    },
    {
        "key": "portasplit_rakuten",
        "product": "Portasplit",
        "site": "Rakuten",
        "url": "https://fr.shopping.rakuten.com/offer/buy/13466164647/clim-reversible-optimea-mmcs-12hrn8-qrd0.html",
        "method": "requests",
    },
    {
        "key": "portasplit_fnac",
        "product": "Portasplit",
        "site": "Fnac",
        "url": "https://www.fnac.com/MIDEA-Climatiseur-Split-Mobile-Reversible-Froid-Chaud-3500W-12000BTU-WiFi-deshumidificateur-ventilateur-jusqu-a-40m2-kit-fenetre-inclus/a21457105/w-4",
        "method": "playwright",
    },
    {
        "key": "portasplit_auchan",
        "product": "Portasplit",
        "site": "Auchan",
        "url": "https://www.auchan.fr/optimea-clim-reversible-midea-climatiseur-split-mobile/pr-10b80596-1b4d-4ebb-aeba-ad08f0943013",
        "method": "playwright",
    },
    {
        "key": "portasplit_amazon",
        "product": "Portasplit",
        "site": "Amazon",
        "url": "https://www.amazon.fr/Climatiseur-Climatisation-rafra%C3%AEchisseur-d%C3%A9shumidificateur-ventilateur/dp/B0CY2YW8BT",
        "method": "requests",
    },
    {
        "key": "portasplit_optimea",
        "product": "Portasplit",
        "site": "Optimea",
        "url": "https://www.optimea.fr/product/climatiseur-split-mobile-midea/",
        "method": "requests",
    },
]

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
