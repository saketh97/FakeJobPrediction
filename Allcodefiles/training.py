from Allcodefiles.Dataread import read_csv
from Allcodefiles.DataHandling import missing_values
from Allcodefiles.DataHandling import texthandling
from Allcodefiles.DataHandling import categorical_cols_train
from model.Model import train_and_save_model
from Allcodefiles.Exceptionhandling import handle

def training():
    try:
        data = read_csv('data/train.csv')

        (data.pipe(missing_values).pipe(texthandling)
             .pipe(categorical_cols_train).pipe(train_and_save_model))

    except Exception as e:
        handle("Training piepline")
