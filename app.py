# from flask import Flask
# import mysql.connector
# import pymysql

# # roomioDb = mysql.connector.connect(
# #   host="127.0.0.1",
# #   port="8889",
# #   database='roomioDb',
# #   # user="bkServer",
# #   # password="complexPasswrd"
# #   user = "root" ,
# #   password = "deepjyot"
# # )


# roomioDb = pymysql.connect(host='localhost',
#                        port = 3306,
#                        user='root',
#                        password='deepjyot',
#                        db='RoomioDb',
#                        charset='utf8mb4',
#                        cursorclass=pymysql.cursors.DictCursor)

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     print(roomioDb)
#     return "<p>Hello, World!</p>"
