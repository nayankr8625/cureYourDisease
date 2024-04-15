# Importing libraries
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import mode
from sklearn.svm import SVC
import seaborn as sns
import pandas as pd
import numpy as np
import joblib

import warnings
# Suppress scikit-learn warnings
warnings.filterwarnings("ignore", category=UserWarning)

class PredictDisease:

    def __init__(self,conditions,data=pd.read_csv("data/Training.csv")):
        self._data = data
        self._condition = conditions
        self._encoder = LabelEncoder()
        
        self._data["prognosis"] = self._encoder.fit_transform(self._data["prognosis"])

    def model_training(self):
        self._data.dropna(axis=1,inplace=True)

        X = self._data.iloc[:,:-1]
        y = self._data.iloc[:, -1]
        # Training the models on whole data
        final_svm_model = SVC()
        final_nb_model = GaussianNB()
        final_rf_model = RandomForestClassifier(random_state=18)

        final_svm_model.fit(X, y)
        final_nb_model.fit(X, y)
        final_rf_model.fit(X, y)

        # Saving Trained models
        joblib.dump(final_svm_model, 'model_weights/final_svm_model.pkl')
        joblib.dump(final_nb_model, 'model_weights/final_nb_model.pkl')
        joblib.dump(final_rf_model, 'model_weights/final_rf_model.pkl')
    
    def process_labels(self):
        self._data.dropna(axis=1,inplace=True)
        X = self._data.iloc[:,:-1]
        # Symptoms prediction function
        symptoms = X.columns.values
        # Creating a symptom index dictionary to encode the
        # input symptoms into numerical form
        symptom_index = {}
        for index, value in enumerate(symptoms):
            symptom = " ".join([i.capitalize() for i in value.split("_")])
            symptom_index[symptom] = index

        data_dict = {
            "symptom_index": symptom_index,
            "predictions_classes": self._encoder.classes_
        }
        return data_dict
    
    def load_trained_model(self):
        final_svm_model = joblib.load('model_weights/final_svm_model.pkl')
        final_nb_model = joblib.load('model_weights/final_nb_model.pkl')
        final_rf_model = joblib.load('model_weights/final_rf_model.pkl')

        return {
            "naive_bayes": final_nb_model,
            "svm": final_svm_model,
            "random_forest": final_rf_model
        }
        
    
    def predictDisease(self):
        symptoms = self._condition.split(",")
        data_dict = self.process_labels()
        models = self.load_trained_model()
        final_rf_model = models["random_forest"]
        final_nb_model = models["naive_bayes"]
        final_svm_model = models["svm"]
        # Creating input data for the models
        input_data = [0] * len(data_dict["symptom_index"])
        for symptom in symptoms:
            index = data_dict["symptom_index"][symptom]
            input_data[index] = 1

        # Reshaping the input data and converting it
        # into a suitable format for model predictions
        input_data = np.array(input_data).reshape(1, -1)

        # Generating individual outputs
        rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
        nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
        svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]

        # Finding the mode using Counter
        predictions_list = [rf_prediction, nb_prediction, svm_prediction]
        count_predictions = Counter(predictions_list)
        final_prediction = count_predictions.most_common(1)[0][0]

        predictions = {
            "rf_model_prediction": rf_prediction,
            "naive_bayes_prediction": nb_prediction,
            "svm_model_prediction": svm_prediction,
            "final_prediction": final_prediction
        }
        return predictions


if __name__=="__main__":

    ob = PredictDisease(conditions="Itching,Skin Rash,Nodal Skin Eruptions")
    print(ob.predictDisease())