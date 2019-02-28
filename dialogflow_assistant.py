from flask import Flask, request, jsonify
from flask_assistant import Assistant, ask, tell

from flask_restful import Resource, Api

import logging 
logging.getLogger('flask_restful').setLevel(logging.DEBUG)

app = Flask(__name__)
api = Api(app)

class ShowroomAssistant(Resource):
    def get(self):
        return {'Default response': 'Use POST method'}
    
    def post(self):
        #data = request.get_json(silent=True)
        response = ""
        if request.headers['Content-Type'] == 'application/json; charset=UTF-8':
            req = dict(request.json)
            action = req.get('queryResult').get('action')
            
            print("Action:{} \n".format(action))
            print("Req parsed:\n",req)

            if action == "input.welcome":
                response = 'Hola! Cuál es tu nombre?'

                reply = {
                    "fulfillmentText": response,
                }

                return jsonify(reply)

            if action == "input.name":
                name = req['queryResult']['parameters']['given-name'] #"WebHook" #req.get()
                print("name: ", name)

                response = name + ', Te gustaría participar en un reto?'
                reply = { "fulfillmentText": response, }

                return jsonify(reply)

        else:
            return jsonify({"fulfillmentText": "No te he entendido, puedes volver a repetir por favor?",})

api.add_resource(ShowroomAssistant, '/test')


if __name__ == "__main__":
    app.run(debug=True)
