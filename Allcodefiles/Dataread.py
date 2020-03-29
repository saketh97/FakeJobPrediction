import pandas as pd

def read_csv(path):
    try:
        if('csv' == path.split(".")[-1]):
            data = pd.read_csv(path)
        else:
            print("The files is not a CSV file")
    except Exception as e:
        print('error raised while reading')
        raise Exception(e)
    return data
