# importing api 
from django.shortcuts import render 
from newsapi.newsapi_client import NewsApiClient
import datetime 

# Create your views here. 
def index(request,coun='in'): 
	newsapi = NewsApiClient(api_key ='950064c202904c90b89cb52b2c859a98') 
	top = newsapi.get_top_headlines(country=coun) 
	# sources = newsapi.get_sources()
	print('\n\n\n',top)

	l = top['articles'] 
	desc =[] 
	news =[] 
	url=[]
	img =[] 

	for i in range(len(l)): 
		f = l[i] 
		if(f['title']=="" or f['description']=="None"):
			continue
		news.append(f['title']) 
		desc.append(f['description']) 
		url.append(f['url'])
		img.append(f['urlToImage']) 
	mylist = zip(news, desc, img, url) 

	return render(request, 'newsapp/index.html', context ={"mylist":mylist, "coun":coun}) 

def top(request,timey=1,coun='in',sour='google-news-in'): 
	newsapi = NewsApiClient(api_key ='950064c202904c90b89cb52b2c859a98') 
	sources = newsapi.get_sources()['sources']
	sids=[]
	sName=[]
	for i in range(len(sources)):
		if(sources[i]['country']==coun):
			sids.append(sources[i]['id'] )
			sName.append(sources[i]['name'] )
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
                                      to=y, q='bitcoin') 

	l = top['articles'] 
	desc =[] 
	news =[] 
	url=[]
	img =[] 

	for i in range(len(l)): 
		f = l[i] 
		if(f['title']=="" or f['description']=="None"):
			continue
		news.append(f['title']) 
		desc.append(f['description']) 
		url.append(f['url'])
		img.append(f['urlToImage']) 
	mylist = zip(news, desc, img, url) 

	return render(request, 'newsapp/top.html', context ={"mylist":mylist, "timeopt":timey, "sources":src, "sour":sour, "coun":coun}) 

