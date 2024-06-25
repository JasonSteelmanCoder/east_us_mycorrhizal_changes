import os
from dotenv import load_dotenv
import csv
import numpy as np
import matplotlib.pyplot as plt
import re

load_dotenv()

regions = [
    "Outer Coastal Plain Mixed Forest Province",
    "Southeastern Mixed Forest Province",
    "Eastern Broadleaf Forest Province",
    "Midwest Broadleaf Forest Province",
    "Central Interior Broadleaf Forest Province",
    "Central Appalachian Broadleaf Forest-Coniferous Forest-Meadow Province",
    "Laurentian Mixed Forest Province",
    "Prairie Parkland (Temperate) Province",
    "Northeastern Mixed Forest Province",
    "Adirondack-New England Mixed Forest--Coniferous Forest--Alpine Meadow Province",
    "Lower Mississippi Riverine Forest Province",
    "Everglades Province"
]

for region in regions:
    current_region = region

    pcts_adapted = []
    pcts_em = []

    with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/adaptation_by_county.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
            else:
                if row[12] == current_region:
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
    plt.title(f'Percent of Fire Adaptation Versus Ectomycorrhizal Association:\n{current_region}')
    plt.legend()

    plt.savefig(f"C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/dot_plots/adaptation_by_county_{re.sub(r'[^a-zA-Z0-9_\-.]', '_', region)}.png")
    plt.clf()
