import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./flatmap-90f33-firebase-adminsdk-i2t5z-dbfe07f578.json")

app = firebase_admin.initialize_app(cred)
db = firestore.client()

def add_liked_to_database(userid, liked_info):
    doc_ref = db.collection('users').document(userid)
    doc = doc_ref.get()
    info_list = []

    if doc.exists:
        for key in doc.to_dict():
            info_list = doc.to_dict().get(key)
    else:
        data = {'liked_list' : []}
        doc_ref.set(data)

    # Добавьте новые данные в массив
    info_list.append(liked_info)

    # Обновите документ пользователя, включая новые данные
    doc_ref.update({'liked_flats': info_list})

    print("Succesfully added")
    return

def get_liked_from_database(userid):
    doc_ref = db.collection('users').document(userid)
    doc = doc_ref.get()

    flats = []
    for key in doc.to_dict():
        flats = doc.to_dict().get(key)

    return flats
