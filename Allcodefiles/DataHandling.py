import re
import string
from sklearn.model_selection import train_test_split

def missing_values(data):
    """
    All columns might contain missing values we have to decide how to handle
    each column. Some columns need to handled seperately.
    """

    """
    1.location

    a second level of handling is done as of to remove numeric valus in the
    location data. regex is used to remove those numeric data and replace with
    no info.
    """

    data['location'].fillna('no info',inplace=True)
    withoutcomma = data[~data['location'].str.contains(",")].index
    withcomma = data[data['location'].str.contains(",")].index

    for i in withcomma:
        data.loc[i,'country']=data.loc[i,'location'].split(',')[0].strip()
        data.loc[i,'province']=data.loc[i,'location'].split(',')[1].strip()
        data.loc[i,'city']=data.loc[i,'location'].split(',')[2].strip()
        data.loc[i,'province'] = re.sub('^[0-9 ]*$','no info',data.loc[i,'province'])
        data.loc[i,'city'] = re.sub('^[0-9 ]*$','no info',data.loc[i,'city'])
    for i in withoutcomma:
        data.loc[i,'country']=data.loc[i,'location'].strip()

    data.drop(['location'],axis=1,inplace=True)

    """2.salary range"""

    data['salary_range'].fillna('0-0',inplace=True)

    for i in range(0,data.shape[0]):
        str = data.loc[i,'salary_range']
        if re.search(r'[a-z,A-Z]',str):
            data.loc[i,'salary_range']='0-0'

        if(data.loc[i,'salary_range'].find("-") != -1):
            data.loc[i,'minimum_salary'] = data.loc[i,
                                                'salary_range'].split('-')[0]
            data.loc[i,'maximum_salary'] = data.loc[i,
                                                'salary_range'].split('-')[1]
        else:
            data.loc[i,'minimum_salary'] = data.loc[i,'salary_range']
            data.loc[i,'maximum_salary'] = data.loc[i,'salary_range']

    data.drop(['salary_range'],axis=1,inplace=True)

    """3. All other categorical columns and remaining numeric columns."""

    columns = data.columns
    for i in columns:
        if(data[i].isna().any()):
            if(data[i].dtypes == 'object'):
                data[i].fillna('no info',inplace=True)
                data[i] = data[i].str.lower()

            else:
                data[i].fillna(0,inplace=True)
    return data


def train_test(X,y):
    '''
    For the training data provided we might need to split into train, test
    because we do not possess any test set to check. If we do possess something
    to test then this function is not required.
    '''

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                            test_size = 0.06, random_state=10)

    return X_train, X_test, y_train, y_test


def texthandling(data):
        '''
        This function is for hnadling text data columns company profile,
        description, requirements, benefits are there is multiple text in those
        columns we need to do something about them.
        '''
        ## company_profile, description, requirements, benifits
        '''
        1. removing punctuations, 2. removing numbered words, 3. removing unknown characters
        '''
        for i in range(0,data.shape[0]):

            data.loc[i,'company_profile'] = re.sub('[%s]'%re.escape(string.punctuation),'',str(data.loc[i,'company_profile']))
            data.loc[i,'description'] = re.sub('[%s]'%re.escape(string.punctuation),'',str(data.loc[i,'description']))
            data.loc[i,'requirements'] = re.sub('[%s]'%re.escape(string.punctuation),'',str(data.loc[i,'requirements']))
            data.loc[i,'benefits'] = re.sub('[%s]'%re.escape(string.punctuation),'',str(data.loc[i,'benefits']))


        for i in range(0,data.shape[0]):

            data.loc[i,'company_profile'] = re.sub('\w*\d\w*', '',str(data.loc[i,'company_profile']))
            data.loc[i,'description'] = re.sub('\w*\d\w*', '',str(data.loc[i,'description']))
            data.loc[i,'requirements'] = re.sub('\w*\d\w*', '',str(data.loc[i,'requirements']))
            data.loc[i,'benefits'] = re.sub('\w*\d\w*', '',str(data.loc[i,'benefits']))

        for i in range(0,data.shape[0]):

            data.loc[i,'company_profile'] = re.sub('[^a-z ]+', ' ',str(data.loc[i,'company_profile']))
            data.loc[i,'description'] = re.sub('[^a-z ]+', ' ',str(data.loc[i,'description']))
            data.loc[i,'requirements'] = re.sub('[^a-z ]+', ' ',str(data.loc[i,'requirements']))
            data.loc[i,'benefits'] = re.sub('[^a-z ]+', ' ',str(data.loc[i,'benefits']))

        print(data.info())
        return data
