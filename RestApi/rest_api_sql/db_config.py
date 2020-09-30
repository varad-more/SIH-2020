from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'corporate_actions'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# app.config['MYSQL_DATABASE_USER'] = 'admin'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'SIH_2020'
# # app.config['MYSQL_DATABASE_DB'] = 'corporate_actions'
# app.config['MYSQL_DATABASE_HOST'] = 'database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com'



# app.config['MYSQL_DATABASE_USER'] = 'admin'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'sih_2020'
# app.config['MYSQL_DATABASE_DB'] = 'corporate_actions'
# app.config['MYSQL_DATABASE_HOST'] = 'database-1.ctqvk0asvfes.us-east-1.rds.amazonaws.com'

mysql.init_app(app)