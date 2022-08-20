package main

import (
    "context"
    "encoding/json"
    "fmt"

    "github.com/go-redis/redis/v9"
)

type ColorGroup struct {
    ByteSlice    []byte
    SingleByte   byte
    IntSlice     []int
}

var (
        ctx = context.Background()
        //rdb *redis.Client
)

func main() {
    rdb := redis.NewClient(&redis.Options{
        Addr:        "localhost:6379",
        Password:    "",
        DB:          0,
        ReadTimeout: -1,
    })

    group := ColorGroup{
        ByteSlice:  []byte{0,0,0,1,2,3},
        SingleByte: 10,
        IntSlice:   []int{0,0,0,1,2,3},
    }

    data, err := json.Marshal(group)
    if err != nil {
        fmt.Println("error:", err)
    }

    err = rdb.Publish(ctx, "mychannel1", data).Err()
    if err != nil {
        panic(err)
    }
    fmt.Println("published, len=", len(data))
}