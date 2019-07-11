package examples

import (
	"context"
	"fmt"
	psh "github.com/platformsh/config-reader-go/v2"
	mongoPsh "github.com/platformsh/config-reader-go/v2/mongo"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"time"
)

func UsageExampleMongoDB() string {

	// Create a NewRuntimeConfig object to ease reading the Platform.sh environment variables.
	// You can alternatively use os.Getenv() yourself.
	config, err := psh.NewRuntimeConfig()
	if err != nil {
		panic(err)
	}

	// Get the credentials to connect to the Solr service.
	credentials, err := config.Credentials("mongodb")
	checkErr(err)

	// Retrieve the formatted credentials for mongo-driver.
	formatted, err := mongoPsh.FormattedCredentials(credentials)
	if err != nil {
		panic(err)
	}

	// Connect to MongoDB using the formatted credentials.
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(formatted))
	checkErr(err)

	// Create a new collection.
	collection := client.Database("main").Collection("starwars")

	// Create an entry.
	res, err := collection.InsertOne(ctx, bson.M{"name": "Rey", "occupation": "Jedi"})
	checkErr(err)
	id := res.InsertedID

	// Read it back.
	cursor, err := collection.Find(context.Background(), bson.M{"_id": id})
	if err != nil {
		panic(err)
	}

	var name string
	var occupation string

	for cursor.Next(context.Background()) {
		document := struct {
			Name       string
			Occupation string
		}{}
		err := cursor.Decode(&document)
		if err != nil {
			panic(err)
		}
		name = document.Name
		occupation = document.Occupation
	}

	return fmt.Sprintf("Found %s (%s)", name, occupation)
}
