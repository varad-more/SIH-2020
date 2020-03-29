const Express = require("express");
const BodyParser = require("body-parser");
const mongoose = require('mongoose');

var app = Express();
app.use(BodyParser.json());
app.use(BodyParser.urlencoded({ extended: true }));

app.listen(3000, function() {
    console.log("Server listening on " + 3000);
  });

mongoose.connect(('mongodb://' + 'localhost' + "/" + 'scarpe_gen'), { useNewUrlParser: true});

var db = mongoose.connection;
db.on('error', (error) => console.error(error))
db.once('open', () => console.log('connected to database'))


var corporate_actions_schema = mongoose.Schema({
    company_name: {type:String, required: true},
    security: {type:String, required: true},
    volume:{type:Number},
    action:{type:String}
})
var corporate_actions = mongoose.model('corporate_actions', corporate_actions_schema);
  

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