# elastic_sw_indexer

The Python-Elasticsearch lab at https://tryolabs.com/blog/2015/02/17/python-elasticsearch-first-steps/ provides a basic introduction into using Python to index data from https://swapi.co/  into Elasticsearch.   

This project takes that demonstration a few more steps.  The objective is to learn more about Elasticsearch mappings, search, and analytics.   


# prerequisites

 - Elasticsearch >= 2.4 
 - Python 2.7, with pip and virtualenv

## basic setup

```bash
$ git clone https://github.com/joelstewart/elastic_sw_indexer.git
$ virturalenv swesenv
$ source swesenv/bin/activate
$ cd elastic_sw_indexer
(swesenv)$ pip install -r requirements.txt
```

Edit the configs in indexsw.py for your environment.

Install the template in elasticsearch:
```bash
$ curl -XPUT http://elasticsearch:9200/_template/sw_template -d@template.json
```

Run the indexer.   This will add 6 indexes to Elasticsearch for the sw data: sw_people, sw_planets, sw_starships, sw_films, sw_vehicles, sw_species.

```bash
(swesenv)$ python indexsw.py
``` 


# the index template 
The index template will turns off analysis for all string fields, except for the opening crawl text field in the sw_film type.   

# fixing the data
The sw data contains many fields in json that are strings that are numeric values.  The template could define those types as integer, and elasticsearch would be smart enough to know how to convert those strings to integers.   Instead, the indexing script takes care of changing types of fields.

# example queries

## full text queries

From a browser, test a few queries

http://192.168.56.10:9200/sw*/_search?q=space&pretty

The _all field is enabled (https://www.elastic.co/guide/en/elasticsearch/reference/2.4/mapping-all-field.html), so this query has higher relevance for the "shortest" json containing the word space as a value of one of its fields.




 
# more to come?  

Explore using Sirenjoin to perform joins https://github.com/sirensolutions/siren-join


