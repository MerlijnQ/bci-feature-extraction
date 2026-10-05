import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score 
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, StandardScaler
from sklearn.pipeline import Pipeline

import pickle
from bandpower import BandPower

def load_epochs(file_path):
    with open(file_path, "rb") as f:
        epochs, labels = pickle.load(f)
    return epochs, labels

def epoch_to_features(epochs, fs=250, band=(8, 30)):
    """
    Convert epochs to features using band power extraction.
    """
    feature_extractor = BandPower(fs=fs, band=band)

    features = []
    for epoch in epochs:
        feat = feature_extractor.compute(epoch)
        features.append(feat)

    return np.array(features)

def train_lda(features, labels):
    """
    Train an LDA classifier using the provided features and labels.
    """
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    pipeline = Pipeline([(('scaler', StandardScaler()),
                          ('classifier', LinearDiscriminantAnalysis()))])

    scores = cross_val_score(pipeline, features, labels, cv=cv, scoring='accuracy')
    print(f"Cross-validated accuracy: {np.mean(scores):.4f} ± {np.std(scores):.4f}")
    print(f"Individual fold accuracies: {scores}")

epochs, labels = load_epochs("epochs.pkl")
features = epoch_to_features(epochs)
train_lda(features, labels)
