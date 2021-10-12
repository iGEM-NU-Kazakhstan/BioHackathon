def measure(listA, listB):
    TP, TF, FP, FN = 0

    for i in range(len(listA)):
        if listB[i] == listA[i] == 1:
           TP += 1
        if listB[i] == listA[i] == 0:
           TF += 1
        if listB[i] == 0 and listA[i] == 1:
           FP += 1
        if listB[i] == 1 and listA[i] == 0:
           FN += 1

    # Recall or true positive rate
    TPR = TP / (TP + FN)

    # Precision or positive predictive value
    PPV = TP / (TP + FP)

    return(TP, FP, TN, FN, TPR, PPV)