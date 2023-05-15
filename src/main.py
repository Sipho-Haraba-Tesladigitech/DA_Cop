# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 10:59:11 2022

@author: Tshegofatso Mohlala


The api endpoint which is exposed to the end user
"""
import json
import subprocess

import flask
from flask_restful import Resource, Api, reqparse
from flask import Response, request
from detector import detection

# Initialize the creation of the flask web app
app = flask.Flask(__name__)


# Inherit the CRUD operations from the Resource class
class URLApi(Resource):
    # only create the get operation
    def get(self):
        try:
            url = request.args.get('url')
            if url is not None:
                output = subprocess.run(["./asserts/extractor.exe",
                                         '-r', url], stdout=subprocess.PIPE).stdout.decode('utf-8')
                if not output.startswith("Error"):
                    feat_values = eval(output)
                    res = detection(feat_values)
                    print(url, res)
                    response = {
                        "url": url,
                        "results": res
                    }

                    f = open("./asserts/Tested Urls.csv", "a")
                    f.write(f"\n{url},{res}")
                    f.close()
                    return response
                elif output.endswith("connect\r\n"):
                    response = {
                        "url": url,
                        "results": "good"
                    }
                    return response
                else:
                    return {"results": f"{output}"}

            else:
                return {"results": "Error: URL parameter is missing"}, 400
        except Exception as e:
            return {"results": f"Error: {e}"}, 404


# Inherit the CRUD operations from the Resource class
class TestedURLApi(Resource):
    def get(self):
        with open("./asserts/Tested Urls.csv", "r") as f:
            response = ""
            for line in f.readlines():
                response += line

            headers = {
                'Content-Type': 'text/plain; charset=utf-8'
            }

            return Response(response.encode("utf-8"), headers=headers)


# Wrap the app in an api to expose only the relevant functionality
api = Api(app)
# Expose the api endpoint
api.add_resource(URLApi, '/url', endpoint='url')
api.add_resource(TestedURLApi, '/Tested_Urls.csv', '/tested_urls.csv')


print("Server Started, Listening for upcoming connections")
# This will automatically detect the ip address where we hosted our api and listen to requests from any host (0.0.0.0)
app.run(host='0.0.0.0')
