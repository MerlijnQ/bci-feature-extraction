"""
Analyze feature stability over time
"""

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../features_size_2.5.csv", header=None)
data.iloc[:, 1:].plot()
plt.title("Feature Stability Over Time")
plt.show()
