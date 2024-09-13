import pandas as pd
import umap
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/pca_input_7_30_2024.csv')

vals = df.iloc[:, 2:7]

# note that n_neighbors is set to 5, instead of the default 15, due to the small number of records in the dataset
reducer = umap.UMAP(n_neighbors=5, min_dist=0.1, n_components=2, random_state=26)
embedding = reducer.fit_transform(vals.values)

colors = df.iloc[:, 0].values
sizes = df.iloc[:, 8]
labels = df.iloc[:, 1]

plt.figure(figsize=(12, 8))
plt.scatter(embedding[:, 0], embedding[:, 1], c=colors, s=100)
for i, label in enumerate(labels):
    plt.annotate(label, (embedding[i, 0] + 0.1, embedding[i, 1]), fontsize = 7)
plt.xlabel('UMAP 1')
plt.ylabel('UMAP 2')
plt.title('UMAP of Fire Characteristics')
plt.show()