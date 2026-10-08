# Assignment 4

To reproduce the code:

- run data_extractor.py to extract the eeg data and markers from the .xdf file. This saves the data to a pickle file
- run train_lda.py to extract the epochs, the feature and train the lda. This also saves the features to a .csv file
- run feature_stability.py to load the features from the .csv and check their stability
