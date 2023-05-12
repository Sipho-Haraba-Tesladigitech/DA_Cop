# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 10:59:11 2022

@author: Tshegofatso Mohlala


The api endpoint which is exposed to the end user
"""

import flask
from flask_restful import Resource, Api, reqparse
from flask import request
from detector import detection
import pandas as pd

app = flask.Flask(__name__)   #Initialize the creation of the flask web app
df = pd.DataFrame({
                    "url": [],
                    "results": []
                })

class URLAPI(Resource):  #Inherit the CRUD operations from the Resource class
    def get(self):   #only create the get operation
        try:
            url = request.args.get('url')
            if url is not None:
                # perform your logic here
                res = detection(url)
                print(url, res)
                response = {
                    "url": url,
                    "results": res
                }
                df.loc[len(df)] = response
                f = open("Tested Urls.csv", "a")
                df.to_csv(f, ",")
                f.close()

                return response
            else:
                return {"results": "Error: URL parameter is missing"}, 400
        except Exception as e:
            return {"url": f"Error: {e}", "results": "good"}


api = Api(app) #Wrap the app in an api to expose only the relevant functionality


class TestedURLApi(Resource):  #Inherit the CRUD operations from the Resource class
    def get(self):
        with open("Tested Urls.csv", "r") as f:
            response = ""
            for line in f.readlines():
                response += line

            return response


api.add_resource(URLAPI, '/url', endpoint='url')     #Expose the api endpoint
api.add_resource(TestedURLApi, '/Tested_Urls.csv')


print("Server Started, Listening for upcoming connections")
app.run(host='0.0.0.0')   #This will automatically detect the ip address where we hosted our api
