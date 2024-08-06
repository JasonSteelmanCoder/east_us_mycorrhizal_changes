import pandas as pd
import os
from dotenv import load_dotenv
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.inspection import permutation_importance
from sklearn.model_selection import LeaveOneOut, KFold, cross_val_score

load_dotenv()

input_file = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/input_to_decision_trees.csv')
input_file = input_file.dropna()

features_df = input_file.iloc[:, 1:8]
features_lst_of_lsts = features_df.values.tolist()

target = list(input_file.iloc[:, 9])

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

# new_instance = [54,88,0.4,None,0.0786,19.12,240]
# predicted_association = clf.predict([new_instance])
# decoded_predicted_association = le.inverse_transform(predicted_association)
# print(decoded_predicted_association)

# imp_data = permutation_importance(clf, encoded_features, encoded_target, n_repeats=100000, n_jobs=-1)       # 100,000 repeats = ~5 minutes runtime
# importances = imp_data.importances_mean
# print('\n')
# print("IMPORTANCE SCORES FOR FIRE ADAPTATION")
# print('\n')
# print(f"flame_duration_s: \t\t{importances[0]}")
# print(f"percent_consumed: \t\t{importances[1]}")
# print(f"mean_litter_k: \t\t\t{importances[2]}")
# print(f"mean_litter_cn: \t\t{importances[3]}")
# print(f"bark_diameter_ratio: \t\t{importances[4]}")
# print(f"bark_vol_percent: \t\t{importances[5]}")
# print(f"smoulder_duration: \t\t{importances[6]}")
# print('\n')

loo_model = DecisionTreeClassifier()
loo = LeaveOneOut()
loo_scores = cross_val_score(loo_model, encoded_features, encoded_target, cv=loo)
print(f"LOO Accuracy for fire adaptation: {loo_scores.mean() * 100}%")

kf_model = DecisionTreeClassifier()
kf = KFold(n_splits=3, shuffle=True, random_state=1)
kf_scores = cross_val_score(kf_model, encoded_features, encoded_target, cv=kf)
print(f"k-Fold Accuracy for fire adaptation: {kf_scores.mean() * 100}%")
