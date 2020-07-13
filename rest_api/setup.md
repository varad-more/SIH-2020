# JS Setup 
sudo apt install npm
npm init
npm install mongoose
npm install body-parser
npm install express

# Starting MongoDB
```
sudo mongod --dbpath=db/
```
# Using Mongo DB
## Start UP 
mongo

## In case of failure
```
sudo netstat -plnt
sudo kill -9 <PID of mongod>
```
## Queries
```
show dbs
use scarpe_gen
show collections
db.corporate_actions.find( {} )
```

### Inserting
```
db.corporate_actions.insertOne(
    {"company_name": "NSE",
    "security": "NIFTY50",
    "volume":12300,
    "action":"Stock Split"
})
```

# Starting Server
```
node app.js
```