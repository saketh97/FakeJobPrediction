from Allcodefiles.Dataread import read_csv
from Allcodefiles.DataHandling import missing_values,train_test_split
def training():
    try:
        data = read_csv('data/fake_job_postings.csv')
        data = missing_values(data)
        
    except Exception as e:
        print('error raised while training')
        raise Exception(e)
