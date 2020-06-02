from flask import Flask, render_template,request
import requests
from bs4 import BeautifulSoup
from news_wordcloud import tes

tes('https://udn.com/news/cate/2/6639','scoical')
tes('https://udn.com/news/cate/2/7227','exerice')
tes('https://udn.com/news/cate/2/6645','stock_market')
tes('https://udn.com/news/cate/1013','travel')

def return_img_stream(img_local_path):
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream
def get_url_title(url):
    global html
    html=[]
    res=requests.get(url)
    bs=BeautifulSoup(res.text,'lxml')
    count=0
    for title in bs.find_all('div',attrs={'class':'story-list__text'}):
        if title.find('a').get('href') != '#':
            if count<=9:
                to_html={}
                WebAddr='https://udn.com'+title.find('a').get('href')
                to_html['title']=title.find('a').text
                to_html['url']=WebAddr
                html.append(to_html)
                count+=1
    return html

app=Flask(__name__) #__name__代表執行的模組
@app.route("/",methods=['POST','GET']) #含式的裝飾
def index():
    if request.method=='POST':
        if request.values['send']=='送出':
            return render_template('index.html',name=request.values['user'])
    return render_template('index.html',name="")
# show photo

@app.route('/500')
def exerice():
    img_path = '/Users/louis/Desktop/python/Flask/exerice.png'
    img_stream = return_img_stream(img_path)

    global html
    #to_html={}
    html=[]
    url='https://udn.com/news/breaknews/1/7#breaknews'
    res=requests.get(url)
    bs=BeautifulSoup(res.text,'lxml')
    count=0
    for title in bs.find_all('div',attrs={'class':'story-list__text'}):
        if title.find('a').get('href') != '#':
            if count<=9:
                to_html={}
                WebAddr='https://udn.com'+title.find('a').get('href')
                to_html['title']=title.find('a').text
                to_html['url']=WebAddr
                html.append(to_html)
                count+=1
    return render_template('index-1.html',
                           img_stream=img_stream,
                           Name=html,)
@app.route('/600')
def scoical():
    img_path = '/Users/louis/Desktop/python/Flask/scoical.png'
    img_stream = return_img_stream(img_path)
    
    url='https://udn.com/news/cate/2/6639'
    get_url_title(url)
    return render_template('index-2.html',
                           img_stream=img_stream,
                           Name=html,)
@app.route('/700')
def stock_market():
    img_path = '/Users/louis/Desktop/python/Flask/stock_market.png'
    img_stream = return_img_stream(img_path)
    
    url='https://udn.com/news/cate/2/6645'
    get_url_title(url)
    return render_template('index-3.html',
                           img_stream=img_stream,
                           Name=html,)
@app.route('/800')
def travel():
    img_path = '/Users/louis/Desktop/python/Flask/travel.png'
    img_stream = return_img_stream(img_path)
    
    url='https://udn.com/news/cate/1013'
    get_url_title(url)
    return render_template('index-4.html',
                           img_stream=img_stream,
                           Name=html,)  

    
if __name__ == '__main__':
    app.run(debug=True)
