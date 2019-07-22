import numpy as np
import os
import itertools
import time

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from config import config


clf_callable_map = {
    'Naive Bayes': GaussianNB(),
    'Gaussian Process': GaussianProcessClassifier(),
    'AdaBoost': AdaBoostClassifier(),
    'SVM': SVC(probability=True),
    'Nearest Neighbors': KNeighborsClassifier(),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'Extra Trees': ExtraTreesClassifier(),
    'MLP': MLPClassifier()}

clf_hyperparams_map = {
    'Naive Bayes': config.NaiveBayes_hyperparameters,
    'Gaussian Process': config.GaussianProcess_hyperparameters,
    'AdaBoost': config.AdaBoost_hyperparameters,
    'SVM': config.SVM_hyperparameters,
    'Nearest Neighbors': config.kNN_hyperparameters,
    'Decision Tree': config.DecisionTree_hyperparameters,
    'Random Forest': config.RandomForest_hyperparameters,
    'Extra Trees': config.RandomForest_hyperparameters,
    'MLP': config.MLP_hyperparameters}


def create_feature_sets_generator(fold_path):
    train_sets = [f for f in os.listdir(fold_path) if f.startswith('X_train_')]
    train_sets = sorted(train_sets, key=lambda i: (len(i), i))

    test_sets = [f for f in os.listdir(fold_path) if f.startswith('X_test_')]
    test_sets = sorted(test_sets, key=lambda i: (len(i), i))

    feature_sets = zip(train_sets, test_sets)
    for feature_set in feature_sets:
        yield feature_set


def train_classifier(clf_name, X_train, y_train):
    clf = clf_callable_map[clf_name]
    params = clf_hyperparams_map[clf_name]
    clf = GridSearchCV(clf, params, cv=4, scoring='f1_weighted', n_jobs=-1)
    clf.fit(X_train, y_train)
    return clf


def evaluate(y_test, y_pred):
    scores = {
        'accuracy': accuracy_score(y_test, y_pred),
        'f1_macro': f1_score(y_test, y_pred, average='macro'),
        'f1_micro': f1_score(y_test, y_pred, average='micro'),
        'f1_weighted': f1_score(y_test, y_pred, average='weighted'),
        'precision_weighted': precision_score(y_test, y_pred, average='weighted'),
        'recall_weighted': recall_score(y_test, y_pred, average='weighted')
    }
    return scores


def is_valid(clf_name):
    supported_clfs = [
        clf for clf in config.supported_classifiers if clf != 'Baseline'
    ]
    if clf_name not in supported_clfs:
        print('Supported classifiers:', supported_clfs)
        return False
    return True


def create_clf_params_product_generator(params_grid):
    keys = params_grid.keys()
    vals = params_grid.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


def softmax(x):
    return np.exp(x) / sum(np.exp(x))


def get_top_k_predictions(model, X_test, k):
    preds = model.predict_proba(X_test)
    k_preds = []
    for pred in preds:
        k_labels = np.argsort(-pred)[:k]
        k_scores = softmax(pred[k_labels])
        k_preds.append(zip(k_labels, k_scores))
    return k_preds


def inverse_transform_labels(encoder, k_preds):
    label_mapping = dict(
        zip(encoder.transform(encoder.classes_), encoder.classes_))
    k_preds_new = [(label_mapping[pred[0]], pred[1]) for k_pred in k_preds
                   for pred in k_pred]
    return k_preds_new
