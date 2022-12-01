import pickle
import pandas as pd
import time
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        temp=-1
        luz=-1
        if "/temp" in self.path:
            temp=float(self.path.split("=")[1])
            luz=float(self.path.split("=")[3])
            print("temp = ")
            print(temp)
            print("luz = ")
            print(luz)
        now = time.strftime("%H:%M:%S")
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        if luz==-1 or temp==-1:
            print("")
        else:
            pred=predict(temp,luz,now)    
            #Subelo a firestore
            cred = credentials.Certificate('IOT/credentials.json')
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            #Crea un documento con el nombre de now y que tenga los datos de pred, temp y luz
            doc_ref = db.collection(u'prediccion').document("Day "+now)
            doc_ref.set({
                u'prediccion': pred,
                u'temperatura': temp,
                u'luz': luz
            })
            print("Subido a firestore")   
        
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