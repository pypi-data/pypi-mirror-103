# wikipeople


Search for concept ID's given a string
```py
>>> from wikipeople import wikipeople as wp
>>> wp.search_wikidata('Andy Murray')
'Q10125'
```


Basic info
```py
>>> wp.get_property(wp.search_wikidata('Andy Murray'), 'P21')
('Q6581097', 'male')
```


Get someone's date of birth
```py
>>> wp.get_date_of_birth(wp.search_wikidata('Andy Murray'))
'+1987-05-15'
```


Get information about someone's profession
```py
>>> wp.get_profession_hierarchy(wp.search_wikidata('Andy Murray'))
['tennis player', 'athlete', 'sportsperson']
```


Get someone's Country of birth
```py
>>> wp.get_country(wp.get_property(wp.search_wikidata('Andy Murray'), 'P19')[0])
('Q145', 'United Kingdom')
```
