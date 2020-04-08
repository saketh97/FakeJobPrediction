from Allcodefiles.Dataread import read_csv
from Allcodefiles.DataHandling import missing_values
from Allcodefiles.DataHandling import train_test

from Allcodefiles.DataHandling import texthandling
def training():
    #try:
        data = read_csv('data/fake_job_postings.csv')
        #print('missing data')
        data = missing_values(data)
    ##    X_train, X_test, y_train, y_test = train_test(
    ##                        data.drop('fraudulent',axis=1),data['fraudulent'])
        #print('text handling')
        data = texthandling(data)
        #print('saving')
        #data.to_csv('fake_job_postings.csv',index=False)
    #except Exception as e:
    #    print('error raised while training')
    #    raise Exception(e)
