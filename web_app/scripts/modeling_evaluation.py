import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report


# Support Vector Machine pipeline
def svm_pipeline(X_train, X_test, y_train, y_test):
    svm_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('svm', SVC(kernel='linear', class_weight='balanced'))
    ])

    svm_pipeline.fit(X_train, y_train)
    y_pred_svm = svm_pipeline.predict(X_test)

    cr_svm = classification_report(y_test, y_pred_svm, target_names=['negative', 'neutral', 'positive'])
    cm_svm = confusion_matrix(y_test, y_pred_svm)

    return svm_pipeline, cr_svm, cm_svm


# K-Nearest Neighbor pipeline
def knn_pipeline(X_train, X_test, y_train, y_test):
    knn_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('knn', KNeighborsClassifier(n_neighbors=3))
    ])

    knn_pipeline.fit(X_train, y_train)
    y_pred_knn = knn_pipeline.predict(X_test)

    cr_knn = classification_report(y_test, y_pred_knn, target_names=['negative', 'neutral', 'positive'])
    cm_knn = confusion_matrix(y_test, y_pred_knn)

    return knn_pipeline, cr_knn, cm_knn


# Naive Bayes pipeline
def nb_pipeline(X_train, X_test, y_train, y_test):
    nb_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('nb', MultinomialNB())
    ])

    nb_pipeline.fit(X_train, y_train)
    y_pred_nb = nb_pipeline.predict(X_test)

    cr_nb = classification_report(y_test, y_pred_nb, target_names=['negative', 'neutral', 'positive'])
    cm_nb = confusion_matrix(y_test, y_pred_nb)

    return nb_pipeline, cr_nb, cm_nb


def modeling_and_evaluation(filepath, chosen_model):
    if '.csv' in filepath:
        df = pd.read_csv(filepath)
    elif '.xlsx' in filepath:
        df = pd.read_excel(filepath)

    X = df["content"]
    y = df["hard_label"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if chosen_model == 'svm':
        pipeline, cr, cm = svm_pipeline(X_train, X_test, y_train, y_test)
    elif chosen_model == 'knn':
        pipeline, cr, cm = knn_pipeline(X_train, X_test, y_train, y_test)
    elif chosen_model == 'nb':
        pipeline, cr, cm = nb_pipeline(X_train, X_test, y_train, y_test)

    return pipeline, cr, cm