import os
from dotenv import load_dotenv
import csv
import numpy as np
import matplotlib.pyplot as plt

load_dotenv()

pcts_adapted = []
pcts_em = []

with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/adaptation_by_county.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    i = 0
    for row in reader:
        if i == 0:
            i += 1
        else:
            pcts_adapted.append(float(row[4]))
            pcts_em.append(float(row[9]))

pcts_adapted_array = np.array(pcts_adapted[1:])
pcts_em_array = np.array((pcts_em[1:]))

coefficients = np.polyfit(pcts_adapted_array, pcts_em_array, 1)
polynomial = np.poly1d(coefficients)
y_fit = polynomial(pcts_adapted_array)

print(coefficients)
print(polynomial)

plt.scatter(pcts_adapted_array, pcts_em_array)
plt.plot(pcts_adapted_array, y_fit, 'k-', label="Line of Best Fit")
plt.xlabel('Percent of Basal Area Adapted to Fire')
plt.ylabel('Percent of Basal Area With Ectomycorrhizal Association')
plt.title('Percent of Fire Adaptation Versus Ectomycorrhizal Association')
plt.legend()
plt.show()