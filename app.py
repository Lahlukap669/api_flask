from flask import Flask, jsonify, request
import json
import hashlib
from flask_cors import CORS
app = Flask(__name__)


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://teecnvbl:ySNvS-XgSa_ql6SKZk87vdKyxwVKp3Ki@kandula.db.elephantsql.com:5432/teecnvbl"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

@app.route("/", methods=['GET','POST'])
def index():
    if(request.method == 'POST'):
        podatki_json = request.get_json()
        print(podatki_json["ime"])
        return jsonify({'ime': podatki_json["ime"]}), 201
    else:
        return jsonify({'u sent':"nothing"})


##REGISTER
@app.route("/register", methods=['GET','POST'])
def register():
    if(request.method == 'POST'):
        ##example of input data:
##        {
##          "ime": "Luka1",
##          "priimek": "Lah1",
##          "email": "luka1.lah@gmail.com",
##          "geslo": "Luka123"
##        }
        podatki_json = request.get_json()
        #print(podatki_json)
        ##Deviding sent data
        ime = podatki_json["ime"]
        priimek = podatki_json["priimek"]
        email = podatki_json["email"]
        geslo = podatki_json["geslo"]
        ##converting from string to byte
        geslo = bytes(geslo, 'utf-8')
        ##Hashing
        geslo_h = hashlib.sha256(geslo).hexdigest()

##interaction db
        try:
            ##Called function
            db.session.execute("""SELECT register('%s', '%s', '%s', '%s');"""%(ime, priimek, email, geslo_h))
            db.session.commit()
            ##Returned data to program
            return jsonify({'bool': True}), 201                
        except Exception as e:
            print(e)
            return jsonify({'bool': False}), 404       
    else:
        return jsonify({'type': "cant use GET"})


##LOGIN
@app.route("/login", methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        ##example of input data:
##        {
##          "email": "luka1.lah@gmail.com",
##          "geslo": "Luka123"
##        }
        podatki_json = request.get_json()
        ##Deviding sent data
        email = podatki_json["email"]
        geslo = podatki_json["geslo"]
        ##converting from string to byte
        geslo = bytes(geslo, 'utf-8')
        ##Hashing
        geslo_h = hashlib.sha256(geslo).hexdigest()
##interaction db
        try:
            ##Called function
            r = db.session.execute("""SELECT login('%s', '%s');"""%(email, geslo_h)).scalar()
            db.session.commit()
            if(r==True):
                return jsonify({"bool": True}), 201
            ##Returned data to program
            else:
                return jsonify({"bool": False})                
        except Exception as e:
            print(e)
            return jsonify({"bool": False}), 404   
    else:
        return jsonify({"u sent": "nothing"})


##ADD PLAYLIST
@app.route("/add_playlist", methods=['GET','POST'])
def add_playlist():
    if(request.method == 'POST'):
        ##example of input data:
##        {
##          "user_id": 1,
##          "ime": "Playlist1",
##          "url": "http://www.yout...",
##          "opis": "neki..."
##        }
        podatki_json = request.get_json()
        ##Deviding sent data
        user_ID = podatki_json["user_id"]
        imeP = podatki_json["ime"]
        URL = podatki_json["url"]
        Opis = podatki_json["opis"]

##interaction db
        try:
            ##Called function
            r = db.session.execute("""SELECT add_playlist('%s', '%s', '%s', '%s');"""%(user_ID, imeP, URL, Opis)).scalar()
            db.session.commit()
            if(r==True):
                return jsonify({'bool': True}), 201
            ##Returned data to program
            else:
                return jsonify({'bool': False})                
        except Exception as e:
            print(e)
            return jsonify({'bool': False}), 404   
    else:
        return jsonify({'u sent': "nothing"})


##DELETE PLAYLIST
@app.route("/add_playlist", methods=['GET','POST'])
def delete_playlist():
    if(request.method == 'POST'):
        ##example of input data:
##        {
##          "pid": 1,
##        }
        podatki_json = request.get_json()
        ##Deviding sent data
        p_ID = podatki_json["pid"]

##interaction db
        try:
            ##Called function
            r = db.session.execute("""SELECT del_playlist(%d);"""%(p_ID)).scalar()
            db.session.commit()
            if(r==True):
                return jsonify({'bool': True}), 201
            ##Returned data to program
            else:
                return jsonify({'bool': False})                
        except Exception as e:
            print(e)
            return jsonify({'bool': False}), 404   
    else:
        return jsonify({'u sent': "nothing"})


##ADD PLAYLIST
@app.route("/add_playlist", methods=['GET','POST'])
def update_playlist():
    if(request.method == 'POST'):
        ##example of input data:
##        {
##          "user_id": 1,
##          "ime": "Playlist1",
##          "url": "http://www.yout...",
##          "opis": "neki..."
##        }
        podatki_json = request.get_json()
        ##Deviding sent data
        user_ID = podatki_json["user_id"]
        imeP = podatki_json["ime"]
        URL = podatki_json["url"]
        Opis = podatki_json["opis"]

##interaction db
        try:
            ##Called function
            r = db.session.execute("""SELECT update_playlist('%s', '%s', '%s', '%s');"""%(user_ID, imeP, URL, Opis)).scalar()
            db.session.commit()
            if(r==True):
                return jsonify({'bool': True}), 201
            ##Returned data to program
            else:
                return jsonify({'bool': False})                
        except Exception as e:
            print(e)
            return jsonify({'bool': False}), 404   
    else:
        return jsonify({'u sent': "nothing"})


@app.route("/userinfo", methods=['GET','POST'])
def userinfo():
    if(request.method == 'POST'):
        ##example of input data:
##        {
##          "user_id": 1,
##          "ime": "Playlist1",
##          "url": "http://www.yout...",
##          "opis": "neki..."
##        }
        podatki_json = request.get_json()
        ##Deviding sent data
        email = podatki_json["email"]

##interaction db
        try:
            ##Called function
            r = db.session.execute("""SELECT userinfo('%s');"""%(email)).scalar()
            db.session.commit()
            return jsonify(r), 200

        except Exception as e:
            print(e)
            return jsonify({'bool': False}), 404   
    else:
        return jsonify({'u sent': "nothing"})

##new_user = Users(ime=ime, priimek=priimek, email=email, geslo=geslo_h)
##db.session.add(new_user)
##db.session.add("SELECT register(%s, %s, %s, %s)"%(ime, priimek, email, geslo))#new_user)
##db.session.query("SELECT register(%s, %s, %s, %s)"%(ime, priimek, email, geslo))
##db.session.commit()

##@app.route("/multi/<int:num>", methods=['GET'])
##def multiply(num):
##    return jsonify({'u sent': num*10})

if __name__ == '__main__':
    app.run(debug=True)
