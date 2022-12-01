import pickle
import pandas as pd
import sqlalchemy
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neural_network import MLPClassifier
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import declarative_base
import time
import random

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

Base =declarative_base()
class Entrada(Base):
    __tablename__ = 'entrada'
    id = Column(Integer, primary_key=True)
    temperatura = Column(Integer)
    hora = Column(Integer)
    luz = Column(Integer)
    coffee= Column(Integer)
    courtain=Column(Integer)
    def __repr__(self):
        return "<Entrada(temperatura='%s', hora='%s', luz='%s', coffee='%s', courtain='%s')>" % (self.temperatura, self.hora, self.luz, self.coffee, self.courtain)

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        temp=0
        luz=0
        if "/temp" in self.path:
            temp=float(self.path.split("=")[1])
            luz=float(self.path.split("=")[3])
            print("temp = ")
            print(temp)
            print("luz = ")
            print(luz)
        now = time.strftime("%H:%M:%S")
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        pred=predict(temp,luz,now)    
        self.do_POST(pred)
        
    def do_POST(self, prediction):
        coffee=prediction[0]
        courtain=prediction[1]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        self.wfile.write("Comfirm: {}".format(1).encode('utf-8'))
        self.wfile.write("Coffee: {}".format(coffee).encode('utf-8'))
        self.wfile.write("Courtain: {}".format(courtain).encode('utf-8'))
        
def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')
    
def predict(luz,temp,now):
    # Load the model from the file
    with open('model.pkl', 'rb') as file:
        pickle_model = pickle.load(file)
    # Use the loaded model to make predictions
    #Convertir la hora a minutos
    hora=now.split(":")[0]
    minuto=now.split(":")[1]
    hora=int(hora)*60
    minuto=int(minuto)
    hora=hora+minuto
    X_new = [[luz,temp,hora]]
    print(X_new)
    prediction = pickle_model.predict(X_new)
    print(prediction)
    return prediction

if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()