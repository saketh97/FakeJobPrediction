import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from Allcodefiles.Exceptionhandling import handle

def train_and_save_model(data):
    try:
        print("Model Training")
        X_train = data.drop('fraudulent',axis = 1)
        y_train = data['fraudulent']

        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        pickle.dump( sc, open( "model/scaler.p", "wb" ))

        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators = 100 , criterion = 'entropy', random_state =1)

        model.fit(X_train,y_train)

        filename = 'model/finalized_model.p'
        pickle.dump(model, open(filename, 'wb'))
    except Exception as e:
        handle('Model Creation and training')
