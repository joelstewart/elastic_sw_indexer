import requests
from elasticsearch import Elasticsearch
import json
import sys

#configs
host="192.168.56.10"
port=9200
esrest='http://'+host+':'+str(port)

#template mapping to use


#separate indexes or same index.
separate=True

#log data as it is added
verbose=True


#returns the int value as id from a url 
def idFromUrl(url):
  tokens= url.split("/")
  return int(tokens[len(tokens) - 2])

#returns in for string, or None
def asint(s):
  try:
    return int(s)     
  except:
    return None  

#modifies swapi json to replace some strings as ints
def format(j):
  if 'height' in j:
    j['height'] = asint(j['height'])
  if 'mass' in j:
    j['mass'] = asint(j['mass'])
  if 'diameter' in j:
    j['diameter'] = asint(j['diameter'])
  if 'population' in j:
    j['population'] = asint(j['population'])
  if 'orbital_period' in j:
    j['orbital_period'] = asint(j['orbital_period'])
  if 'surface_water' in j:
    j['surface_water'] = asint(j['surface_water'])
  if 'rotation_period' in j:
    j['rotation_period'] = asint(j['rotation_period'])
  if 'passengers' in j:
    j['passengers'] = asint(j['passengers'])
  if 'cargo_capacity' in j:
    j['cargo_capacity'] = asint(j['cargo_capacity'])
  if 'max_atmosphering_speed' in j:
    j['max_atmosphering_speed'] = asint(j['max_atmosphering_speed'])
  if 'diameter' in j:
    j['diameter'] = asint(j['diameter'])
  if 'crew' in j:
    j['crew'] = asint(j['crew'])
  if 'length' in j:
    j['length'] = asint(j['length'])
  if 'MGLT' in j:
    j['MGLT'] = asint(j['MGLT'])
  if 'cost_in_credits' in j:
    j['cost_in_credits'] = asint(j['cost_in_credits'])
  if 'average_lifespan' in j:
    j['average_lifespan'] = asint(j['average_lifespan'])
  if 'average_height' in j:
    j['average_height'] = asint(j['average_height'])

#iterates through pages of sw stuff and indexes it
def idxsw(indx, type, swapi):
  r=requests.get(swapi+'?page=1')
  while r.status_code == 200:
    j = json.loads(r.content)
    for obj in j['results']:      
      id = idFromUrl(obj['url'])
      format(obj)
      if verbose:
	print obj
      es.index(index=indx, doc_type=type, id=id, body=obj)
    if 'None' !=  str(j['next']):
       r = requests.get(j['next'])
    else:
      return

#test es running 
res = requests.get(esrest)
print(res.content)
es = Elasticsearch([{'host': host, 'port': port}])

#index   
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

    
