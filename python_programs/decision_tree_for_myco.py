import pandas as pd
import os
from dotenv import load_dotenv
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.inspection import permutation_importance

load_dotenv()

input_file = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/input_to_decision_trees.csv')

features_df = input_file.iloc[:, 1:8]
features_lst_of_lsts = features_df.values.tolist()

target = list(input_file.iloc[:, 8])

flattened_features = []
for j in range(7):
    for value in features_df.iloc[:, j]:
        flattened_features.append(value)

le = LabelEncoder()
le.fit(target)

encoded_features = [item for item in features_lst_of_lsts]
encoded_target = le.transform(target)

clf = DecisionTreeClassifier()
clf.fit(encoded_features, encoded_target)

imp_data = permutation_importance(clf, encoded_features, encoded_target, n_repeats=700)
importances = imp_data.importances_mean
print('\n')
print("IMPORTANCE SCORES")
print('\n')
print(f"flame_duration_s: \t\t{importances[0]}")
print(f"percent_consumed: \t\t{importances[1]}")
print(f"mean_litter_k: \t\t\t{importances[2]}")
print(f"mean_litter_cn: \t\t{importances[3]}")
print(f"bark_diameter_ratio: \t\t{importances[4]}")
print(f"bark_vol_percent: \t\t{importances[5]}")
print(f"smoulder_duration: \t\t{importances[6]}")
print('\n')

# new_instance = [102.3,29.1,0.1828,83.15789474,0.0252,13,None]
# predicted_adaptation = clf.predict([new_instance])
# decoded_predicted_adaptation = le.inverse_transform(predicted_adaptation)
# print(decoded_predicted_adaptation)
