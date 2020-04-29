# importing api 
from django.shortcuts import render, redirect
from newsapi.newsapi_client import NewsApiClient
import datetime 
from bs4 import BeautifulSoup
import requests
import json
newsapi = NewsApiClient(api_key ='950064c202904c90b89cb52b2c859a98')
state_name_mapping = {}
# Create your views here. 
def index(request,keyw=None, coun='in'): 
	if(keyw==None or keyw=="None"):
		top = newsapi.get_top_headlines(country=coun)
	else:
		top = newsapi.get_top_headlines(q=keyw,country=coun)
	 
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
		# print(f) 
	mylist = zip(news, sw, desc, img, url) 

	return render(request, 'newsapp/index.html', context ={"mylist":mylist, "coun":coun, "key":keyw}) 

def search(request):
	if(request.method=="POST"):
		keyword = request.POST['word']
		return redirect(index, keyw=keyword, coun='in')
	else:
		print("no post")
		return redirect(index, keyw=None)

def map(request):
	x = requests.get('https://api.covid19india.org/data.json')
	y = x.json()
	
	a = y['statewise']

	for state in a:
		state_name_mapping[state['statecode'].lower()] = state['state']
	# print("state mapping: \n\n",state_name_mapping)

	x = requests.get('https://api.covid19india.org/states_daily.json')
	y = x.json()
	confirmed={}
	recovered={}
	deceased={}
	b =y['states_daily']
	states=[]
	for i in b:
		if(i['status']=="Confirmed"):
			for j in i:
				# confirmed[j]=i[j]
				if j!= "status" and j!="date":
					states.append(j)
		break
	for state in states:
		confirmed[state] = {'labels':[],'data':[]}	
		recovered[state] = {'labels':[],'data':[]}		
		deceased[state] = {'labels':[],'data':[]}		
		for i in b:
			if(i['status']=="Confirmed"):
				confirmed[state]['labels'].append(i['date'])
				confirmed[state]['data'].append(i[state])
			elif(i['status']=="Recovered"):
				recovered[state]['labels'].append(i['date'])
				recovered[state]['data'].append(i[state])
			elif(i['status']=="Deceased"):
				deceased[state]['labels'].append(i["date"])
				deceased[state]['data'].append(i[state])
	# print(deceased)
	del state_name_mapping['tt']
	x_ = requests.get('https://api.covid19india.org/state_district_wise.json').json()
	x_ = json.dumps(x_)
	
	return render(request, 'newsapp/map.html', context={"statewise":json.dumps(a),"confirmed":json.dumps(confirmed),"recovered":json.dumps(recovered),"deceased":json.dumps(deceased),"codes":json.dumps(state_name_mapping), "code_map":state_name_mapping, "table":x_})

def help(request, c_id=None, s_id=None):
	x = requests.get('https://api.covid19india.org/resources/resources.json').json()['resources']
	states=['All States']
	category=[]
	for i in x:
		if(i['state'] not in states):
			states.append(i['state'])
		if(i['category'] not in category):
			category.append(i['category'])
	ind = [i for i in range(0,len(category))]
	ind2 = [i for i in range(0,len(states))]

	cat = zip(ind,category)
	s=zip(ind2,states)

	if(c_id==None):
		return render(request, 'newsapp/help.html', context={"category":cat})
	else:
		lis=[]
		x = requests.get('https://api.covid19india.org/resources/resources.json').json()['resources']
		for i in x:
			if(s_id==None and i['category']==category[int(c_id)]  ):
				lis.append(i)
			elif(s_id!=None and int(s_id)==0 and i['category']==category[int(c_id)]  ):
				lis.append(i)
			elif(s_id!=None and i['state']==states[int(s_id)] and i['category']==category[int(c_id)]):
				lis.append(i)
		# print(len(lis))
		if s_id==None:
			s_id=0
		return render(request, 'newsapp/helpCategory.html', context={"list":lis, "category":category[int(c_id)],"states":s, "c_id":c_id,"s_id":s_id})

def trend(request, tr="COVID"):
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
	else:
		x=_.strftime("%Y-%m-%d")

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

