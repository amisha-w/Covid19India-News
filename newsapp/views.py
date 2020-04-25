# importing api 
from django.shortcuts import render 
from newsapi.newsapi_client import NewsApiClient
import datetime 
from bs4 import BeautifulSoup
import requests
import json


# Create your views here. 
def index(request,coun='in'): 
	newsapi = NewsApiClient(api_key ='950064c202904c90b89cb52b2c859a98') 
	top = newsapi.get_top_headlines(country=coun) 
	# sources = newsapi.get_sources()
	# print('\n\n\n',top)
	
	l = top['articles'] 
	desc =[] 
	news =[] 
	url=[]
	img =[] 
	sw=[]

	for i in range(len(l)): 
		f = l[i] 
		if(f['title']=="" or f['description']=="None"):
			continue
		news.append(f['title']) 
		sw.append(f['source']['name'])
		desc.append(f['description']) 
		url.append(f['url'])
		img.append(f['urlToImage']) 
	mylist = zip(news, sw, desc, img, url) 



	return render(request, 'newsapp/index.html', context ={"mylist":mylist, "coun":coun}) 

def map(request):
	x = requests.get('https://api.covid19india.org/data.json')
	y = x.json()
	# print((y['statewise']))
	for i in y['statewise']:
		print(i)
	return render(request, 'newsapp/map.html', context={"statewise":json.dumps(y['statewise'])})

def trend(request, tr):
	site = 'https://news.google.com'

	source = requests.get('https://news.google.com/topics/CAAqBwgKMMqAmAsw9KmvAw').text
	soup = BeautifulSoup(source, 'lxml')
	head=[]
	link=[]
	pic=[]
	src1=[]
	desc=[]
	time=[]
	iii=0
	err=0
	for article in soup.find_all('article'):
		try:
			# print("\n\n----------heading\t",article.h3.a.text)
			head.append(article.h3.a.text)
			link.append(site+article.h3.a['href'][1:])

		except:
			try:
				head.append(article.h4.a.text)
				link.append(site+article.h4.a['href'][1:])
				
			except:
				print('\n\n-------------------ERRORS iii: ',iii)
				err+=1
				
		try:
			pic.append(article.figure.img['src'])
		except:
			pic.append(None)

		try:
			src1.append(article.find('div', class_="SVJrMe").a.text)
		except:
			src1.append(None)
		try:
			desc.append(article.find('span',class_="xBbh9").text)
		except:
			desc.append(None)
		try:
			time.append(article.find('time').text)
		except:
			time.append(None)
		iii+=1


	articles=zip(head,link,pic,src1,desc,time)

	return render(request, 'newsapp/trend.html', context = { "articles" : articles, "tr" : tr }) 


def top(request,timey=1,coun='in',sour=None): 
	newsapi = NewsApiClient(api_key ='950064c202904c90b89cb52b2c859a98') 
	sources = newsapi.get_sources()['sources']
	sids=[]
	sName=[]
	for i in range(len(sources)):
		if(sources[i]['country']==coun):
			sids.append(sources[i]['id'] )
			sName.append(sources[i]['name'] )
	if(sour==None):
		sour=sids[0]
	src=zip(sids,sName)
	_ = datetime.datetime.now()
	y=_.strftime("%Y-%m-%d")
	x=""
	if(timey=="1"):
		x=_.strftime("%Y-%m-%d")
		print("-------------------is1")
	elif(timey=="2"):
		x1= _ - datetime.timedelta(days=7)
		x=x1.strftime("%Y-%m-%d")
	elif(timey=="3"):
		today = datetime.date.today()
		first = today.replace(day=1)
		lastMonth = first - datetime.timedelta(days=1)
		x=lastMonth.strftime("%Y-%m-%d")
	elif(timey=="4"):
		x1= _ - datetime.timedelta(days=365)
		x=x1.strftime("%Y-%m-%d")

	# print('mn\n\n\n-------------------------------------',sources)
	print("--------------------------",coun,sour,timey)
	top = newsapi.get_everything(from_param=x,
                                      to=y, sources=sour) 

	l = top['articles'] 
	desc =[] 
	news =[] 
	url=[]
	img =[] 
	sw=[]

	for i in range(len(l)): 
		f = l[i] 
		if(f['title']=="" or f['description']=="None"):
			continue
		news.append(f['title']) 
		sw.append(f['source']['name'])
		desc.append(f['description']) 
		url.append(f['url'])
		img.append(f['urlToImage']) 
	mylist = zip(news, sw, desc, img, url) 

	return render(request, 'newsapp/top.html', context ={"mylist":mylist, "timeopt":timey, "sources":src, "sour":sour, "coun":coun}) 

