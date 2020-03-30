var Express = require("express");
var BodyParser = require("body-parser");
var mongoose = require('mongoose');

var app = Express();
app.use(BodyParser.json());
app.use(BodyParser.urlencoded({ extended: true }));

app.listen(3000, function() {
     console.log("Server listening on " + 3000); 
    });

mongoose.connect('mongodb://localhost/scrape_gen', {useNewUrlParser: true, useUnifiedTopology: true });

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
});

var corporate_actions_schema = new mongoose.Schema({
    company_name: String,
    security: String,
    volume: Number,
    action: String
}); 

var Corporate_actions = mongoose.model('Corporate_actions', corporate_actions_schema);


app.get('/',function(req,res){

Corporate_actions.find(function (err, corporate_actions) {
    if (err) return console.error(err);
    res.json({corporate_actions  });
    console.log(corporate_actions);
  })
})