import argparse

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from const import MOUTH_LANDMARKS, NUMBER_HAND_LANDMARKS

RANDOM_SEED = 42
NUM_CLASSES = 3
DIMENSIONS = 3


dataset = 'data.csv'
model_path = "model.pkl"
scaler_path = "scaler.pkl"

def main(num_landmarks: int, model_folder:str):
    dataset_path = model_folder + '/' + dataset
    X_dataset = np.loadtxt(dataset_path, delimiter=',', dtype='float32', usecols=list(range(1, (num_landmarks * DIMENSIONS) + 1)))
    y_dataset = np.loadtxt(dataset_path, delimiter=',', dtype='int32', usecols=(0))

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_dataset)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_dataset, train_size=0.75, random_state=RANDOM_SEED)

    # Train Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    print("Random Forest Accuracy:", accuracy_score(y_test, rf_preds))

    # Train SVM
    svm_model = SVC(kernel="rbf", C=1.0, gamma="scale")
    svm_model.fit(X_train, y_train)
    svm_preds = svm_model.predict(X_test)
    print("SVM Accuracy:", accuracy_score(y_test, svm_preds))

    full_model_path = model_folder + '/' + model_path
    joblib.dump(rf_model, full_model_path)

    full_scaler_path = model_folder + '/' + scaler_path
    joblib.dump(scaler, full_scaler_path)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Train ML model')
    parser.add_argument('-t','--target', choices=['hand', 'face'])
    parser.add_argument('-f', '--folder', required=True)

    args = parser.parse_args()
    if args.target == 'hand':
        num_landmarks = NUMBER_HAND_LANDMARKS
    elif args.target == 'face':
        num_landmarks = len(MOUTH_LANDMARKS)
    else:
        num_landmarks = 0
    main(num_landmarks, args.folder)
