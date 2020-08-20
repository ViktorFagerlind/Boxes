package backend

import (
	pb "boxes/backend/protos"
	"context"
	"log"
	"sync"
	"time"

	"google.golang.org/grpc"
)

type proxy struct {
	Connection *grpc.ClientConn
	Client     pb.DataEngineClient
}

var dataEngineProxySingleton *proxy
var dataEngineProxyOnce sync.Once

func GetDataEngineProxy() *proxy {
	dataEngineProxyOnce.Do(func() {
		dataEngineProxySingleton = &proxy{}
	})
	return dataEngineProxySingleton
}

func (this *proxy) Connect(address string) error {
	// Set up a connection to the server.
	var err error
	this.Connection, err = grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
		return err
	}
	//defer singleton.Connection.Close() TODO: Close somewhere
	this.Client = pb.NewDataEngineClient(this.Connection)

	log.Printf("Successful connection established")

	return nil
}

func (this *proxy) ExecuteQuery(query string, columnTypes []pb.ColumnType) error {
	ctx, cancel := context.WithTimeout(context.Background(), time.Minute)
	defer cancel()
	r, err := this.Client.ExecuteQuery(ctx, &pb.Query{Q: query, ColumnTypes: columnTypes})
	if err != nil {
		log.Fatalf("Error executing query: %v", err)
		return err
	}

	log.Printf("Query result: %v", r)

	return nil
}
