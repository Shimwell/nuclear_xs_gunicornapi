
from flask import Flask, jsonify, make_response, request
import json
from bson import json_util
from bson.objectid import ObjectId
from data_formatting_tools import *
from database_tools import *
from flask_cors import CORS, cross_origin

application = Flask(__name__)
CORS(application)

VERSION = '0.1'


@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# collection, client, db = connect_to_database()
# collection, client, db = connect_to_docker_database()
collection, client, db = connect_to_atlas_database()

basepath = os.path.dirname(os.path.realpath(__file__))

print('basepath',basepath)

meta_data_fields = ["Library", "MT number / reaction products", "Mass number", "Neutron number", "Proton number / element"]

axis_option_fields = ["cross section", "energy"]

axis_option_fields_dict = {}
for i in axis_option_fields:
    axis_option_fields_dict[i] = 0


def get_entries_in_field(collection, field, query=None):
    if query != {}:
      result = collection.distinct(field,query)
    else:
      result = collection.distinct(field)
    return result

@application.route('/test' ,methods=['GET','POST'])
@cross_origin()
def test():
    return 'working'

@application.route('/get_matching_entrys_and_distinct_values_for_fields' ,methods=['GET','POST'])
@cross_origin()
def get_matching_entrys_and_distinct_values_for_fields():
    query_string = request.args.get('query')
    limit = request.args.get('limit', default=30, type=int)

    query = json.loads(query_string)

    print('query = ',query)

    results = collection.find(query,axis_option_fields_dict).limit(limit)

    results_str = json_util.dumps(results)
    results_json = json.loads(results_str)

    for res in results_json: 
        res['id']=res['_id']['$oid'] 
        res.pop('_id')

    results_json2={}
    results_json2['search_results'] = results_json

    fields_and_available_options = []
    for field in meta_data_fields:

        available_options = get_entries_in_field(collection, field, query=query)
        fields_and_available_options.append({
                                             'field':field,
                                             'available_options':available_options
                                             })

    results_json2['dropdown_options'] = fields_and_available_options

    return json_util.dumps(results_json2)


@application.route('/get_matching_entry' ,methods=['GET','POST'])
@cross_origin()
def get_matching_entry():
    query_string = request.args.get('query')

    print('query_string',query_string)

    query = json.loads(query_string)
    if list(query.keys())[0] == "id":

        query = {"_id": ObjectId(list(query.values())[0])}

    print('query = ',query)
    results = collection.find_one(query)

    results_str = json_util.dumps(results)
    results_json = json.loads(results_str)

    for res in [results_json]: 
        res['id']=res['_id']['$oid'] 
        res.pop('_id')
    results_str = json_util.dumps(results_json)
    return results_str



# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5001)


# context = ('cloudflare.crt', 'private_key.pem')

if __name__ == '__main__':
    application.run(
        #debug=True,
        host='0.0.0.0',
        port=8080,
        # ssl_context=context
    )
