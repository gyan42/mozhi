import numpy as np
from seqeval.metrics import precision_score, recall_score, f1_score, classification_report
from sklearn_crfsuite.metrics import flat_classification_report


def get_flat_classification_report(test_labels, pred_labels):
    report = flat_classification_report(y_pred=pred_labels, y_true=test_labels)
    print(report)
    return report


def get_f1_score(test_labels, pred_labels):
    f1 = f1_score(test_labels, pred_labels)
    print("F1-score: {:.1%}".format(f1))
    return f1


def tag_stats(tags, tag2idx, idx2tag, test_x, text_y, test_pred):
    TP = {}
    TN = {}
    FP = {}
    FN = {}
    for tag in tag2idx.keys():
        TP[tag] = 0
        TN[tag] = 0
        FP[tag] = 0
        FN[tag] = 0

    def accumulate_score_by_tag(gt, pred):
        """
        For each tag keep stats
        """
        if gt == pred:
            TP[gt] += 1
        elif gt != 'O' and pred == 'O':
            FN[gt] += 1
        elif gt == 'O' and pred != 'O':
            FP[gt] += 1
        else:
            TN[gt] += 1

    for i, sentence in enumerate(test_x):
        y_hat = np.argmax(test_pred[0], axis=-1)
        gt = np.argmax(text_y[0], axis=-1)
        for idx, (w, pred) in enumerate(zip(sentence, y_hat)):
            accumulate_score_by_tag(idx2tag[gt[idx]], tags[pred])

    for tag in tag2idx.keys():
        print(f'Tag : {tag}')
        print('\t TN:{:10}\tFP:{:10}'.format(TN[tag], FP[tag]))
        print('\t FN:{:10}\tTP:{:10}'.format(FN[tag], TP[tag]))

