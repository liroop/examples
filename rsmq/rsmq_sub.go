package main

import (
    "context"
    "encoding/json"
    "fmt"

    "github.com/go-redis/redis/v9"
)

type Info struct {
    Name string
    Age  int
}

var (
        ctx = context.Background()
        //rdb *redis.Client
)

func (i Info) MarshalBinary() ([]byte, error) {
    return json.Marshal(i)
}

func main() {
    rdb := redis.NewClient(&redis.Options{
        Addr:        "localhost:6379",
        Password:    "",
        DB:          0,
        ReadTimeout: -1,
    })

    // There is no error because go-redis automatically reconnects on error.
	pubsub := rdb.Subscribe(ctx, "mychannel1")

	// Close the subscription when we are done.
	defer pubsub.Close()

	ch := pubsub.Channel()

	for msg := range ch {
			b := []byte(msg.Payload)
			fmt.Printf("ch:%v, pl:%v, b:%v\n", msg.Channel, msg.Payload, b)
	}
}