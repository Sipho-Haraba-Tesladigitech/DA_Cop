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

app = flask.Flask(__name__)   #Initialize the creation of the flask web app
api = Api(app) #Wrap the app in an api to expose only the relevant functionality

class URLAPI(Resource):  #Inherit the CRUD operations from the Resource class
    def get(self):   #only create the get operation
        try:
            url = request.args.get('url')
            if url is not None:
                # perform your logic here
                res = detection(url)
                print(url, res)
                return {
                    "url": url,
                    "results": res
                }
            else:
                return {"results": "Error: URL parameter is missing"}, 400
        except Exception as e:
            return {"results": f"Error: {e}"}

        # parser = reqparse.RequestParser()   #Used to get the parameters from the url
        # parser.add_argument('url', type=str)  #Set the name of the parameters and their data type, to avoid reading it as code
        # # arguments = parser.parse_args() #Store the arguments/parameters
        # print(parser)
        # res = "Not correct"#detection(arguments['url']) #Pass the parameters to detection and get the label
        # # print(arguments['url'], res)
        # return res   #Return the classification label to the end user

api.add_resource(URLAPI, '/url', endpoint='url')     #Expose the api endpoint


print("Server Started, Listening for upcoming connections")
app.run(host='0.0.0.0')   #This will automatically detect the ip address where we hosted our api
