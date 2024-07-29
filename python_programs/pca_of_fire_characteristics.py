# uncomment lines 18, 27-28 to add species labels to the plot

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/pca_input_7_29_2024.csv')

X = df.iloc[:, 2:7].values
colors = df.iloc[:, 0].values
sizes = df.iloc[:, 7] * 60
# labels = df.iloc[:, 1]

X_standardized = StandardScaler().fit_transform(X)

pca = PCA(n_components=2)
principal_components = pca.fit_transform(X_standardized)

plt.figure(figsize = (8, 6))
plt.scatter(principal_components[:, 0], principal_components[:, 1], c = colors, cmap = 'viridis', edgecolor='k', s=sizes)
# for i, label in enumerate(labels):
#     plt.annotate(label, (principal_components[i, 0], principal_components[i, 1]), (principal_components[i, 0] + 0.1, principal_components[i, 1]), fontsize = 7)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA of fire characteristics of various common species')
plt.show()