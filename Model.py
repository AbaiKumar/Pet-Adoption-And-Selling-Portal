from tkinter import Image
from pymongo import MongoClient
from Classes import *

class Data:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.database = self.client["Pet_Adoption"]
        self.userCollection = self.database["Users"]
        self.breedCollection = self.database["Breeds"]
        self.petCollection = self.database["Pets"]
        self.orderCollection = self.database["Order"]

    def getMatchedPets(self, mail):

        query = {"mail": mail}
        result = self.userCollection.find_one(query)
        pets = self.petCollection.find()

        if result['survey'] == None:
            return [[0, {
                "id": x["_id"],
                "breed": pets['pet'],
                "image": str(x["image_data"]).replace('\\', '/'),
                "seller_email": x["email"],
                "score": 0
            }] for x in pets][:5]
        pet_details = []
        survey = result['survey']

        for pet in pets:
            if int(pet["price"]) <= 0:
                continue
            a = 0
            pet_survey = self.breedCollection.find_one(
                {"name": pet['breed']})['pet']
            
            if pet['breed'] == "JA Pets":
                b = {
                    "id": pet["_id"],
                    "breed": str(pet_survey['pet']),
                    "image": str(pet["image_data"]).replace('\\', '/'),
                    "seller_email": pet["email"],
                    "score": a,
                    "price": pet["price"]
                }
                pet_details.append(b)
                continue

            if pet_survey['preferences'] not in survey['preferences']:
                continue

            a = sc.calculate(survey, pet_survey)

            b = {
                "id": pet["_id"],
                "breed": str(pet_survey['pet']),
                "image": str(pet["image_data"]).replace('\\', '/'),
                "seller_email": pet["email"],
                "score": a,
                "price": pet["price"]
            }
            pet_details.append(b)
        return sorted(pet_details, key=lambda x: x['score'], reverse=True)[:5]

    def getAdoptionPets(self, mail):
        query = {"mail": mail}
        result = self.userCollection.find_one(query)
        pets = self.petCollection.find()

        if result['survey'] == None:
            return [[0, {
                "id": x["_id"],
                "breed": pets['pet'],
                "image": str(x["image_data"]).replace('\\', '/'),
                "seller_email": x["email"],
                "score": 0
            }] for x in pets][:5]
        pet_details = []
        survey = result['survey']

        for pet in pets:
            print(pet['breed'])
            if int(pet["price"]) != 0:
                continue
            a = 0
            pet_survey = self.breedCollection.find_one(
                {"name": pet['breed']})['pet']
            
            if pet['breed'] == "JA Pets":
                b = {
                    "id": pet["_id"],
                    "breed": str(pet_survey['pet']),
                    "image": str(pet["image_data"]).replace('\\', '/'),
                    "seller_email": pet["email"],
                    "score": a,
                }
                pet_details.append(b)
                continue
                
            if pet_survey['preferences'] not in survey['preferences']:
                continue
            pet_survey = self.breedCollection.find_one(
                {"name": pet['breed']})['pet']
            
        
            a = sc.calculate(survey, pet_survey)

            b = {
                "id": pet["_id"],
                "breed": str(pet_survey['pet']),
                "image": str(pet["image_data"]).replace('\\', '/'),
                "seller_email": pet["email"],
                "score": a,
            }
            pet_details.append(b)
        return sorted(pet_details, key=lambda x: x['score'], reverse=True)

    def createAccount(self, mail, usrObj):
        user_document = {
            "mail": mail,
            "user": usrObj.__dict__
        }
        if (self.userCollection.find_one({"mail": mail}) == None):
            self.userCollection.insert_one(user_document)
            return True
        else:
            return False

    def loginAccount(self, mail, pwd):
        query = {"mail": mail}
        result = self.userCollection.find_one(query)

        if result:
            mail = result.get("mail")
            user = result.get("user")
            if user['pwd'] == pwd:
                return True
        return False

    def updatesurvey(self, mail, usrsurvey):
        query = {"mail": mail}
        result = self.userCollection.find_one(query)
        if result:
            temp = result.get("user")
            user_document = {
                "mail": result.get("mail"),
                "user": temp,
                "survey": usrsurvey.__dict__
            }
            self.userCollection.delete_one(query)
            self.userCollection.insert_one(user_document)

    def updatebreed(self, breed, breedsurvey):
        breed_document = {
            "name": breed,
            "pet": breedsurvey.__dict__
        }
        self.breedCollection.insert_one(breed_document)

    def uploadpet(self, imageid, breed, username, imageURL, price):
        query = {"name": breed}
        result = self.breedCollection.find_one(query)
        if (result != None):
            print("Here err")
            image_document = {
                "_id": imageid,
                "email": username,
                "image_data": imageURL,
                "breed": breed,
                "price": price,
            }
            self.petCollection.insert_one(image_document)
        else:
            print("JA Pets")
            query = {"name": "JA Pets"}
            result = self.breedCollection.find_one(query)
            image_document = {
                "_id": imageid,
                "email": username,
                "image_data": imageURL,
                "breed": "JA Pets",
                "price": price,
            }
            self.petCollection.insert_one(image_document)

    def confirm(self, username, pet_id):
        query = {"_id": pet_id}
        result = self.petCollection.find_one(query)

        order_document = {
            "_id": pet_id,
            "buyer": username,
            "seller": result.get("email"),
            "pet_data": result,
            "seller_confirm": "no",
            "buyer_confirm": "no"
        }
        self.orderCollection.insert_one(order_document)
        self.petCollection.delete_one(result)

    def sellerConfirm(self, pet_id):
        query = {"_id": pet_id}

        update = {
            "$set": {
                "seller_confirm": "yes"
            }
        }
        self.orderCollection.update_one(query, update)

    def buyerConfirm(self, pet_id):
        query = {"_id": pet_id}

        update = {
            "$set": {
                "buyer_confirm": "yes"
            }
        }
        self.orderCollection.update_one(query, update)

    def sellerCancel(self, pet_id):
        query = {"_id": pet_id}
        result = self.orderCollection.find_one(query)
        self.petCollection.insert_one(result.get("pet_data"))
        self.orderCollection.delete_one(query)

    def buyerCancel(self, pet_id):
        query = {"_id": pet_id}
        result = self.orderCollection.find_one(query)
        self.petCollection.insert_one(result.get("pet_data"))
        self.orderCollection.delete_one(query)

    def remove(self, pet_id):
        query = {"_id": pet_id}
        self.petCollection.delete_one(query)

    def getsell(self, mail):

        query = {"email": mail}
        result = self.petCollection.find(query)

        pet_details = []
        for pet in result:
            b = {
                "id": pet["_id"],
                "breed": pet["breed"],
                "seller": pet["email"],
                "image": str(pet["image_data"]).replace('\\', '/'),
                "price": pet["price"]
            }
            pet_details.append(b)
        return pet_details

    def orderList(self, mail):
        query = {"seller": mail}
        cursor = self.orderCollection.find(query)
        sell_list = []
        # Retrieve and store matching documents in a list
        data_list = list(cursor)
        for d in data_list:
            doc = {
                "id": d.get("_id"),
                "seller": d.get("seller"),
                "buyer": d.get("buyer"),
                "seller_confirm": d.get("seller_confirm"),
                "buyer_confirm": d.get("buyer_confirm"),
                "image": str(d.get("pet_data")["image_data"]).replace('\\', '/'),
                "price": (d.get("pet_data")["price"]),
                "breed": (d.get("pet_data")["breed"])
            }
            sell_list.append(doc)

        query = {"buyer": mail}
        cursor = self.orderCollection.find(query)
        buylist = []
        # Retrieve and store matching documents in a list
        data_list1 = list(cursor)
        for d in data_list1:
            doc = {
                "id": d.get("_id"),
                "seller": d.get("seller"),
                "buyer": d.get("buyer"),
                "seller_confirm": d.get("seller_confirm"),
                "buyer_confirm": d.get("buyer_confirm"),
                "image": str(d.get("pet_data")["image_data"]).replace('\\', '/'),
                "price": (d.get("pet_data")["price"]),
                "breed": (d.get("pet_data")["breed"])
            }
            buylist.append(doc)
        print(sell_list)
        print(buylist)

        return list(reversed(sell_list)), list(reversed(buylist))


data = Data()
