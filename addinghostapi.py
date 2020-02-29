from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import json
from mongoengine import *
import os



if 'VCAP_SERVICES' in os.environ:
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    # XXX: avoid hardcoding here
    mongo_srv = vcap_services['mongodb'][0]
    cred = mongo_srv['credentials']
    host = cred['hostname']
    user = cred['username']
    pw = cred['password']
    mongo_url = cred['uri']
else:
    host = "localhost"
    user = ""
    pw = ""
    mongo_url = "mongodb://localhost"


if 'VCAP_SERVICES' in os.environ:
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    # XXX: avoid hardcoding here
    mongo_srv = vcap_services['fs-storage'][0]
    cred = mongo_srv['volume_mounts'][0]
    container_dir = cred['container_dir']
    



app = Flask(__name__)
app.config["MONGO_URI"] = mongo_url
##"mongodb+srv://dbuser:dbuserpassword@cluster0-o5lsl.mongodb.net/runtimeapi?retryWrites=true&w=majority"
mongo = PyMongo(app)



@app.route("/dir", methods=['GET'])
def getdir():
	return container_dir


@app.route('/api/rthosts', methods=['POST'])
def add_runtimehost():
    rthostcollection = mongo.db.runtimehosts 
    rthosturl = request.json['runtimeurl']
    rthosturl_id = rthostcollection.insert({'runtimeurl' : rthosturl})
    new_runtimehost = rthostcollection.find_one({'_id' : rthosturl_id})

    rtoutput = {'runtimeurl' : new_runtimehost['runtimeurl']}
    return jsonify({'result' : rtoutput})



@app.route("/api/rthosts", methods=['GET'])
def getrthosts():
    rthostcollection = mongo.db.runtimehosts.find({}, {'_id': False})
    output = []
    for item in rthostcollection:
        output.append(item)
    return jsonify({'rthosts' : output})
####################################################################################
@app.route('/api/dthosts', methods=['POST'])
def add_dthost():
    dthostcollection = mongo.db.dthosts 
    dthosturl = request.json['designurl']
    dthosturl_id = dthostcollection.insert({'designurl' : dthosturl})
    new_dthost = dthostcollection.find_one({'_id' : dthosturl_id})

    dtoutput = {'runtimeurl' : new_dthost['designurl']}
    return jsonify({'result' : dtoutput})


@app.route("/api/dthosts", methods=['GET'])
def getdthosts():
    dthostcollection = mongo.db.dthosts.find({}, {'_id': False})
    output = []
    for item in dthostcollection:
        output.append(item)
    return jsonify({'dthosts' : output})

#####################################################################################
@app.route("/api/runtimeapihosts", methods=['GET'])
def getruntimeapihost():
    runtimeapi_collection = mongo.db.runtimeapidb.find({}, {'_id': False})
    output = []
    for item in runtimeapi_collection:
        output.append(item)
    return jsonify({'runtimeapihosts' : output})


@app.route('/api/runtimeapihosts', methods=['POST'])
def add_rtapihost():
    runtimeapi_collection = mongo.db.runtimeapidb 
    dccode = request.json['dccode']
    apiurl = request.json['apiurl']
    orgname = request.json['orgname']
    spacename = request.json['spacename']
    dtdomain = request.json['dtdomain']
    rtdomain = request.json['rtdomain']

    newruntimeapihost_id = runtimeapi_collection.insert({'apiurl' : apiurl,'dccode' : dccode,'orgname' : orgname, 'spacename': spacename, 'dtdomain':dtdomain, 'rtdomain':rtdomain})
    new_rtapihost = runtimeapi_collection.find_one({'_id' : newruntimeapihost_id})

    rtapioutput = {'apiurl' : new_rtapihost['apiurl'],'dccode' : new_rtapihost['dccode'], 'orgname' :new_rtapihost['orgname'],'spacename':new_rtapihost['spacename'],'dtdomain':new_rtapihost['dtdomain'],'rtdomain':new_rtapihost['rtdomain']}

    return jsonify({'result' : rtapioutput})

cf_port = os.getenv("PORT")

if __name__ == '__main__':
	if cf_port is None:
		app.run(host='0.0.0.0', port=5000, debug=True)
	else:
		app.run(host='0.0.0.0', port=int(cf_port), debug=True)
