import requests

BASE_URL = 'http://localhost:3100/'  # -> Your URL
API_KEY = 'YOUR-METABASE-API-TOKEN'
IMPORT_NAME = 'IMPORT_210227_MARYLAND'  # -> Import Name for the Queries

# --- CREATE COLLECTION CODE ---
collection_data = {
  "name": "Python Made Maryland Import",
  "color": "#ff0000"
}

response_collection = requests.post(f'{BASE_URL}api/collection', json=collection_data,
                                    headers={"X-Metabase-Session": API_KEY})
# Extract the id:
collection_id = response_collection.json()["id"]

if response_collection.status_code == 200:
  print("Collection Created Succesfully")
    
else:
  print(f"Failed to create collection. Status code: {response_collection.status_code}")
    

# --- CREATE DASHBOARD CODE ---
dashboard_data = {
  "name": "Python Made Dashboard Import Maryland",
  "collection_id": collection_id
}
response_dashboard = requests.post(f'{BASE_URL}api/dashboard', json=dashboard_data,
                                   headers={"X-Metabase-Session": API_KEY})
dashboard_id = response_dashboard.json()["id"]

if response_dashboard.status_code == 200:
  print("Dashboard Created Succesfully")
else:
  print(f"Failed to create collection. Status code: {response_collection.status_code}")
    
    
# === CREATING CARDS CODE ===

# --- IMPORT MARYLAND MAP ---
map_query_data = {
  "database": 2,  # Replace with the correct database ID
  "type": "native",  
  "native": {
    "query": f"SELECT dl.state, COUNT(*) AS COUNT\nFROM doctor d\nJOIN hospital h ON d.HOSPITAL_ID = h.HOSPITAL_ID\nJOIN doctor_location dl ON d.doctor_id = dl.doctor_id AND h.HOSPITAL_UUID = dl.group_id\nJOIN authz_doctors_labels adl ON d.doctor_uuid = adl.doctor_uuid\nJOIN authz_labels al ON al.uuid = adl.label_uuid\nWHERE al.name = ''{IMPORT_NAME}''\nGROUP BY state;"
  }
}


map_card_data = {
  "collection_id": collection_id,
  "dashboard_id": dashboard_id,  
  "name": "Map from Providers 1",
  "dataset_query": map_query_data,
  "display": "map",  
  "visualization_settings": {
    "type": "map",
    "map_type": "region",
    "map_options": {
      "map_type": "region",
      "region_map": "us_states",
      "region_column": "state",
      "value_column": "count"
    },
    "map.region": "us_states"
  }
}

response_map_card = requests.post(f'{BASE_URL}api/card', json=map_card_data,
                                  headers={"X-Metabase-Session": API_KEY})
map_card_id = response_map_card.json()['id']

if response_map_card.status_code == 200:
  print("Import Maryland Map Card Created Successfully")
else:
  print(f"Failed to create Import Maryland Map Card. Status code: {response_map_card.status_code}")
    

# --- # doctors ---
ndoctors_query_data = {  
  "database": 2,  
  "type": "native",  
  "native": {
    "query": f"-- # doctors\nselect count(*) from doctor d\njoin authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\njoin authz_labels al on al.uuid = adl.label_uuid\nwhere al.name = ''{IMPORT_NAME}''"
  }
}

ndoctors_card_data = {  
  "collection_id": collection_id,
  "dashboard_id": dashboard_id,  
  "name": "# doctors",  
  "dataset_query": ndoctors_query_data, 
  "display": "scalar", 
  "visualization_settings": {}  
}

response_ndoctors_card = requests.post(f'{BASE_URL}api/card', json=ndoctors_card_data,
                                       headers={"X-Metabase-Session": API_KEY}) 
ndoctors_card_id = response_ndoctors_card.json()['id']  

if response_ndoctors_card.status_code == 200: 
  print("# doctors Card Created Successfully")
else:
  print(f"Failed to create # doctors Card. Status code: {response_ndoctors_card.status_code}")


# --- # locations ---
nlocations_query_data = {  
  "database": 2,  
  "type": "native",  
  "native": {
    "query": f"-- # locations imported\nselect count(dl.LOCATION_ID) from doctor d\njoin hospital h on d.HOSPITAL_ID = h.HOSPITAL_ID\njoin doctor_location dl on d.doctor_id = dl.doctor_id and h.HOSPITAL_UUID = dl.group_id\njoin authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\njoin authz_labels al on al.uuid = adl.label_uuid\nwhere al.name = ''{IMPORT_NAME}'' "
  }
}

nlocations_card_data = { 
  "collection_id": collection_id,
  "dashboard_id": dashboard_id,  
  "name": "# locations", 
  "dataset_query": nlocations_query_data, 
  "display": "scalar", 
  "visualization_settings": {}  
}

response_nlocations_card = requests.post(f'{BASE_URL}api/card', json=nlocations_card_data,
                                         headers={"X-Metabase-Session": API_KEY}) 
nlocations_card_id = response_nlocations_card.json()['id']  

if response_nlocations_card.status_code == 200:  
  print("# locations Card Created Successfully")
else:
  print(f"Failed to create # locations Card. Status code: {response_nlocations_card.status_code}")
    
    
# --- doctors imported table ---
docimported_query_data = {  
  "database": 2,  
  "type": "native",  
  "native": { 
    "query": f"select\nd.doctor_id 'Doctor ID',\nd.npi 'NPI',\nd.first_name 'First Name',\nd.last_name 'Last Name',\nd.email 'E-mail',\nh.name 'Network',\nd2.credentials->>\"$.suffix\" 'Credentials',\ndl.ADDRESS_LINE_1 'Address Line 1',\ndl.CITY 'City',\ndl.STATE 'State',\ndl.ZIP_CODE 'Zip Code'\nfrom doctor d\njoin (select dx.doctor_id, convert(dx.preference, json) credentials from doctor dx) d2 on d.DOCTOR_ID = d2.DOCTOR_ID\nleft join doctor_padmins dpa on d.doctor_id = dpa.doc_id\nleft join hospital h on d.HOSPITAL_ID = h.HOSPITAL_ID\nleft join doctor_location dl on d.DOCTOR_ID = dl.DOCTOR_ID\nleft join authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\nleft join authz_labels al on al.uuid = adl.label_uuid\nwhere al.name = ''{IMPORT_NAME}'' "
  }
}

docimported_card_data = {
  "collection_id": collection_id,
  "dashboard_id": dashboard_id,  
  "name": "Doctors Imported",  
  "dataset_query": docimported_query_data,  
  "display": "table",  
  "visualization_settings": {} 
}

response_docimported_card = requests.post(f'{BASE_URL}api/card', json=docimported_card_data,
                                          headers={"X-Metabase-Session": API_KEY}) 
docimported_card_id = response_docimported_card.json()['id']  

if response_docimported_card.status_code == 200: 
  print("Doctors Imported Table Card Created Successfully")
else:
  print(f"Failed to create Doctors Imported Table Card. Status code: {response_docimported_card.status_code}")
    

# --- Insurance Distribution ---
insdist_query_data = {  
  "database": 2,  
  "type": "native",  
  "native": { 
    "query": f"-- Insurance distribution\nselect ip.NAME 'Plan Name', count(di.doctor_id) Counted from doctor d\njoin doctor_insurance di on d.doctor_id = di.doctor_id\njoin insurance_plans ip on di.PLAN_ID = ip.PLAN_ID\njoin authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\njoin authz_labels al on al.uuid = adl.label_uuid\nwhere al.name = '''{IMPORT_NAME}''\nand di.PLAN_ID != 117\ngroup by ip.NAME "
  }
}

insdist_card_data = {
  "collection_id": collection_id,
  "dashboard_id": dashboard_id,  
  "name": "Insurance Distribution",  
  "dataset_query": insdist_query_data,  
  "display": "table",  
  "visualization_settings": {
    "table.pivot_column": "Counted",
    "table.cell_column": "Plan Name"
  }  
}

response_insdist_card = requests.post(f'{BASE_URL}api/card', json=insdist_card_data,
                                      headers={"X-Metabase-Session": API_KEY})  
insdist_card_id = response_insdist_card.json()['id']  

if response_insdist_card.status_code == 200:  
  print("Insurance Distribution Table Card Created Successfully")
else:
  print(f"Failed to create Insurance Distribution Table Card. Status code: {response_insdist_card.status_code}")
    

# --- Insurance Summary ---
inssum_query_data = {  
  "database": 2,  
  "type": "native",  
  "native": {  
    "query": f"-- INSURANCE SUMMARIZE\nselect 'Doctors with Self Pay' Description, count(distinct di.doctor_id) Count from doctor d\njoin doctor_insurance di on d.doctor_id = di.doctor_id\njoin authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\njoin authz_labels al on al.uuid = adl.label_uuid\nwhere al.name = '''{IMPORT_NAME}''\nand di.PLAN_ID = 117\nunion\nselect 'Doctors with Insurances', count(distinct di.doctor_id) Count from doctor d\njoin doctor_insurance di on d.doctor_id = di.doctor_id\njoin authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\njoin authz_labels al on al.uuid = adl.label_uuid\nwhere al.name = '''{IMPORT_NAME}''\nand di.PLAN_ID != 117 "
  }
}

inssum_card_data = {
  "collection_id": collection_id,
  "dashboard_id": dashboard_id,  
  "name": "Insurance Summary",  
  "dataset_query": inssum_query_data, 
  "display": "table", 
  "visualization_settings": {
    "table.pivot_column": "Description",
    "table.cell_column": "Count"
  }  
}

response_inssum_card = requests.post(f'{BASE_URL}api/card', json=inssum_card_data,
                                     headers={"X-Metabase-Session": API_KEY})  
inssum_card_id = response_inssum_card.json()['id']  

if response_inssum_card.status_code == 200:  
  print("Insurance Summary Table Card Created Successfully")
else:
  print(f"Failed to create Insurance Summary Table Card. Status code: {response_inssum_card.status_code}")
    
    
# --- Specialty Distribution (specdist) ---
specdist_query_data = {
  "database": 2,  # Replace with the correct database ID
  "type": "native",  
  "native": {  
    "query": f"-- SPECIALTY DISTRIBUTION\nselect s.name Specialty, c.name Subspecialty, count(ds.doctor_id) Count from doctor d\nleft join doctor_location dl on d.doctor_id = dl.doctor_id\nleft join specialties ds on d.doctor_id = ds.doctor_id\nleft join specialty s on ds.SPECIALTY_ID = s.SPECIALTY_ID\nleft join cpt_loc cl on dl.location_id = cl.loc_id\nleft join cpts c on cl.cpt_id = c.id\nleft join authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\nleft join authz_labels al on al.uuid = adl.label_uuid\nwhere al.name = '''{IMPORT_NAME}''\ngroup by s.name, c.name\norder by Count desc "
  }
}

specdist_card_data = {
  "collection_id": collection_id,
  "dashboard_id": dashboard_id,  
  "name": "Specialty Distribution",  
  "dataset_query": specdist_query_data, 
  "display": "table",  
  "visualization_settings": {
    "table.pivot_column": "Subspecialty",
    "table.cell_column": "Count"
  }  
}

response_specdist_card = requests.post(f'{BASE_URL}api/card', json=specdist_card_data,
                                       headers={"X-Metabase-Session": API_KEY})  
specdist_card_id = response_specdist_card.json()['id']  

if response_specdist_card.status_code == 200:  
  print("Specialty Distribution Table Card Created Successfully")
else:
  print(f"Failed to create Specialty Distribution Table Card. Status code: {response_specdist_card.status_code}")
    
    
# --- Specialty Summary (specsum) ---
specsum_query_data = { 
  "database": 2, 
  "type": "native",  
  "native": { 
    "query": f"-- SPECIALTY SUMMARY\nselect 'Doctors with specialties' Description, count(distinct s.doctor_id) Count from doctor d\njoin specialties s on d.doctor_id = s.doctor_id\njoin authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\njoin authz_labels al on al.uuid = adl.label_uuid\nwhere al.name = '''{IMPORT_NAME}''\nunion\nselect 'Doctors without specialties', count(distinct d.doctor_id) Count from doctor d\nleft join specialties s on d.doctor_id = s.doctor_id\nleft join authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\nleft join authz_labels al on al.uuid = adl.label_uuid\nwhere al.name = '''{IMPORT_NAME}''\nand s.doctor_id is null\nunion\nselect 'Total', sum(x.Count) from (\n    select 'Doctors with specialties' Description, count(distinct s.doctor_id) Count from doctor d\n    join specialties s on d.doctor_id = s.doctor_id\n    join authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\n    join authz_labels al on al.uuid = adl.label_uuid\n    where al.name = '''{IMPORT_NAME}''\n    union\n    select 'Doctors without specialties', count(distinct d.doctor_id) Count from doctor d\n    left join specialties s on d.doctor_id = s.doctor_id\n    left join authz_doctors_labels adl on d.doctor_uuid = adl.doctor_uuid\n    left join authz_labels al on al.uuid = adl.label_uuid\n    where al.name = '''{IMPORT_NAME}''\n    and s.doctor_id is null\n) x "
  }
}

specsum_card_data = {
  "collection_id": collection_id,
  "dashboard_id": dashboard_id,  
  "name": "Specialty Summary",  
  "dataset_query": specsum_query_data,  
  "display": "table",
  "visualization_settings": {
    "table.pivot_column": "Count",
    "table.cell_column": "Description"
  }  
}

response_specsum_card = requests.post(f'{BASE_URL}api/card', json=specsum_card_data,
                                      headers={"X-Metabase-Session": API_KEY}) 
specsum_card_id = response_specsum_card.json()['id']  

if response_specsum_card.status_code == 200:  
  print("Specialty Summary Table Card Created Successfully")
else:
  print(f"Failed to create Specialty Summary Table Card. Status code: {response_specsum_card.status_code}")


# === UPLOADING THE CARD INSIDE THE DASHBOARD ===
cards_inside_dashboard = {
  "cards": [
    {  # Doctors Imported Table
      "id": -1,
      "card_id": docimported_card_id,
      "row": 0,
      "col": 0,
      "size_x": 24,
      "size_y": 9,
      "series": [],
      "visualization_settings": {},
      "parameter_mappings": []
    },
    {  # # doctors
      "id": 1,
      "card_id": ndoctors_card_id,
      "row": 9,
      "col":0,
      "size_x":4,
      "size_y":4,
      "series":[],
      "visualization_settings":{},
      "parameter_mappings":[]
    },
    {
      "id": 2,
      "card_id": nlocations_card_id,
      "row":9,
      "col":4,
      "size_x":4,
      "size_y":4,
      "series":[],
      "visualization_settings":{},
      "parameter_mappings":[]
    },
    {  # insurance distribution
      "id": 3,
      "card_id": insdist_card_id,
      "row":9,
      "col":8,
      "size_x":5,
      "size_y":9,
      "series":[],
      "visualization_settings":{},
      "parameter_mappings":[]
    },
    {  # insurance summary
      "id":4,
      "card_id": inssum_card_id,
      "row":13,
      "col": 0,
      "size_x":8,
      "size_y":3,
      "series":[],
      "visualization_settings":{},
      "parameter_mappings":[]
    },
    {  # specialty distribution
      "id": 5,
      "card_id": specdist_card_id,
      "row": 9,
      "col": 13,
      "size_x": 11,
      "size_y": 8,
      "series": [],
      "visualization_settings": {},
      "parameter_mappings": []
    },
    {  # specialty summary
      "id": 6,
      "card_id": specsum_card_id,
      "row":17,
      "col":13,
      "size_x":11,
      "size_y":4,
      "series":[],
      "visualization_settings":{},
      "parameter_mappings":[]
    },
    {  # IMPORT MARYLAND MAP
      "id": -2,
      "card_id": map_card_id,
      "row": 21,
      "col": 0,
      "size_x": 24,
      "size_y": 8,
      "series": [],
      "visualization_settings": {},
      "parameter_mappings": []
    }
  ]
}

response_card_order = requests.put(f'{BASE_URL}api/dashboard/{dashboard_id}/cards', json=cards_inside_dashboard,
                                   headers={"X-Metabase-Session": API_KEY})

if response_card_order.status_code == 200:
  print("All Cards Were Uploaded to the Dashboard Successfully")
else:
  print(f"Failed to associate card with the dashboard. Status code: {response_card_order.status_code}")
