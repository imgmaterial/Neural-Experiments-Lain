from urllib import response
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from flask_cors import CORS
import rec
from mysqlconnect import mysqlkey

app = Flask(__name__)
mysql = MySQL()
api = Api(app)
CORS(app)

app.config['MYSQL_DATABASE_USER'] = mysqlkey("user")
app.config['MYSQL_DATABASE_PASSWORD'] = mysqlkey("password")
app.config['MYSQL_DATABASE_DB'] = mysqlkey("database")
app.config['MYSQL_DATABASE_HOST'] = mysqlkey("host")

mysql.init_app(app)

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
        _user = request.form['user']
        _animeid = request.form['animeid']
        _rating = request.form['rating']
        set_user_cmd = "UPDATE anime_lists SET rating = %s WHERE user = %s and animeid = %s"
        cursor.execute(set_user_cmd,(_rating,_user,_animeid))
        response = jsonify(_user,_animeid,_rating)
        response.status_code = 200
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



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"






api.add_resource(Users,'/users')
api.add_resource(Recommender,'/rec')
api.add_resource(user_rate_list, '/rate')
api.add_resource(Anime,'/anime')












if __name__ == '__main__':
    ##from waitress import serve
    ##serve(app, host="0.0.0.0", port=5000)\
    app.run(debug=True)
