import os, sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from elastic import query
from flask import Flask
from flask_cors import CORS,cross_origin
from flask import request
import json

FULL_FIELDS = ["title","description","content"]

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"/search": {"origins": "*"}})
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/search',methods=['POST'])
    @cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
    def getData():
        key = request.form.get('key')
        fields = request.form.get('field').split(",")

        if(fields[0] == ""):
            fields = FULL_FIELDS

        if (key.startswith("\"") and key.endswith("\"")):
            if ("*" in key):
                return json.dumps(query.match_phrase_prefix(fields, key))
            else:
                return json.dumps(query.matchMultifield(fields, key.strip('"')))

        elif(("AND" in key) or ("OR" in key) or ("NOT" in key) or("*" in key)):
            key=key.replace("OR", '|')
            key=key.replace("AND", '+')
            key=key.replace("NOT ", '-')
            return json.dumps(query.queryString(fields,key))

        else:
            return json.dumps(query.searchField(fields,key))

    @app.route('/suggest',methods=['POST'])
    def getSuggest():
        key = request.form.get('key')
        return json.dumps(query.querySuggest(key))


    return app

if __name__ == "__main__" :
    create_app().run(host="localhost",port=5000,debug=True)