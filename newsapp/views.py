# importing api 
from django.shortcuts import render 
from newsapi.newsapi_client import NewsApiClient 

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

