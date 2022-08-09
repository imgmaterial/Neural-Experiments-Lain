from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from flask_cors import CORS
import scrape
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

class Users(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""select * from anime_lists""")
        rows = cursor.fetchall()
        return jsonify(rows)


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
        return jsonify(rows)
        



class Recommender(Resource):
    def get(self):
        _user = request.args.get("user")
        recomends = scrape.translate(_user)
        return jsonify(recomends)



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"






api.add_resource(Users,'/users')
api.add_resource(Recommender,'/rec')
api.add_resource(user_rate_list, '/rate')












if __name__ == '__main__':
    ##from waitress import serve
    ##serve(app, host="0.0.0.0", port=5000)\
    app.run(debug=True)
