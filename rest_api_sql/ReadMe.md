# REST API for SQL using Flask 

## Installing requirements

```
python3 install_requirements.py
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