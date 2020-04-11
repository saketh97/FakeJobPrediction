import re
import string
import math
from nltk.cluster import cosine_distance
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
stop_words = set(stopwords.words('english'))


def missing_values(data):
    """
    All columns might contain missing values we have to decide how to handle
    each column. Some columns need to handled seperately.
    """

    """
    1.location

    a second level of handling is done as of to remove numeric values in the
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


    """3. All other categorical columns and remaining numeric columns."""

    columns = data.columns
    for i in columns:
        if(data[i].isna().any()):
            if(data[i].dtypes == 'object'):
                data[i].fillna('no info',inplace=True)
                data[i] = data[i].str.lower()

            else:
                data[i].fillna(0,inplace=True)

    data.drop(['salary_range','location'],axis=1,inplace=True)
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
        This function is for handling text data columns company profile,
        description, requirements, benefits are there is multiple text in those
        columns we need to do something about them.
        '''
        stop_words = set(stopwords.words('english'))
        for i in range(0,data.shape[0]):

            data.loc[i,'company_profile'] = removeuncessary(data.loc[i,'company_profile'])
            data.loc[i,'description'] = removeuncessary(data.loc[i,'description'])
            data.loc[i,'requirements'] = removeuncessary(data.loc[i,'requirements'])
            data.loc[i,'benefits'] = removeuncessary(data.loc[i,'benefits'])
            data.loc[i,'title'] = re.sub('[%s]'%re.escape(string.punctuation),'',str(data.loc[i,'title']))

            words = str(data.loc[i,'company_profile'])
            if(words == 'no info'):
                data.loc[i,'company_profile_word_count'] = 0
            else:
                data.loc[i,'company_profile_word_count'] = len(words.split())

            words = str(data.loc[i,'benefits'])
            if(words == 'no info'):
                data.loc[i,'benefits_word_count'] = 0
            else:
                data.loc[i,'benefits_word_count'] = len(words.split())

            data.loc[i,'title_and_job_similarity'] = similarity_finder(data.loc[i,'title'], data.loc[i,'description'])
            data.loc[i,'title_and_req_similarity'] = similarity_finder(data.loc[i,'title'], data.loc[i,'requirements'])
            data.loc[i,'profile_and_job_similarity'] = similarity_finder(data.loc[i,'company_profile'], data.loc[i,'description'])
            data.loc[i,'profiel_and_req_similarity'] = similarity_finder(data.loc[i,'company_profile'], data.loc[i,'requirements'])

        data.drop(['company_profile','benefits','description','requirements'],axis=1,inplace=True)
        print(data.info())
        return data

def stopwordsremove(text):
    word_token = word_tokenize(text)
    ps = PorterStemmer()
    filtered = [ps.stem(w.lower()) for w in word_token if not w in stop_words]
    return filtered

def similarity_finder(text1,text2):
    if(text1 == 'no info' or text2 == 'no info'):

        return 0
    else:
        text1 = stopwordsremove(text1)
        text2 = stopwordsremove(text2)

        word_set = set(text1).union(set(text2))

        #tf calculation
        freq1 = FreqDist(text1)
        txt1_length = len(text1)
        txt1_tf_dict = dict.fromkeys(word_set,0)
        for word in text1:
            txt1_tf_dict[word] = freq1[word]/txt1_length

        freq2 = FreqDist(text2)
        txt2_length = len(text2)
        txt2_tf_dict = dict.fromkeys(word_set,0)
        for word in text2:
            txt2_tf_dict[word] = freq2[word]/txt2_length

        #idf calculation
        txt12_idf_dict = dict.fromkeys(word_set,0)
        txt12_length = 2
        for word in txt12_idf_dict.keys():
            if word in text1:
                txt12_idf_dict[word] +=1
            if word in text2:
                txt12_idf_dict[word] +=1
        for word, val in txt12_idf_dict.items():
            txt12_idf_dict[word] = 1 + math.log(txt12_length/float(val))

        #tf_idf calculations
        text1_tfidf_dict = dict.fromkeys(word_set,0)
        for word in text1:
            text1_tfidf_dict[word] = (txt1_tf_dict[word])*(txt12_idf_dict[word])
        text2_tfidf_dict = dict.fromkeys(word_set,0)
        for word in text2:
            text2_tfidf_dict[word] = (txt2_tf_dict[word])*(txt12_idf_dict[word])

        #cosine distance
        v1 = list(text1_tfidf_dict.values())
        v2 = list(text2_tfidf_dict.values())
        similarity = 1 - cosine_distance(v1,v2)
        return (similarity*100)

def removeuncessary(text):
    '''
    1. removing punctuations, 2. removing numbered words, 3. removing unknown characters
    '''
    text = re.sub('[%s]'%re.escape(string.punctuation),'',str(text))
    text = re.sub('\w*\d\w*', '',str(text))
    text = re.sub('[^a-z ]+', ' ',str(text))

    return text
