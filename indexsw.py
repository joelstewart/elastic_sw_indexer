import requests
from elasticsearch import Elasticsearch
import json

#configs
host="192.168.56.10"
port=9200
esrest='http://'+host+':'+str(port)
verbose=True
separate=False

#iterates through pages of sw stuff and indexes it
def idxsw(indx, type, swapi):
  r=requests.get(swapi+'?page=1')
  while r.status_code == 200:
    j = json.loads(r.content)
    for obj in j['results']:
      id = obj['url']
      if verbose:
	print obj
      print id
      es.index(index=indx, doc_type=type, id=id, body=obj)
    if 'None' !=  str(j['next']):
       r = requests.get(j['next'])
    else:
      return

#test es running 
res = requests.get(esrest)
print(res.content)
es = Elasticsearch([{'host': host, 'port': port}])

#index into separate indexes...  
if (separate):
  idxsw('sw_people','people','http://swapi.co/api/people/')
  idxsw('sw_species','species','http://swapi.co/api/species/')
  idxsw('sw_films','films','http://swapi.co/api/films/')
  idxsw('sw_planets','planets','http://swapi.co/api/planets/')
  idxsw('sw_starships','starships','http://swapi.co/api/starships/')
  idxsw('sw_vehicles','vehicles','http://swapi.co/api/vehicles/')
else:
  idxsw('swapi','people','http://swapi.co/api/people/')
  idxsw('swapi','species','http://swapi.co/api/species/')
  idxsw('swapi','films','http://swapi.co/api/films/')
  idxsw('swapi','planets','http://swapi.co/api/planets/')
  idxsw('swapi','starships','http://swapi.co/api/starships/')
  idxsw('swapi','vehicles','http://swapi.co/api/vehicles/')

    
