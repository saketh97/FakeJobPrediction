import re
from sklearn.model_selection import train_test_split
def missing_values(data):
    """
    All columns might contain missing values we have to decide how to handle
    each column. Some columns need to handled seperately.
    """

    """1.location"""

    data['location'].fillna('No Info',inplace=True)
    withoutcomma = data[~data['location'].str.contains(",")].index
    withcomma = data[data['location'].str.contains(",")].index

    for i in withcomma:
        data.loc[i,'country']=data.loc[i,'location'].split(',')[0]
        data.loc[i,'province']=data.loc[i,'location'].split(',')[1]
        data.loc[i,'city']=data.loc[i,'location'].split(',')[2]
    for i in withoutcomma:
        data.loc[i,'country']=data.loc[i,'location']

    data['province'].fillna('No Info',inplace=True)
    data['city'].fillna('No Info',inplace=True)
    data['province'].replace(' ','No Info',inplace=True)
    data['city'].replace(' ','No Info',inplace=True)

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
                data[i].fillna('No Info',inplace=True)
            else:
                daata[i].fillna(0,inplace=True)
    return data


def train_test(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.06, random_state=10)

    return X_train, X_test, y_train, y_test
