import pandas as pd
import json
import csv

promotions = []
df = pd.read_excel('PromotionTrier.xlsx')
for index,row in df.iterrows():
    [codebar,prix,typePromo,numProduit,reduction] = row
    promotions.append(
        [
            codebar,
            float(prix.replace(' ','').replace(',','.')),
            typePromo if isinstance(typePromo,str) else 'NULL',
            int(numProduit),
            float(reduction.replace(' ','').replace(',','.')),
        ]
    )
    # promotions.append(
    #     {
    #         "CODE_BAR":codebar,
    #         "PRIX":prix,
    #         "TYPE_PROMO":typePromo if isinstance(typePromo,str) else 'NULL',
    #         "NUM_PRODUIT":numProduit,
    #         "REDUCTION":reduction
    #     }
    # )

header = ["CODE_BAR","PRIX","TYPE_PROMO","NUM_PRODUIT","REDUCTION"]
with open('promotions.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # write multiple rows
    writer.writerows(promotions)

# with open('promotions.json', 'w') as f:
#     json.dump(promotions, f)