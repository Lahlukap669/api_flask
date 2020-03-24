from flask import Flask, jsonify, request
import json
import hashlib
from flask_cors import CORS
app = Flask(__name__)


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://hfprgeev:QEUmvQfSGTj1Pueh3q02mjUxUl0Fa93e@kandula.db.elephantsql.com:5432/hfprgeev"
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
        user_ID = int(podatki_json["user_id"])
        imeP = podatki_json["ime"]
        URL = podatki_json["url"]
        Opis = podatki_json["opis"]
        print(user_ID, imeP, URL, Opis)
##interaction db
        try:
            ##Called function
            r = db.session.execute("""SELECT add_playlist(%d, '%s', '%s', '%s');"""%(user_ID, imeP, URL, Opis)).scalar()
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
@app.route("/del_playlist", methods=['GET','POST'])
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


##UPDATE PLAYLIST
@app.route("/update_playlist", methods=['GET','POST'])
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



##USER INFO
@app.route("/userinfo", methods=['GET','POST'])
def userinfo():
    if(request.method == 'POST'):
        ##example of input data:
##        {
##          "email": "luka1.lah@gmail.ocm",
##        }
        podatki_json = request.get_json()
        ##Deviding sent data
        email = podatki_json["email"]

##interaction db
        try:
            ##Called function
            r = db.session.execute("""SELECT * FROM users WHERE email='%s' LIMIT 1;"""%(email)).first()
            db.session.commit()
            r=str(r)[1:-1]
            r=r.replace(" ", "")
            r=r.replace("'", "")
            r=r.split(",")
            r1 = {"id": int(r[0]), "ime": "%s"%(r[1]), "priimek": "%s"%(r[2]), "email": "%s"%(r[3]), "geslo": "%s"%(r[4]), "admin": int(r[5])}  
            return r1, 200

        except Exception as e:
            print(e)
            return jsonify({'bool': False}), 404   
    else:
        return jsonify({'u sent': "nothing"})


##PLAYLISTS
@app.route("/playlists", methods=['GET','POST'])
def playlists():
    if(request.method == 'POST'):
        ##example of input data:
##        {
##          "email": "luka1.lah@gmail.ocm",
##        }
        podatki_json = request.get_json()
        ##Deviding sent data
        email = podatki_json["email"]

##interaction db
        try:
            ##Called function
            r = db.session.execute("""SELECT * FROM playlists WHERE user_id=(SELECT id FROM users WHERE email='%s') LIMIT 1;"""%(email)).fetchall()
            db.session.commit()
            #r=str(r)[1:-1]
            print(r)
            for i in range(len(r)):
                r1 = {"id": int(r[i][0]), "user_id": int(r[i][1]), "name": "%s"%(r[i][2]), "url": "%s"%(r[i][3]), "opis": "%s"%(r[i][4])}  
            return r1, 200

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
