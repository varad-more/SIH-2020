import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request


# Using flask to make an api 
# import necessary libraries and functions 

from flask import Flask, jsonify, request 
  
# creating a Flask app 
app = Flask(__name__) 
  
# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 
@app.route('/', methods = ['GET', 'POST']) 
def home():
	if(request.method == 'GET'):

		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM company_list")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		print (resp)
		return  resp
        # data = "hello world"
	else : 
		pass 



@app.route('/add/<int:num>/<string:company_name>', methods=['POST'])
def add(num, company_name):
	try:
		if request.method == 'POST':

			sql = "INSERT INTO company_list (id, name ) VALUES(%s, %s)"
			data = (num,company_name)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Added successfully!')
			resp.status_code = 200
			return resp
		else:
    			pass
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update/<int:num>/<string:company_name>', methods=['PUT'])
def update(num, company_name):
	try:
		# _json = request.json
		# _id = _json['id']
		# _name = _json['name']
		# _email = _json['email']
		# _password = _json['pwd']		
		# validate the received values
		if request.method == 'PUT':
			
			sql = "UPDATE company_list SET name=%s WHERE id=%s"
			data = (company_name, num)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
				print(" Incorrect method, update function failed")
				pass
			
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		



@app.route('/delete/<int:num>', methods=['DELETE'])
def delete(num):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM company_list  WHERE id=%s", (num,))
		conn.commit()
		resp = jsonify('Deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

  
# A simple function to calculate the square of a number 
# the number to be squared is sent in the URL when we use GET 
# on the terminal type: curl http://127.0.0.1:5000 / home / 10 
# this returns 100 (square of 10) 
# @app.route('/home/<int:num>', methods = ['GET']) 
# def disp(num): 
  
#     return jsonify({'data': num**2}) 
  
  
# driver function 
# if __name__ == '__main__': 
#     # app.run(debug = True) 
#     app.config['TEMPLATES_AUTO_RELOAD'] = True
#     app.run(debug=True, host='0.0.0.0')