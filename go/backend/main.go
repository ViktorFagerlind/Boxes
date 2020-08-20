package main

import (
	"context"
	"log"
	"net"
	"os"

	"boxes/backend/backend"
	pb "boxes/backend/protos"

	"google.golang.org/grpc"
)

const (
	port = ":50051"
)

// server is used to implement helloworld.GreeterServer.
type server struct {
	pb.UnimplementedBackendServer
}

func initialise(yamlPath string) error {
	config, err := backend.LoadConfiguration(yamlPath)

	if err != nil {
		log.Fatalf("Failed to load confix: %v", err)
		return err
	}

	log.Printf("--- Config:\n%v\n\n", config)

	chartCollection := backend.GetChartsManager()

	chartCollection.Initialise(config.Charts)

	dataEngine := backend.GetDataEngineProxy()

	err = dataEngine.Connect("vfhome.asuscomm.com:51234")

	if err != nil {
		log.Fatalf("Failed to connect to data engine: %v", err)
		return err
	}

	err = dataEngine.ExecuteQuery("select * from all_activities", []pb.ColumnType{pb.ColumnType_TEXT})

	return nil
}

func (c *server) Initialise(ctx context.Context, in *pb.ConfigFile) (*pb.Empty, error) {
	err := initialise(in.GetYamlPath())

	return &pb.Empty{}, err
}

func (c *server) GetCharts(context.Context, *pb.Empty) (*pb.ChartCollection, error) {
	collection, err := backend.GetChartsManager().GetCharts()

	return collection, err
}

/*
func (*UnimplementedBackendServer) GetPlotValues(context.Context, *PlotName) (*PlotValues, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetPlotValues not implemented")
}
func (*UnimplementedBackendServer) GetLoadedTables(context.Context, *Empty) (*TableCollection, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetLoadedTables not implemented")
}
func (*UnimplementedBackendServer) GetAllTableNames(context.Context, *Empty) (*TableNames, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetAllTableNames not implemented")
}
func (*UnimplementedBackendServer) GetTableSchemas(context.Context, *TableNames) (*TableSchemas, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetTableSchemas not implemented")
}
func (*UnimplementedBackendServer) GetTable(context.Context, *TableName) (*Table, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetTable not implemented")
}
func (*UnimplementedBackendServer) AddChart(context.Context, *ChartInfo) (*Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method AddChart not implemented")
}
func (*UnimplementedBackendServer) RemoveChart(context.Context, *ChartName) (*Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method RemoveChart not implemented")
}
func (*UnimplementedBackendServer) LoadTable(context.Context, *TableName) (*TableCollection, error) {
	return nil, status.Errorf(codes.Unimplemented, "method LoadTable not implemented")
}
func (*UnimplementedBackendServer) UnloadTable(context.Context, *TableName) (*TableCollection, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UnloadTable not implemented")
}
func (*UnimplementedBackendServer) mustEmbedUnimplementedBackendServer() {}
*/

func main() {

	if len(os.Args) >= 2 && os.Args[1] == "-i" {
		initialise("../../input/tables_and_charts.yaml")
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
