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
