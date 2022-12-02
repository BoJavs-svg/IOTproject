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
        menu=0
        cred = credentials.Certificate('credentials.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        pred=[[-1,-1]]
        while menu!=5:
            menu=(input("1.Caso de prueba 0 0\n2.Caso de prueba 0 1\n3.Caso de prueba 1 0\n4.Caso de prueba 1 1\n5.Salir\n"))
            if(menu=="1"):
                pred[0][0]=0
                pred[0][1]=0
            elif(menu=="2"):
                pred[0][0]=0
                pred[0][1]=1
            elif(menu=="3"):
                pred[0][0]=1
                pred[0][1]=0
            elif(menu=="4"):
                pred[0][0]=1
                pred[0][1]=1
            elif(menu=="5"):
                return
            else:
                print("Opcion incorrecta")
            
            doc_ref = db.collection(u'aprediccion').document("LastAccess")
            doc_ref.set({
                u'accesso':"Casodeprueba"
            })
            doc_ref = db.collection(u'aprediccion').document("Casodeprueba")
            doc_ref.set({
                u'flip':"1",
                u'coffee': str(pred[0][0]),
                u'courtain': str(pred[0][1]),
                u'temperatura': "0",
                u'luz': "0"
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
    
if __name__=="__main__":
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()