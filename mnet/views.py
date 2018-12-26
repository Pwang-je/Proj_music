# -*- coding: utf-8 -*-
from django.shortcuts import render
import pymongo
import pandas as pd
import numpy as np
import seaborn as sns
import xlrd


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

