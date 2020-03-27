const Express = require("express");
const BodyParser = require("body-parser");
// const router = Express.Router()
const mongoose = require('mongoose');
//const MongoClient = require("mongodb").MongoClient;
// const ObjectId = require("mongodb").ObjectID;
var app = Express();
app.use(BodyParser.json());
app.use(BodyParser.urlencoded({ extended: true }));
// app.listen(5000, () => {});

app.listen(3000, function() {
    console.log("Server listening on " + 3000);
  });

mongoose.connect(('mongodb://' + 'localhost' + "/" + 'scarpe_gen'), { useNewUrlParser: true});
const db = mongoose.connection
db.on('error', (error) => console.error(error))
db.once('open', () => console.log('connected to database'))


var corporate_actions_schema = mongoose.Schema({
    company_name: {type:String, required: true},
    security: {type:String, required: true},
    volume:{type:Number},
    action:{type:String}
})
const corporate_actions = mongoose.model('corporate_actions', corporate_actions_schema);
  

app.get('/',function(req,res,db){

    res.send("Reached");
    console.log("Requesting MongoDB");

    db.corporate_actions.find({}, function(error, found){
    res.json(found);
    if (error){
        console.log (error);
    }
    })
})    

// db.corporate_actions.find

// const Express = require("express");
// const BodyParser = require("body-parser");
// const MongoClient = require("mongodb").MongoClient;
// const ObjectId = require("mongodb").ObjectID;
// const CONNECTION_URL = ;
// const DATABASE_NAME = "accounting_department";
 
 

// var app = Express();

// app.use(BodyParser.json());
// app.use(BodyParser.urlencoded({ extended: true }));
// var database, collection;


// app.listen(5000, () => {
//     MongoClient.connect(CONNECTION_URL, { useNewUrlParser: true }, (error, client) => {
//         if(error) {
//             throw error;
//         }
//         database = client.db(DATABASE_NAME);
//         collection = database.collection("personnel");
//         console.log("Connected to `" + DATABASE_NAME + "`!");
//     });
// });