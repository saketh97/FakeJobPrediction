import pickle
from Allcodefiles.Exceptionhandling import handle
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from Allcodefiles.Dataread import read_csv


def load_model_predict(data):
    try:
        X_test = data.drop('fraudulent',axis = 1)
        y_test = data['fraudulent']

        scaler = pickle.load( open( "model/scaler.p", "rb" ) )
        X_test = scaler.transform(X_test)

        filename = 'model/finalized_model.p'
        model = pickle.load(open(filename, 'rb'))

        y_pred = model.predict(X_test)
        score_and_save(y_pred)
    except Exception as e:
        handle('prediction process')



def score_and_save(y_pred):
    try:
        data = read_csv('data/test.csv')

        y_test = data['fraudulent']
        cm = confusion_matrix(y_test, y_pred)
        print("\n"+"SCORES")
        print("confusion matrix")
        print(cm)
        print('F1-Score'+' = '+str(round(f1_score(y_test, y_pred),4)))
        print('Precision'+' = '+str(round(precision_score(y_test, y_pred),4)))
        print('Recall'+' = '+str(round(recall_score(y_test, y_pred),4)))
        print('Accuracy'+' = '+str(round(accuracy_score(y_test,y_pred),4)))

        data['fraud_prediction'] = y_pred

        data.to_csv('predictionoutput/testsetprediction.csv')
    except Exception as e:
        handle('scoring and saving process')
