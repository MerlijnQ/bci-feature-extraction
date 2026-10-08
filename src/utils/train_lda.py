import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score 
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd

import pickle
from bandpower import BandPower
CHANNEL_IDX = [1, 3]


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
        epoch = epoch[:, CHANNEL_IDX] #assuming epoch shape is (samples, channels)
        feat = feature_extractor.compute(epoch)
        features.append(feat)
        print(feat.shape)

    return np.array(features)
    

def train_lda(features, labels):
    """
    Train an LDA classifier using the provided features and labels.
    """
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    pipeline = Pipeline([('scaler', StandardScaler()),
                          ('classifier', LinearDiscriminantAnalysis())])

    print(labels)
    print(features)

    scores = cross_val_score(pipeline, features, labels, cv=cv, scoring='balanced_accuracy', error_score='raise')
    print(f"Cross-validated accuracy: {np.mean(scores):.4f} ± {np.std(scores):.4f}")
    print(f"Individual fold accuracies: {scores}")

epochs, labels = load_epochs("epochs.pkl")
features = epoch_to_features(epochs)
data = pd.DataFrame(features)
data.to_csv("../../features_size_2.5.csv", index=False, header=False)
train_lda(features, labels)
