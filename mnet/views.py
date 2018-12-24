# -*- coding: utf-8 -*-
from django.shortcuts import render
import pymongo
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import xlrd
import json

uri = "mongodb://yoo:123yoo@ds117109.mlab.com:17109/music_db_kic"
client = pymongo.MongoClient(uri)
music_db = client.music_db_kic
music_collection = music_db.music
df = pd.DataFrame(list(music_collection.find()))

# 콤보박스에서 년도 가져오기
x = 2009

# 장고에서 그래프 값 대입
df_2 = pd.read_excel('C:\work\Proj_music\music_ex.xlsx')
data = df_2[df_2['년월'] == x].groupby('활동유형').size()
month = sorted(df_2['년월'].unique())
male_single = (data[0])
male_duo = (data[1])
female_single = (data[2])
female_duo = (data[3])
mixed = (data[4])


def ajax_tag_autosearch(request):
    if request.Get.has_key('year'):


def main(request):
    return render(request, 'main.html',
                  {
                      "data": df,
                      "month": month,
                      "male": male_single + male_duo,
                      "female": female_single + female_duo,
                      "male_single": male_single,
                      "male_duo": male_duo,
                      "female_single": female_single,
                      "female_duo": female_duo,
                      "mixed": mixed
                  })
