package main

import (
	"context"
	"log"
	"net"

	"google.golang.org/grpc"
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
	log.Printf("Received: %v", in.GetYamlPath())

	return &pb.Empty{}, nil
}

func main() {
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()

	pb.RegisterBackendServer(s, &server{})
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
