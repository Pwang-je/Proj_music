# -*- coding: utf-8 -*-
from django.shortcuts import render
import pymongo
import pandas as pd
import numpy as np
import pickle
import math
import xlrd

from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer

from scipy.sparse import csr_matrix
from scipy.sparse import hstack
from scipy.sparse import vstack
from sklearn.metrics import accuracy_score


# mongodb connection
uri = "mongodb://yoo:123yoo@ds117109.mlab.com:17109/music_db_kic"
client = pymongo.MongoClient(uri)
music_db = client.music_db_kic
music_collection = music_db.music
df = pd.DataFrame(list(music_collection.find()))

# 콤보박스에서 년도 가져오기
x = 2009

# data;
df_2 = pd.read_excel('C:\work\Proj_music\mnet_music777.xlsx')
df_3 = pd.read_excel('C:\work\Proj_music\music_ex.xlsx')
test_data = df_2[df_2['년월'] == x].groupby('활동유형').size()  # main용도.
month_data = sorted(df_2['년월'].unique())

# model;
with open('C:\\work\\Proj_music\\final_model', 'rb') as f:
    final_model = pickle.load(f)
with open('C:\\work\\Proj_music\\feature_list_singer_2.txt', 'rb') as f:
    feature_list_singer_2 = pickle.load(f)
with open('C:\\work\\Proj_music\\feature_list_pd_2.txt', 'rb') as f:
    feature_list_pd_2 = pickle.load(f)


def trans_music_type(x):
    if str(x) == 'OST':
        return 0
    if str(x) == '가요 > 락':
        return 1
    if str(x) == '가요 > 알앤비':
        return 2
    if str(x) == '가요 > 힙합':
        return 3
    if str(x) == '기타':
        return 4
    if str(x) == '댄스 > 댄스':
        return 5
    else:
        return 6


def main(request):

    # chart data;
    # year default = 2009;
    year = 2009
    a_process = np.array(df_2[df_2['년월'] == year].groupby('활동유형').size())
    activity_type = ['남성', '여성', '프로젝트', '혼성']
    df_process = pd.DataFrame(a_process, columns=['활동 수'])
    df_process['활동유형'] = activity_type

    cnt = 0
    for i in df_3['활동유형']:
        if i == 'Various Artists':
            df_3['활동유형'][cnt] = '프로젝트 | 그룹'
        cnt += 1

    alpha = df_3[df_3['년월'] == int(year)].groupby('활동유형').size()
    alpha = np.array(alpha)

    return render(request, 'main.html',
                  {
                      "month": month_data,
                      "male": a_process[0],
                      "female": a_process[1],
                      "project_group": a_process[2],
                      "mixed": a_process[3],
                      "male_single": alpha[1],
                      "male_duo": alpha[0],
                      "female_single": alpha[3],
                      "female_duo": alpha[2],
                  })


def chart(request):
    # month = request.GET['month']
    year = request.GET['year']

    a_process = np.array(df_2[df_2['년월'] == int(year)].groupby('활동유형').size())
    activity_type = ['남성', '여성', '프로젝트', '혼성']
    df_process = pd.DataFrame(a_process, columns=['활동 수'])
    df_process['활동유형'] = activity_type

    cnt = 0
    for i in df_3['활동유형']:
        if i == 'Various Artists':
            df_3['활동유형'][cnt] = '프로젝트 | 그룹'
        cnt += 1

    alpha = df_3[df_3['년월'] == int(year)].groupby('활동유형').size()
    alpha = np.array(alpha)

    return render(request, 'main.html',
                  {
                      "month": month_data,
                      "male": a_process[0],
                      "female": a_process[1],
                      "project_group": a_process[2],
                      "mixed": a_process[3],
                      "male_single": alpha[1],
                      "male_duo": alpha[0],
                      "female_single": alpha[3],
                      "female_duo": alpha[2],
                  })


def musicmodel(request):
    singer = request.GET['singer']
    producer = request.GET['composer']
    user_music_type = request.GET['music_type']

    singer = str(singer).replace(" ", "")
    producer = str(producer).replace(" ", "")
    user_music_type = trans_music_type(user_music_type)

    user_x = {"가수": [singer], "작곡": [producer], "장르": [user_music_type]}
    user_x = pd.DataFrame(user_x, columns=["가수", "작곡", "장르"])

    user_vectorizer_singer = TfidfVectorizer(ngram_range=(1, 1), vocabulary=feature_list_singer_2)
    user_vectorizer_pd = TfidfVectorizer(ngram_range=(1, 1), vocabulary=feature_list_pd_2)

    user_vec_singer = user_vectorizer_singer.fit_transform(user_x['가수'])
    user_vec_pd = user_vectorizer_pd.fit_transform(user_x['작곡'])
    user_vec_singer_pd = hstack((user_vec_singer, user_vec_pd))

    user_x_2 = hstack((user_vec_singer_pd, user_x['장르']))
    pred_user = final_model.predict(user_x_2)

    proba_model = final_model.predict_proba(user_x_2)
    proba = proba_model * 100
    # print(proba[0])

    # if proba > 50:
    #     proba_final

    if pred_user:
        msg = '축하합니다! 10위안에 들 수 있을 것 같아요!'
    else:
        msg = '아쉽네요! 10위안에 들 수 없을 것 같아요..'

    # activity type
    year = 2009

    a_process = np.array(df_2[df_2['년월'] == int(year)].groupby('활동유형').size())
    activity_type = ['남성', '여성', '프로젝트', '혼성']
    df_process = pd.DataFrame(a_process, columns=['활동 수'])
    df_process['활동유형'] = activity_type

    cnt = 0
    for i in df_3['활동유형']:
        if i == 'Various Artists':
            df_3['활동유형'][cnt] = '프로젝트 | 그룹'
        cnt += 1

    alpha = df_3[df_3['년월'] == int(year)].groupby('활동유형').size()
    alpha = np.array(alpha)

    proba_msg = '10위안에 들 확률은 <strong>' + '%d' % (round(proba[0][1], 2)) + '%</strong> 입니다.'

    return render(request, 'main.html',
                  {
                    'examp': msg,
                    "proba": proba_msg,
                    "month": month_data,
                    "male": a_process[0],
                    "female": a_process[1],
                    "project_group": a_process[2],
                    "mixed": a_process[3],
                    "male_single": alpha[1],
                    "male_duo": alpha[0],
                    "female_single": alpha[3],
                    "female_duo": alpha[2],
                  })
