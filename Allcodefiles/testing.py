from Allcodefiles.Dataread import read_csv
from Allcodefiles.DataHandling import missing_values
from Allcodefiles.DataHandling import texthandling
from Allcodefiles.DataHandling import categorical_cols_test
from Allcodefiles.Predict import load_model_predict
from Allcodefiles.Exceptionhandling import handle

def testing():
    try:
        data = read_csv('data/test.csv')

        (data.pipe(missing_values).pipe(texthandling)
             .pipe(categorical_cols_test).pipe(load_model_predict))

    except Exception as e:
        handle('testing process')
