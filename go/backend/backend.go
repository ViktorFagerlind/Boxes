package main

import (
	"context"
	"log"
	"os"
	"net"

	"google.golang.org/grpc"
	"boxes/backend/config"
	pb "boxes/backend/protos"
)


const (
	port = ":50051"
)


// server is used to implement helloworld.GreeterServer.
type server struct {
	pb.UnimplementedBackendServer
}


func (c *server) Initialise(ctx context.Context, in *pb.ConfigFile) (*pb.Empty, error) {
	config, err := config.LoadConfiguration(in.GetYamlPath())

	log.Printf("--- Config:\n%v\n\n", config)

	return &pb.Empty{}, err
}

func main() {

	if len(os.Args) >= 2 && os.Args[1] == "-c" {
		config, _ := config.LoadConfiguration("../../input/tables_and_charts.yaml")
	  log.Printf("--- Config:\n%v\n\n", config)
		return
	}


	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
		return
	}
	s := grpc.NewServer()

	pb.RegisterBackendServer(s, &server{})
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
		return
	}
}
