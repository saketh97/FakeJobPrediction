from Allcodefiles.Dataread import read_csv
from Allcodefiles.DataHandling import missing_values,train_test
def training():
    try:
        data = read_csv('data/fake_job_postings.csv')
        data = missing_values(data)
        X_train, X_test, y_train, y_test = train_test(data.drop('fraudulent',axis=1),data['fraudulent'])
    except Exception as e:
        print('error raised while training')
        raise Exception(e)
