"""
    @author: svanstroud
    Get information about people using the wikidata API
"""

import requests 



def search_wikidata(string):
  """
  Query the Wikidata API using the wbsearchentities function.
  Return the concept ID of the first search result.
  """

  query = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&search='
  query += string
  query += '&language=en&format=json'

  res = requests.get(query).json()

  if len(res['search']) == 0:
    raise Exception('Wikidata search failed.')

  return res['search'][0]['id']


def get_concept_label(concept_id):
  """
  Given a concept ID, get the natural language label.
  """
  query = 'https://www.wikidata.org/w/api.php?action=wbgetentities&ids='
  query += concept_id
  query += '&format=json&languages=en&props=labels'

  res = requests.get(query).json()

  return res['entities'][concept_id]['labels']['en']['value']


def get_property(concept_id, property_id):
  """
  Properties:
   - P569 = Date of birth
   - P106 = Career
   - Place of birth (P19)
   - Country of citizenship (P27)
   - Sex or Gender (P21)
  Get the concept ID for a property associated to an input concept.
  """

  query = 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity='
  query += concept_id
  query += '&property='+property_id+'&language=en&format=json'

  res = requests.get(query).json()

  try:
    for prop in res['claims'][property_id]:
      concept_result = prop['mainsnak']['datavalue']['value']['id']
      break # just get the first result for now
    
    concept_label = get_concept_label(concept_result)
  except: 
    concept_result = prop['mainsnak']['datavalue']['value']['id']
    concept_label = 'NA'
  
  return concept_result, concept_label


def get_date_of_birth(concept_id):
  """
  Properties:
   - P569 = Date of birth
  Get a person's DOB given their concept. This gets it's own function
  as the structure of the result is slightly different.
  """

  property_id = 'P569'

  query = 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity='
  query += concept_id
  query += '&property='+property_id+'&language=en&format=json'

  res = requests.get(query).json()

  for prop in res['claims'][property_id]:
    concept_result = prop['mainsnak']['datavalue']['value']['time'].split('T')[0]
    break
  
  return concept_result



def get_parent_class(profession_concept_id):
  """
  Given a profession concept ID, find the parent profession.
  """

  property_id = 'P279' # "is subclass of"

  query = 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity='
  query += profession_concept_id
  query += '&property='+property_id+'&format=json'

  res = requests.get(query).json()

  for claim in res['claims'][property_id]:
    parent_concept = claim['mainsnak']['datavalue']['value']['id']
    break # just use the first result for now

  return parent_concept, get_concept_label(parent_concept)



def get_profession_hierarchy(castaway_concept_id):
  person_concept_id = 'Q215627' # we don't need to go further than this

  # get the persons profession
  concept_id, label = get_property(castaway_concept_id, 'P106')

  # store the first progression we get
  hierarchy = [label]

  # while we didn't reach the top
  while True:
    
    # get the parent profession of the current profession
    concept_id, label = get_parent_class(concept_id)
    
    # if the parent is the person conept, we are done
    if concept_id == person_concept_id:
      break

    # otherwise store this profession and go again
    hierarchy.append(label)

  return hierarchy


def get_country(place_concept_id):
  """
  Given a place concept ID, find the Country which this place is in.
  """

  property_id = 'P17' # "Country"

  query = 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity='
  query += place_concept_id
  query += '&property='+property_id+'&format=json'

  res = requests.get(query).json()

  for claim in res['claims'][property_id]:
    parent_concept = claim['mainsnak']['datavalue']['value']['id']
    break # just use the first result for now

  return parent_concept, get_concept_label(parent_concept)