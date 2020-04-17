import re
import string
import math
import pandas as pd
from nltk.cluster import cosine_distance
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from nltk.corpus import wordnet
import category_encoders as ce
import pickle
from Allcodefiles.Exceptionhandling import handle

stop_words = set(stopwords.words('english'))


def missing_values(data):
    print('Handling Missing Data')
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
    try:
        data['location'].fillna('no info',inplace=True)
        withoutcomma = data[~data['location'].str.contains(",")].index
        withcomma = data[data['location'].str.contains(",")].index

        for i in withcomma:
            data.loc[i,'country']=data.loc[i,'location'].split(',')[0].strip()
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
    except Exception as e:
        handle('missing data handling process')

def texthandling(data):
        print('Text Handling')
        try:
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
                data.loc[i,'title'] = removeuncessary(data.loc[i,'title'])
                data.loc[i,'department'] = removeuncessary(data.loc[i,'department'])
                data.loc[i,'industry'] = removeuncessary(data.loc[i,'industry'])
                data.loc[i,'function'] = removeuncessary(data.loc[i,'function'])

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

                data.loc[i,'title_and_job_similarity'] = synonym_relation(data.loc[i,'title'], data.loc[i,'description'])
                data.loc[i,'title_and_req_similarity'] = synonym_relation(data.loc[i,'title'], data.loc[i,'requirements'])
                data.loc[i,'profile_and_job_similarity'] = synonym_relation(data.loc[i,'company_profile'], data.loc[i,'description'])
                data.loc[i,'profiel_and_req_similarity'] = synonym_relation(data.loc[i,'company_profile'], data.loc[i,'requirements'])
                data.loc[i,'title_and_department_syn_similarity'] = synonym_relation(data.loc[i,'title'],data.loc[i,'department'])
                data.loc[i,'title_and_industry_syn_similarity'] = synonym_relation(data.loc[i,'title'],data.loc[i,'industry'])
                data.loc[i,'title_and_function_syn_similarity'] = synonym_relation(data.loc[i,'title'],data.loc[i,'function'])
                data.loc[i,'industry_and_department_syn_similarity'] = synonym_relation(data.loc[i,'industry'],data.loc[i,'department'])
                data.loc[i,'function_and_department_syn_similarity'] = synonym_relation(data.loc[i,'function'],data.loc[i,'department'])
                data.loc[i,'industry_and_function_syn_similarity'] = synonym_relation(data.loc[i,'industry'],data.loc[i,'function'])

            for i in ['title_and_job_similarity','title_and_req_similarity','profile_and_job_similarity','profiel_and_req_similarity','title_and_department_syn_similarity','title_and_industry_syn_similarity','title_and_function_syn_similarity','function_and_department_syn_similarity','industry_and_department_syn_similarity','industry_and_function_syn_similarity']:
                data[i].fillna(0,inplace=True)
            data.drop(['company_profile','benefits','description','requirements','title','department','industry','function','job_id'],axis=1,inplace=True)
            return data
        except Exception as e:
            handle('Text handling process')

def stopwordsremove(text):
    try:
        word_token = word_tokenize(text)
        ps = PorterStemmer()
        filtered = [ps.stem(w.lower()) for w in word_token if not w in stop_words]
        return filtered
    except Exception as e:
        handle('stop words removing')


def removeuncessary(text):
    try:
        '''
        1. removing punctuations, 2. removing numbered words, 3. removing unknown characters
        '''
        text = re.sub('[%s]'%re.escape(string.punctuation),'',str(text))
        text = re.sub('\w*\d\w*', '',str(text))
        text = re.sub('[^a-zA-Z ]+', ' ',str(text))

        return text
    except Exception as e:
        handle('removing unnecessary text')

def synonym_relation(text1,text2):
    try:
        if(text1 == 'no info' or text2 == 'no info'):
            return 0
        else:
            text1 = stopwordsremove(text1)
            text2 = stopwordsremove(text2)
            syn_set = set()
            count  = 0
            if(len(text1) ==0 or len(text2) ==0):
                return 0
            if(len(text1) < len(text2)):
                for word in text2:
                    for syn in wordnet.synsets(word):
                        for l in syn.lemmas():
                            syn_set.add(l.name())

                for word in text1:
                    if word in syn_set:
                            count+=1
                return (count/len(text1))
            else:
                for word in text1:
                    for syn in wordnet.synsets(word):
                        for l in syn.lemmas():
                            syn_set.add(l.name())

                for word in text2:
                    if word in syn_set:
                            count+=1
                return (count/len(text2))
    except Exception as e:
        handle('synonym relation finding process')
def categorical_cols_train(data):
    try:
        print('Categorical Encoding')
        encoder = ce.BinaryEncoder(cols=['employment_type','required_experience','required_education','country'])
        newdata = encoder.fit_transform(data)
        pickle.dump( encoder, open( "model/encoder.p", "wb" ) )
        return newdata
    except Exception as e:
        handle('categorical column handling')
def categorical_cols_test(data):
    print('Categorical Encoding')
    try:
        encoder = pickle.load( open( "model/encoder.p", "rb" ) )
        newdata = encoder.transform(data)
        return newdata
    except Exception as e:
        handle('categorical columns handling for testing process')
