# elastic_sw_indexer

The Python-Elasticsearch lab at https://tryolabs.com/blog/2015/02/17/python-elasticsearch-first-steps/ provides a basic introduction into using Python to index data from https://swapi.co/  into Elasticsearch.   

This project takes that demonstration a few more steps.  The objective is to learn more about Elasticsearch mappings, search, and analytics.   


# prerequisites

 - Elasticsearch >= 2.4 
 - Python 2.7, with pip and virtualenv
 - docker

## basic setup

### install elasticsearch template
The template will allow for correct mappings when indexing the sw data.

```bash
$ curl -XPUT http://elasticsearch:9200/_template/sw_template -d@template.json
```

### create a python virtual env


```bash
$ git clone https://github.com/joelstewart/elastic_sw_indexer.git
$ virturalenv swesenv
$ source swesenv/bin/activate
$ cd elastic_sw_indexer
(swesenv)$ pip install -r requirements.txt
```

### Edit the configs 

Edit the indexsw.py file to point to your elastic instance.


### Run the indexer
Run the indexer.   This will add 6 indexes to Elasticsearch for the sw data: sw_people, sw_planets, sw_starships, sw_films, sw_vehicles, sw_species.

```bash
(swesenv)$ python indexsw.py
``` 

### Check it all worked
1) From a browser, check

http://elasticsearch:9200/sw_films/_search?pretty

You should see 7 json files for the films.

The indexer script has modified some of the json.  It has denormalized the relationship values.  This is because Elasticsearch lacks join capabilities like SQL.   It is necessary to generate good visualizations with readable values instead of keys.

2) From a browser, test a few queries

http://192.168.56.10:9200/sw*/_search?q=space&pretty

The _all field is enabled (https://www.elastic.co/guide/en/elasticsearch/reference/2.4/mapping-all-field.html), so this query has higher relevance for the "shortest" json containing the word space as a value of one of its fields.

### Run KIBI

Kibi has a community version to enable joins between dashboards.  This will allow selections on one dashboard to filter records on another.

You will need to first install the siren-join plugin into your elasticsearch.  See instructions here: https://github.com/sirensolutions/siren-join

Then run kibi using docker.  You can find instructions here:  https://hub.docker.com/r/sirensolutions/kibi-community-standalone/

For example:

```bash
$ docker run --name -e ELASTICSEARCH_URL=http://elasticsearch:9200 -p 5606:5606 -d sirensolutions/kibi-community-standalone:4.6.4-4
```

Once kibi is running, try importing the included visualizations and dashboard.  In Kibi -> settings -> objects, import the export.json file.  


 
# more to come?  

Explore using Sirenjoin to perform joins https://github.com/sirensolutions/siren-join


