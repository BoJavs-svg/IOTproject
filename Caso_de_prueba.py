import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

menu=int(input("1.Caso de prueba 0 0\n2.Caso de prueba 0 1\n3.Caso de prueba 1 0\n4.Caso de prueba 1 1\n5.Salir\n"))
cred = credentials.Certificate('IOT/credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
pred=[[0,0]]
while menu!=5:
    if(menu==1):
        pred[0][0]=0
        pred[0][1]=0
    elif(menu==2):
        pred[0][0]=0
        pred[0][1]=1
    elif(menu==3):
        pred[0][0]=1
        pred[0][1]=0
    elif(menu==4):
        pred[0][0]=1
        pred[0][1]=1
    else:
        print("Opcion incorrecta")
    if(menu!=5):   
        doc_ref = db.collection(u'prediccion').document("LastAccess")
        doc_ref.set({
            u'accesso':"Caso de prueba"
        })
        doc_ref = db.collection(u'prediccion').document("Caso de prueba")
        doc_ref.set({
            u'flip':"1",
            u'coffee': str(pred[0][0]),
            u'courtain': str(pred[0][1]),
            u'temperatura': "0",
            u'luz': "0"
        })
        print("Subido a firestore")   
