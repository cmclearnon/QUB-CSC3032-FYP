from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score

'''
Functions for retrieving Confusion-matrix derived performance metrics of models
'''
def tn(y_true, y_pred): return confusion_matrix(y_true, y_pred)[0, 0]   # y_pred = Model's prediction results
def fp(y_true, y_pred): return confusion_matrix(y_true, y_pred)[0, 1]   # y_pred = Model's prediction results
def fn(y_true, y_pred): return confusion_matrix(y_true, y_pred)[1, 0]   # y_pred = Model's prediction results
def tp(y_true, y_pred): return confusion_matrix(y_true, y_pred)[1, 1]   # y_pred = Model's prediction results

# Returns True Negative Rate
def tnr(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    rate = (tn/(tn+fp))
    return rate

# Returns True Positive Rate
def tpr(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    rate = (tp/(tp+fn))
    return rate

# Returns False Negative Rate
def fnr(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    rate = (fn/(fn+tp))
    return rate

# Returns False Positive Rate
def fpr(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    rate = (fp/(fp+tn))
    return rate

# Returns Accuracy of model predictions
def accuracy(y_true, y_pred):
    return accuracy_score(y_true, y_pred, normalize=True)

# Returns Area under Curve score of model performance
def auc_score(y_true, y_score):
    return roc_auc_score(y_true, y_score)

def avg_precision_score(y_true, y_score):
    return average_precision_score(y_true, y_score)

