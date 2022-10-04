import pandas as pd
import json

promotions = []

df = pd.read_excel('PromotionTrier.xlsx')
for index,row in df.iterrows():
    [codebar,prix,typePromo,numProduit,reduction] = row
    promotions.append(
        {
            "CODE_BAR":codebar,
            "PRIX":prix,
            "TYPE_PROMO":typePromo if isinstance(typePromo,str) else 'NULL',
            "NUM_PRODUIT":numProduit,
            "REDUCTION":reduction
        }
    )

with open('promotions.json', 'w') as f:
    json.dump(promotions, f)