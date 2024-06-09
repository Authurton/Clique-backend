import firebase_admin
from firebase_admin import firestore

db = firestore.client()

def add_user_to_firestore(user_data):
    db.collection('users').add(user_data)

def get_users_from_firestore():
    users = db.collection('users').stream()
    return [user.to_dict() for user in users]

def update_user_in_firestore(user_id, updated_data):
    db.collection('users').document(user_id).update(updated_data)

def delete_user_from_firestore(user_id):
    db.collection('users').document(user_id).delete()
