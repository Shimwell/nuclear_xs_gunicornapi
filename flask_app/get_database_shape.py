

import math
import time

from io import BytesIO, StringIO
import json
from bson import json_util
from bson.objectid import ObjectId
from data_formatting_tools import *
from database_tools import *
# from flask_cors import CORS, cross_origin
import pandas as pd
import re




 


collection, client, db = connect_to_database()
# collection, client, db = connect_to_docker_database()

all_database_fields = get_database_fields(collection)
print('all_database_fields',all_database_fields)

# # meta_data_fields = get_database_fields(collection, ignore_fields=['Time [sec]', 'Stroke', 'Extens', 'Load', 'Temp1', 'Temp2', 'Temp3'])
# # print(meta_data_fields)

meta_data_fields = find_all_fields_not_of_a_particular_types_in_database(collection,'list')
print('meta_data_fields',meta_data_fields)

axis_option_fields = find_all_fields_of_a_particular_types_in_database(collection,'list')
print('axis_option_fields',axis_option_fields)

# metadata_values=[]
metadata_fields_and_their_distinct_values={}
for entry in meta_data_fields:
    values = get_entries_in_field(collection,entry)
    # metadata_values.append(values)
    values.sort()#(key=natural_keys) 
    metadata_fields_and_their_distinct_values[entry]=values


meta_data_fields_and_distinct_entries = []
for field in meta_data_fields:
    print('meta_data_fields_and_distinct_entries', field)
    meta_data_fields_and_distinct_entries.append({'field':[field],'distinct_values':metadata_fields_and_their_distinct_values[field]})




with open('all_database_fields.json', 'w') as outfile:
    json.dump(all_database_fields, outfile)

with open('meta_data_fields.json', 'w') as outfile:
    json.dump(meta_data_fields, outfile)

with open('axis_option_fields.json', 'w') as outfile:
    json.dump(axis_option_fields, outfile)


with open('metadata_fields_and_their_distinct_values.json', 'w') as outfile:
    json.dump(meta_data_fields_and_distinct_entries, outfile)



with open('meta_data_fields_and_distinct_entries.json', 'w') as outfile:
    json.dump(meta_data_fields_and_distinct_entries, outfile)

