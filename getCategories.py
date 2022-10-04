import json
from Categories.Auchan_get_Categories import *

carrefour_categories = [
    {
        "CATEGORIE_ID": 'shopping',
        "CATEGORIE_NOM": 'High-Tech, Maison et Loisirs',
        "IMAGE":"https://media.carrefour.fr/medias/66ee4696427d30daa7adb51c47a9fe67/p_96x96/34452.jpg",
    },
    {
        "CATEGORIE_ID": 'bio-et-ecologie',
        "CATEGORIE_NOM": 'Bio et Ecologie',
        "IMAGE":"https://media.carrefour.fr/medias/5f3d0dc998fd3a20831086a36082fd36/p_96x96/1838.jpg",
    },
    {
        "CATEGORIE_ID": 'fruits-et-legumes',
        "CATEGORIE_NOM": 'Fruits et Légumes',
        "IMAGE":"https://media.carrefour.fr/medias/185e7fe99d4a39b5a6cca9e806324d3d/p_96x96/1882.jpg",
    },
    {
        "CATEGORIE_ID": 'viandes-et-poissons',
        "CATEGORIE_NOM": 'Viandes et Poissons',
        "IMAGE":"https://media.carrefour.fr/medias/9e116ecf9a313f8b959b5e603d7933a5/p_96x96/1921.jpg",
    },
    {
        "CATEGORIE_ID": 'pains-et-patisseries',
        "CATEGORIE_NOM": 'Pains et Patisseries',
        "IMAGE":"https://media.carrefour.fr/medias/7555898f95a53010996592b7d2ecf854/p_96x96/1952.jpg",
    },
    {
        "CATEGORIE_ID": 'frais',
        "CATEGORIE_NOM": 'Frais',
        "IMAGE":"https://media.carrefour.fr/medias/9fb528d6d5db306cb9f413840d7b6425/p_96x96/28127.jpg",
    },
    {
        "CATEGORIE_ID": 'surgeles',
        "CATEGORIE_NOM": 'Surgelés',
        "IMAGE":"https://media.carrefour.fr/medias/5586596a0fc730d5846de9a72d3cea57/p_96x96/2074.jpg",
    },
    {
        "CATEGORIE_ID": 'boissons',
        "CATEGORIE_NOM": 'Boissons',
        "IMAGE":"https://media.carrefour.fr/medias/5994db3414e934f68edcb2a3cd59ba20/p_96x96/27070.jpg",
    },
    {
        "CATEGORIE_ID": 'epicerie-salee',
        "CATEGORIE_NOM": 'Epicerie salée',
        "IMAGE":"https://media.carrefour.fr/medias/e4d537e30ae43902b93147c989d2ad02/p_96x96/2112.jpg",
    },
    {
        "CATEGORIE_ID": 'epicerie-sucree',
        "CATEGORIE_NOM": 'Epicerie sucrée',
        "IMAGE":"https://media.carrefour.fr/medias/844bd69b601734e28a6a6071e6595585/p_96x96/2183.jpg",
    },
    {
        "CATEGORIE_ID": 'produits-du-monde',
        "CATEGORIE_NOM": 'Produits du monde',
        "IMAGE":"https://media.carrefour.fr/medias/6dba74396dcc3773b42c18b71c1367f8/p_96x96/29650.jpg",
    },
    {
        "CATEGORIE_ID": 'hygiene-et-beaute',
        "CATEGORIE_NOM": 'Hygiène et Beauté',
        "IMAGE":"https://media.carrefour.fr/medias/a0812ad978dd398e92bad45650bcc925/p_96x96/2415.jpg",
    },
    {
        "CATEGORIE_ID": 'entretien-et-nettoyage',
        "CATEGORIE_NOM": 'Entretien et Nettoyage',
        "IMAGE":"https://media.carrefour.fr/medias/4334cdd14c8735afb0f595215f1efe1c/p_96x96/2589.jpg",
    },
    {
        "CATEGORIE_ID": 'bebe',
        "CATEGORIE_NOM": 'Bébé',
        "IMAGE":"https://media.carrefour.fr/medias/ca56671104913afaac2ac8c5e22c0e6a/p_96x96/26953.jpg",
    },
]

auchan_categories,auchan_sous_categories = getAuchanCategories()

with open('Produits/toutes_categories.json', 'w') as f:
    json.dump(carrefour_categories+auchan_categories, f)
with open('Produits/toutes_sous_categories.json', 'w') as f:
    json.dump(auchan_sous_categories, f)