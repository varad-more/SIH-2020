# REST API for SQL using Flask 

## Installing requirements

### Python requirements
```
python3 install_requirements.py
```

### Database requirements

Follow steps for installing SQL 
```
https://support.rackspace.com/how-to/install-mysql-server-on-the-ubuntu-operating-system/
```

Incase of permission issue follow the following guide
```
https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost
```

## Running the code 

```
export FLASK_APP=main.py 
flask run
```
<!-- or use 
```
python3 -m flask run
``` -->


## URLs 

Works for CRUD operations with following urls and methods for each operation.

**Read**: Use *GET*
```
http://127.0.0.1:5000/ 
```

**Add**: Use *POST*
```
http://127.0.0.1:5000/add/<int:num>/<string:company_name>
```

**Update**: Use *PUT*
```
http://127.0.0.1:5000/update/<int:num>/<string:company_name>
```

**Delete**: Use *DELETE*
```
http://127.0.0.1:5000/delete/<int:num>
```