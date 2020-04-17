import pandas as pd
from Allcodefiles.Exceptionhandling import handle

def read_csv(path):
    try:
        if('csv' == path.split(".")[-1]):
            data = pd.read_csv(path)
        else:
            print("The files is not a CSV file")
    except Exception as e:
        handle('file reading')
    return data
