# JS Setup 
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


