var redis = require("redis"),
        client = redis.createClient();

    // if you'd like to select database 3, instead of 0 (default), call
    // client.select(3, function() { /* ... */ });

    client.on("error", function (err) {
        console.log("DEN: Error " + err);
        client.end();
    });

    client.set("string key", "string val_den", redis.print);
    client.hset("hash key", "hashtest 1", "some value", redis.print);
    client.hset(["hash key", "hashtest 2", "some other value"], redis.print);
    client.hkeys("hash key", function (err, replies) {
        console.log(replies.length + " replies:");
        replies.forEach(function (reply, i) {
            console.log("    " + i + ": " + reply);
        });        
    });

    client.get("missingkey", function(err, reply) {
        // reply is null when the key is missing
        console.log(reply);
    });

    client.get("string key", function(err, reply) {        
        console.log(reply);
    });
    

    setTimeout(
        function() {
            console.log('wait done');
            client.get("string key", function(err, reply) {                
                console.log(reply);
                client.quit();
            });
        }, 
    5000);
