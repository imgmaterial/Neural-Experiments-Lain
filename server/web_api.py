from urllib import response
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from flask_cors import CORS
import rec
from datetime import datetime, timedelta, timezone
from mysqlconnect import mysqlkey, jwtsecret
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
import json

app = Flask(__name__)
mysql = MySQL()
api = Api(app)
CORS(app)

app.config["JWT_SECRET_KEY"] = jwtsecret()
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

app.config['MYSQL_DATABASE_USER'] = mysqlkey("user")
app.config['MYSQL_DATABASE_PASSWORD'] = mysqlkey("password")
app.config['MYSQL_DATABASE_DB'] = mysqlkey("database")
app.config['MYSQL_DATABASE_HOST'] = mysqlkey("host")

mysql.init_app(app)

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response


class Anime(Resource):
    def get(self):
        _anime_id = request.args.get("anime_id")
        conn = mysql.connect()
        cursor = conn.cursor()
        sql_command = "select * from anime_info WHERE anime_id in (%s)"
        cursor.execute(sql_command, (_anime_id))
        rows = cursor.fetchall()
        rows = list(rows)[0]
        response = {"anime_id":rows[0], "anime_name":rows[1], "anime_type":rows[2], "anime_score":rows[3]}
        return response



class Users(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""select distinct(user) from anime_lists""")
        rows = cursor.fetchall()
        rows = list(rows)
        user_list = []
        for i in rows:
            i = str(i[0])
            user = {"user_name": i}
            user_list.append(user)
        response = user_list
        return response


    def post(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        _user = request.form['user']
        _animeid = request.form['animeid']
        _rating = request.form['rating']
        insert_user_cmd = """INSERT INTO anime_lists(user, animeid, rating) VALUES(%s, %s, %s)"""
        cursor.execute(insert_user_cmd, (_user, _animeid, _rating))
        conn.commit()
        response = jsonify(message='User added successfully.', id=cursor.lastrowid)
        response.status_code = 200
        cursor.close()
        conn.close()
        return(response)
    
class user_rate_list(Resource):
    def get(self):
        _user = request.args.get("user")
        response = _user
        conn = mysql.connect()
        cursor = conn.cursor()
        sql_command = "select * from anime_lists WHERE user in (%s)"
        cursor.execute(sql_command, (str(_user)))
        rows = cursor.fetchall()
        rows = list(rows)
        rate_list = []
        for i in rows:
            i = list(i)
            user_rates = {"animeid": i[1], "rating": i[2]}
            rate_list.append(user_rates)
        response = {"user": str(_user), "titles": rate_list}
        return response

    def put(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        _user = request.args.get("user")
        _animeid = request.args.get("animeid")
        _rating = request.args.get("rating")
        set_user_cmd = "UPDATE anime_lists SET rating = %s WHERE (user = %s and animeid = %s) limit 1"
        cursor.execute(set_user_cmd,(int(_rating),str(_user),int(_animeid)))
        conn.commit()
        response = {"user":_user,"animeid":_animeid,"rating":_rating}
        return response

        



class Recommender(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        _user = request.args.get("user")
        recomends = rec.get_preds_for_user(_user)
        recomends = list(recomends)
        recommendation_list = []
        for i in recomends:
            i = list(i)
            command = "select anime_name from anime_info where anime_id = %s"
            cursor.execute(command,(i[0]))
            rows = cursor.fetchall()
            item = {"animeid":i[0], "anime_name":rows[0][0], "rating":i[1]}
            recommendation_list.append(item)
        response = {"user":_user, "recommendations":recommendation_list}
        return response


class token(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        _email = request.args.get("email")
        _password = request.args.get("password")
        command = "select * from user_data where email = %s limit 1"
        cursor.execute(command, (_email))
        rows = list(cursor.fetchall())
        if rows == [] or _password != rows[0][3]:
            response = "Wrong email or password"
            return response
        access_token = create_access_token(identity=rows[0][1],)
        response = {"access_token":access_token}
        return response

class logout(Resource):
    def get(self):
        response = "Logging out"
        unset_jwt_cookies(response)
        return response



class registration(Resource):
    def post(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        _user_name = request.form['user_name']
        _email = request.form['email']
        _password = request.form['password']
        rows = cursor.execute("select * from user_data where email = %s",(_email))
        if rows != 0:
            return "Email already in use"
        rows = cursor.execute("select * from user_data where user_name = %s",(_user_name))
        if rows != 0:
            return "Username already in use"
        insert_user_cmd = "INSERT INTO user_data(user_id, user_name, email, password) VALUES(%s, %s, %s, %s)"
        cursor.execute("select max(user_id) from user_data")
        _user_id = cursor.fetchone()
        _user_id = _user_id[0] + 1
        print(_user_id)
        cursor.execute(insert_user_cmd, (_user_id, _user_name, _email,_password ))
        response = {"user_id":_user_id}
        return response


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"




list = {}
list("recomendations")

api.add_resource(Users,'/users')
api.add_resource(Recommender,'/rec')
api.add_resource(user_rate_list, '/rate')
api.add_resource(Anime,'/anime')
api.add_resource(token, '/token')
api.add_resource(logout, '/logout')
api.add_resource(registration, '/registration')








if __name__ == '__main__':
    ##from waitress import serve
    ##serve(app, host="0.0.0.0", port=5000)\
    app.run(debug=True)
