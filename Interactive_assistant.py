#!/usr/bin/env python
# coding: utf-8

"""
    Interactive Assistant Service - From scratch
    ============================================
    Voice Assistant Prototype:
        Webservice bot that interacts with user in front
        of the screen.
    Server side

    Note: 
    Structure:
        interactive_assistant.py
    _copyright_ = 'Copyright (c) 2019 J.W. - Everis', 
    _license_ = GNU General Public License
"""

# Load libraries
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_assistant import Assistant, ask, tell

import random
import time
import win32com.client as wincl
import win32api

app = Flask(__name__)
api = Api(app)

session_active = True
class ShowroomAssistant(Resource):
    def __init__(self):
        """ Initialize some common phrases and Microsoft Voice Api """
        self.sentiment = ['happiness', 'surprise', 'sadness', 'anger', 'disgust', 'fear']
        self.congrats = ["Muy bien! excelente trabajo.", "¡Excelente!", "¡Bien hecho!"]
        self.again = ["A ver, inténtalo nuevamente", "Vamos a intentarlo de nuevo con otra expresión"]

        import pythoncom
        pythoncom.CoInitialize()
        self.speak = wincl.Dispatch("SAPI.SpVoice")

    def get(self):
        return {'Default response': 'Use POST method'}
    
    def post(self):
        response = ""
        if request.headers['Content-Type'] == 'application/json; charset=UTF-8':
            req = dict(request.json)
            action = req['action']

            if action == 'input.welcome':
                print("<input.welcome>")
                name = req['name']

                msg = 'Hola ' + name + '!'
                print(msg)
                self.speak.Speak(msg)

                msg = "Te presentamos un sistema que implementa diversos modelos de inteligencia artificial."
                print(msg)
                self.speak.Speak(msg)

                msg = "Para mostrarte cómo funcionan estos modelos, hagamos algunas pruebas o retos."
                print(msg)
                self.speak.Speak(msg)

                response = { "session":"active", "reto": "", "detected":"Yes", "state":"welcome"}

                reply = {
                    "fulfillmentText": response,
                }

                return jsonify(reply)  

            if action == 'input.challenge':
                print("<input.challenge>")

                reto = req['reto']

                listReto = req['listReto']
                remainingSent = sorted(set(self.sentiment) - set(listReto))

                if len(remainingSent) > 0:
                    #challenge = random.choice(self.sentiment)
                    challenge = random.choice(remainingSent)
                    
                    if challenge == "happiness":
                        msg = "Muéstranos una sonrisa"
                        print(msg)
                        self.speak.Speak(msg)
                        response = { "session":"active", "reto": challenge, "detected":"Yes", "state":"challenge"}
                    
                    if challenge == "surprise":
                        msg = "Danos tu mejor cara de asombro."
                        print(msg)
                        self.speak.Speak(msg)
                        response = { "session":"active", "reto": challenge, "detected":"Yes", "state":"challenge"}
                    
                    if challenge == "sadness":
                        msg = "¿Qué tal una cara de tristeza?"
                        print(msg)
                        self.speak.Speak(msg)
                        response = { "session":"active", "reto": challenge, "detected":"Yes", "state":"challenge"}
                    
                    if challenge == "anger":
                        msg = "¿Cuál es tu cara de enojo?"
                        print(msg)
                        self.speak.Speak(msg)
                        response = { "session":"active", "reto": challenge, "detected":"Yes", "state":"challenge"}
                    
                    if challenge == "disgust":
                        msg = "¿Cómo es tu cara de desagrado?"
                        print(msg)
                        self.speak.Speak(msg)
                        response = { "session":"active", "reto": challenge, "detected":"Yes", "state":"challenge"}
                    
                    if challenge == "fear":
                        msg = "¿Muéstranos una cara de miedo?"
                        print(msg)
                        self.speak.Speak(msg)
                        response = { "session":"active", "reto": challenge, "detected":"Yes", "state":"challenge"}
                else: 
                    msg = "Gracias por participar" 
                    print(msg)
                    self.speak.Speak(msg)
                    response = {"session":"end", "reto": "ninguno", "detected":"No", "state":"terminate"}
                
                reply = {
                    "fulfillmentText": response,
                }

                return jsonify(reply)
            
            if action == 'input.feedback':
                print("<input.feedback>")
                score = req['score']
                reto = req['reto']

                if score == "positive":
                    msg = random.choice(self.congrats)
                    print(msg)
                    self.speak.Speak(msg)

                    repeat = int(req['repeat'])
                    if repeat <= 3:
                        if repeat == 1:
                            msg = "Por eso te has ganado " + str(repeat) + " punto en tu monedero virtual"
                            print(msg)
                            self.speak.Speak(msg)
                        else:
                            msg = "Por eso te has ganado " + str(repeat) + " puntos en tu monedero virtual"
                            print(msg)
                            self.speak.Speak(msg)
                        
                        if repeat == 3:
                            msg = "Muchas gracias por visitarnos"
                            print(msg)
                            self.speak.Speak(msg)
                            response = {'session':'end', "reto": "ninguno", "detected":"No", "state":"terminate"}
                        else:
                            response = {"session":"active", "reto": "", "detected":"Yes", "state":"welcome"}

                else:
                    fail = int(req['fail'])

                    if fail <= 4:
                        msg = random.choice(self.again)
                        print(msg)
                        self.speak.Speak(msg)

                        response = {"session":"active", "reto": reto, "detected":"Yes", "state":"welcome"}
                    else:
                        msg = "Empecemos de nuevo"
                        print(msg)
                        self.speak.Speak(msg)
                        response = {"session":"end", "reto": "ninguno", "detected":"No", "state":"terminate"}
                   
                reply = { "fulfillmentText": response, }

                return jsonify(reply)
            
            if action == "input.terminate":
                print("<input.terminate>")
                msg = "** Persona abandonó el juego"
                print(msg)
                response = {'session':'end', "reto": "ninguno", "detected":"No", "state":"terminate"}

                reply = { "fulfillmentText": response, }

                return jsonify(reply)

        else:
            return jsonify({"Message": "Invalid post request",})

api.add_resource(ShowroomAssistant, '/test')


if __name__ == "__main__":
    app.run(debug=True)
