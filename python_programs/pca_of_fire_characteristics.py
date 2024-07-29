# uncomment lines 18, 27-28 to add species labels to the plot

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from adjustText import adjust_text

load_dotenv()

df = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/pca_input_7_29_2024.csv')

X = df.iloc[:, 2:7].values
colors = df.iloc[:, 0].values
sizes = df.iloc[:, 8]
labels = df.iloc[:, 1]

X_standardized = StandardScaler().fit_transform(X)

pca = PCA(n_components=2)
principal_components = pca.fit_transform(X_standardized)

plt.figure(figsize = (10, 8))
plt.scatter(principal_components[:, 0], principal_components[:, 1], c = colors, edgecolor='k', s=sizes * 0.01, linewidths=0.5)
texts = []
for i, label in enumerate(labels):
    texts.append(plt.annotate(label, (principal_components[i, 0], principal_components[i, 1]), fontsize = 7))
adjust_text(texts, only_move={'texts':'xy'})
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA of fire characteristics of various common species')
plt.show()