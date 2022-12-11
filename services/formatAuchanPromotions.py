def formatAuchanPromotions(data):
    fData = []
    for dt in data:
        id = dt[3]
        prix = dt[2]
        promo = dt[1]
        type = ''
        numProduit = "1"
        reduction = "0"
        match promo.split()[0]:
            case "Vu":
                type = "catalogue"
            case "PROMO":
                type = "reduction"
                reduction = promo.split()[2][:-1]
            case "Le":
                type = "reduction"
                numProduit = promo.split()[1][0]
                reduction = promo.split()[3][1: -1]
            case "Prenez":
                type = "combinaison"
                numProduit = promo.split()[2]
                # a 100% s'il gagne un ex : prenez en 3 = payez en 2 | 200% s'il gagne 2 ex : prenez en 5 = payez en 3
                reduction = str((int(numProduit) - int(promo.split()[6]))*100)
            case default:
                if promo.split()[0][-1] == "%" : 
                    type = "economie"
                    reduction = promo.split()[0][:-1]
                else:
                    if promo.split()[0].isnumeric():
                        if '%' in promo:
                            type = "Remise"
                            numProduit = promo.split()[0]
                            reduction = promo.split()[3][:-1]
                        else:
                            type = "iRemise"
                            numProduit = promo.split()[0]
                            reduction = promo.split()[3][:-1]
                    else:
                        type = "n/a"
        fData.append([id, prix, type, numProduit, reduction])
    return fData