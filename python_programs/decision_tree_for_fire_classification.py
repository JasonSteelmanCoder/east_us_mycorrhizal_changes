import pandas as pd
import os
from dotenv import load_dotenv
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.inspection import permutation_importance
from sklearn.model_selection import LeaveOneOut, KFold, cross_val_score
from statistics import mean

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

clf = DecisionTreeClassifier(random_state=1)
clf.fit(encoded_features, encoded_target)

# PREDICT A NEW SPECIES
# new_instance = [54,88,0.4,None,0.0786,19.12,240]
# predicted_association = clf.predict([new_instance])
# decoded_predicted_association = le.inverse_transform(predicted_association)
# print(decoded_predicted_association)

# CHECK PERMUTATION IMPORTANCE OF EACH VARIABLE
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

# CHECK ACCURACY OF PREDICTIONS USING TWO METHODS
loo_model = DecisionTreeClassifier(random_state=1)
loo = LeaveOneOut()
loo_scores = cross_val_score(loo_model, encoded_features, encoded_target, cv=loo)
print(f"LOO Accuracy for fire adaptation: {loo_scores.mean() * 100}%")

kf_model = DecisionTreeClassifier(random_state=1)
kf = KFold(n_splits=3, shuffle=True)
kf_scores = []
for i in range(150):
    scores = cross_val_score(kf_model, encoded_features, encoded_target, cv=kf)
    kf_scores.append(scores.mean())
print(f"k-Fold Accuracy for fire adaptation: {mean(kf_scores) * 100}%")

# CHECK ACCURACY OF PREDICTIONS AGAINST SPECIES WITH 6/7 VARIABLES
test_data = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/input_to_accuracy_test.csv')
test_data = test_data.dropna(subset=["fire_classification"])

test_features_df = test_data.iloc[:, 1:8]
test_features_lol = test_features_df.values.tolist()

test_target = list(test_data.iloc[:, 9])

flattened_test_features = []
for k in range(7):
    for test_value in test_features_df.iloc[:, k]:
        flattened_test_features.append(test_value)

encoded_test_features = [item for item in test_features_lol]
encoded_test_target = le.transform(test_target)

test_accuracy = clf.score(encoded_test_features, encoded_test_target)
print(f'Test accuracy: {test_accuracy * 100}%')