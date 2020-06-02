#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 09:25:56 2020

@author: louis
"""
import requests
from bs4 import BeautifulSoup
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
def tes(url,filename):
    #爬取每篇新聞內容
    def GetNewsContent(WebAddr):
        global news_dic
        article=[]
        res=requests.get(WebAddr)
        bs=BeautifulSoup(res.text,'lxml')
        
        for i in bs.find('div',attrs={"class":"article-content__paragraph"}).find_all('p'):
            if i != None:
                article.append(i.text)
        return article
    #對新聞內容做jieba斷詞
    def GenKeywords(s,threshold):
        global news
        remainderWords=[]
        stopWords=[]
        count_news={}
        news={}
        with open('stopWords.txt', 'r', encoding='UTF-8') as file:
            for data in file.readlines():
                data = data.strip()
                stopWords.append(data)
        text=jieba.cut(str(s),cut_all=False)
        remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', text))     
        for word in remainderWords:
            if word not in count_news:
                count_news[word]=1
            else:
                count_news[word]+=1
        for key in count_news:
            if count_news[key]>=threshold:
                news[key]=count_news[key]
        return news
        
       
    #主程式開始
    news_dic={}
    threshold=3   
    stopWords=[]
    segments=[]
    remainderWords=[]
    res=requests.get(url)
    bs=BeautifulSoup(res.text,'lxml')
    count=0
    for title in bs.find_all('div',attrs={'class':'story-list__text'}):
        if title.find('a').get('href') != '#':
            if count<=9:
                WebAddr='https://udn.com'+title.find('a').get('href')
                GenKeywords(GetNewsContent(WebAddr),threshold)
                for i in GenKeywords(GetNewsContent(WebAddr),threshold):
                    if i in news_dic.keys():
                        news_dic[i]=news_dic[i]+news[i]
                    else:
                        news_dic.setdefault(i,news[i])
                count+=1
    
    #製作文字雲
    def FuncFilter(a):
        if (a not in stopWords and a != '\n'):
            return a
    textWords=[]
    for i in news_dic.keys():
        textWords.append(i)
    
    afterFilter=filter(FuncFilter, textWords)
    afterFilter_SpaceSplit = " ".join(afterFilter)    
    wc = WordCloud(background_color="white",    #   背景顏色
                   max_words=500,              #   最大詞數             
                   max_font_size=60,           #   顯示字體的最大值 max size=150
                   font_path='/Users/louis/Library/Group Containers/UBF8T346G9.Office/FontCache/4/CloudFonts/TTC/78992571833.ttc',              #   解決顯示口字型亂碼問題，可進入C:/Windows/Fonts/目錄更換字體
                   random_state=42,             #   為每一詞返回一個PIL顏色
                   prefer_horizontal=5)
    wc.generate(afterFilter_SpaceSplit)
    plt.figure(figsize=(10,5))
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(filename)

