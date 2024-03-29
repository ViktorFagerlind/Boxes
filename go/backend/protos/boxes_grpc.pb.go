// Code generated by protoc-gen-go-grpc. DO NOT EDIT.

package protos

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion6

// ConnectorClient is the client API for Connector service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type ConnectorClient interface {
	// Get table schemas
	GetTableNames(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*TableNames, error)
	// Get table schemas
	GetTableSchemas(ctx context.Context, in *TableNames, opts ...grpc.CallOption) (*TableSchemas, error)
	// Get table contents
	GetTable(ctx context.Context, in *TableName, opts ...grpc.CallOption) (*Table, error)
}

type connectorClient struct {
	cc grpc.ClientConnInterface
}

func NewConnectorClient(cc grpc.ClientConnInterface) ConnectorClient {
	return &connectorClient{cc}
}

func (c *connectorClient) GetTableNames(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*TableNames, error) {
	out := new(TableNames)
	err := c.cc.Invoke(ctx, "/boxes.Connector/GetTableNames", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *connectorClient) GetTableSchemas(ctx context.Context, in *TableNames, opts ...grpc.CallOption) (*TableSchemas, error) {
	out := new(TableSchemas)
	err := c.cc.Invoke(ctx, "/boxes.Connector/GetTableSchemas", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *connectorClient) GetTable(ctx context.Context, in *TableName, opts ...grpc.CallOption) (*Table, error) {
	out := new(Table)
	err := c.cc.Invoke(ctx, "/boxes.Connector/GetTable", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// ConnectorServer is the server API for Connector service.
// All implementations must embed UnimplementedConnectorServer
// for forward compatibility
type ConnectorServer interface {
	// Get table schemas
	GetTableNames(context.Context, *Empty) (*TableNames, error)
	// Get table schemas
	GetTableSchemas(context.Context, *TableNames) (*TableSchemas, error)
	// Get table contents
	GetTable(context.Context, *TableName) (*Table, error)
	mustEmbedUnimplementedConnectorServer()
}

// UnimplementedConnectorServer must be embedded to have forward compatible implementations.
type UnimplementedConnectorServer struct {
}

func (*UnimplementedConnectorServer) GetTableNames(context.Context, *Empty) (*TableNames, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetTableNames not implemented")
}
func (*UnimplementedConnectorServer) GetTableSchemas(context.Context, *TableNames) (*TableSchemas, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetTableSchemas not implemented")
}
func (*UnimplementedConnectorServer) GetTable(context.Context, *TableName) (*Table, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetTable not implemented")
}
func (*UnimplementedConnectorServer) mustEmbedUnimplementedConnectorServer() {}

func RegisterConnectorServer(s *grpc.Server, srv ConnectorServer) {
	s.RegisterService(&_Connector_serviceDesc, srv)
}

func _Connector_GetTableNames_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ConnectorServer).GetTableNames(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Connector/GetTableNames",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ConnectorServer).GetTableNames(ctx, req.(*Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _Connector_GetTableSchemas_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(TableNames)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ConnectorServer).GetTableSchemas(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Connector/GetTableSchemas",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ConnectorServer).GetTableSchemas(ctx, req.(*TableNames))
	}
	return interceptor(ctx, in, info, handler)
}

func _Connector_GetTable_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(TableName)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(ConnectorServer).GetTable(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Connector/GetTable",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(ConnectorServer).GetTable(ctx, req.(*TableName))
	}
	return interceptor(ctx, in, info, handler)
}

var _Connector_serviceDesc = grpc.ServiceDesc{
	ServiceName: "boxes.Connector",
	HandlerType: (*ConnectorServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "GetTableNames",
			Handler:    _Connector_GetTableNames_Handler,
		},
		{
			MethodName: "GetTableSchemas",
			Handler:    _Connector_GetTableSchemas_Handler,
		},
		{
			MethodName: "GetTable",
			Handler:    _Connector_GetTable_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "boxes.proto",
}

// AlgorithmsClient is the client API for Algorithms service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type AlgorithmsClient interface {
	Max(ctx context.Context, in *DoubleList, opts ...grpc.CallOption) (*DoubleValue, error)
	Min(ctx context.Context, in *DoubleList, opts ...grpc.CallOption) (*DoubleValue, error)
	Average(ctx context.Context, in *DoubleList, opts ...grpc.CallOption) (*DoubleValue, error)
	Median(ctx context.Context, in *DoubleList, opts ...grpc.CallOption) (*DoubleValue, error)
}

type algorithmsClient struct {
	cc grpc.ClientConnInterface
}

func NewAlgorithmsClient(cc grpc.ClientConnInterface) AlgorithmsClient {
	return &algorithmsClient{cc}
}

func (c *algorithmsClient) Max(ctx context.Context, in *DoubleList, opts ...grpc.CallOption) (*DoubleValue, error) {
	out := new(DoubleValue)
	err := c.cc.Invoke(ctx, "/boxes.Algorithms/Max", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *algorithmsClient) Min(ctx context.Context, in *DoubleList, opts ...grpc.CallOption) (*DoubleValue, error) {
	out := new(DoubleValue)
	err := c.cc.Invoke(ctx, "/boxes.Algorithms/Min", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *algorithmsClient) Average(ctx context.Context, in *DoubleList, opts ...grpc.CallOption) (*DoubleValue, error) {
	out := new(DoubleValue)
	err := c.cc.Invoke(ctx, "/boxes.Algorithms/Average", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *algorithmsClient) Median(ctx context.Context, in *DoubleList, opts ...grpc.CallOption) (*DoubleValue, error) {
	out := new(DoubleValue)
	err := c.cc.Invoke(ctx, "/boxes.Algorithms/Median", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// AlgorithmsServer is the server API for Algorithms service.
// All implementations must embed UnimplementedAlgorithmsServer
// for forward compatibility
type AlgorithmsServer interface {
	Max(context.Context, *DoubleList) (*DoubleValue, error)
	Min(context.Context, *DoubleList) (*DoubleValue, error)
	Average(context.Context, *DoubleList) (*DoubleValue, error)
	Median(context.Context, *DoubleList) (*DoubleValue, error)
	mustEmbedUnimplementedAlgorithmsServer()
}

// UnimplementedAlgorithmsServer must be embedded to have forward compatible implementations.
type UnimplementedAlgorithmsServer struct {
}

func (*UnimplementedAlgorithmsServer) Max(context.Context, *DoubleList) (*DoubleValue, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Max not implemented")
}
func (*UnimplementedAlgorithmsServer) Min(context.Context, *DoubleList) (*DoubleValue, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Min not implemented")
}
func (*UnimplementedAlgorithmsServer) Average(context.Context, *DoubleList) (*DoubleValue, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Average not implemented")
}
func (*UnimplementedAlgorithmsServer) Median(context.Context, *DoubleList) (*DoubleValue, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Median not implemented")
}
func (*UnimplementedAlgorithmsServer) mustEmbedUnimplementedAlgorithmsServer() {}

func RegisterAlgorithmsServer(s *grpc.Server, srv AlgorithmsServer) {
	s.RegisterService(&_Algorithms_serviceDesc, srv)
}

func _Algorithms_Max_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(DoubleList)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AlgorithmsServer).Max(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Algorithms/Max",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AlgorithmsServer).Max(ctx, req.(*DoubleList))
	}
	return interceptor(ctx, in, info, handler)
}

func _Algorithms_Min_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(DoubleList)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AlgorithmsServer).Min(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Algorithms/Min",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AlgorithmsServer).Min(ctx, req.(*DoubleList))
	}
	return interceptor(ctx, in, info, handler)
}

func _Algorithms_Average_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(DoubleList)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AlgorithmsServer).Average(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Algorithms/Average",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AlgorithmsServer).Average(ctx, req.(*DoubleList))
	}
	return interceptor(ctx, in, info, handler)
}

func _Algorithms_Median_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(DoubleList)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AlgorithmsServer).Median(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Algorithms/Median",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AlgorithmsServer).Median(ctx, req.(*DoubleList))
	}
	return interceptor(ctx, in, info, handler)
}

var _Algorithms_serviceDesc = grpc.ServiceDesc{
	ServiceName: "boxes.Algorithms",
	HandlerType: (*AlgorithmsServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Max",
			Handler:    _Algorithms_Max_Handler,
		},
		{
			MethodName: "Min",
			Handler:    _Algorithms_Min_Handler,
		},
		{
			MethodName: "Average",
			Handler:    _Algorithms_Average_Handler,
		},
		{
			MethodName: "Median",
			Handler:    _Algorithms_Median_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "boxes.proto",
}

// DataEngineClient is the client API for DataEngine service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type DataEngineClient interface {
	// Plot x antal axlar
	// Axel kategorisk eller numerisk
	ExecuteQuery(ctx context.Context, in *Query, opts ...grpc.CallOption) (*Table, error)
}

type dataEngineClient struct {
	cc grpc.ClientConnInterface
}

func NewDataEngineClient(cc grpc.ClientConnInterface) DataEngineClient {
	return &dataEngineClient{cc}
}

func (c *dataEngineClient) ExecuteQuery(ctx context.Context, in *Query, opts ...grpc.CallOption) (*Table, error) {
	out := new(Table)
	err := c.cc.Invoke(ctx, "/boxes.DataEngine/ExecuteQuery", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// DataEngineServer is the server API for DataEngine service.
// All implementations must embed UnimplementedDataEngineServer
// for forward compatibility
type DataEngineServer interface {
	// Plot x antal axlar
	// Axel kategorisk eller numerisk
	ExecuteQuery(context.Context, *Query) (*Table, error)
	mustEmbedUnimplementedDataEngineServer()
}

// UnimplementedDataEngineServer must be embedded to have forward compatible implementations.
type UnimplementedDataEngineServer struct {
}

func (*UnimplementedDataEngineServer) ExecuteQuery(context.Context, *Query) (*Table, error) {
	return nil, status.Errorf(codes.Unimplemented, "method ExecuteQuery not implemented")
}
func (*UnimplementedDataEngineServer) mustEmbedUnimplementedDataEngineServer() {}

func RegisterDataEngineServer(s *grpc.Server, srv DataEngineServer) {
	s.RegisterService(&_DataEngine_serviceDesc, srv)
}

func _DataEngine_ExecuteQuery_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Query)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(DataEngineServer).ExecuteQuery(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.DataEngine/ExecuteQuery",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(DataEngineServer).ExecuteQuery(ctx, req.(*Query))
	}
	return interceptor(ctx, in, info, handler)
}

var _DataEngine_serviceDesc = grpc.ServiceDesc{
	ServiceName: "boxes.DataEngine",
	HandlerType: (*DataEngineServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "ExecuteQuery",
			Handler:    _DataEngine_ExecuteQuery_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "boxes.proto",
}

// BackendClient is the client API for Backend service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type BackendClient interface {
	// Initialises the backend by loading charts/tables accoring to configuration
	Initialise(ctx context.Context, in *ConfigFile, opts ...grpc.CallOption) (*Empty, error)
	// Get all charts (actual graph window) contaning all plots (each line/scat/bar-collection), excluding actual values
	GetCharts(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*ChartCollection, error)
	// Get x/y values for a certain plot
	GetPlotValues(ctx context.Context, in *PlotName, opts ...grpc.CallOption) (*PlotValues, error)
	// Get information on the loaded plots
	GetLoadedTables(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*TableCollection, error)
	// Get table schemas available in data engine
	GetAllTableNames(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*TableNames, error)
	// Get table schemas from data engine
	GetTableSchemas(ctx context.Context, in *TableNames, opts ...grpc.CallOption) (*TableSchemas, error)
	// Get table contents from loaded table or from one in data engine
	GetTable(ctx context.Context, in *TableName, opts ...grpc.CallOption) (*Table, error)
	// Add chart (and save this configuration in the yaml config)
	AddChart(ctx context.Context, in *ChartInfo, opts ...grpc.CallOption) (*Empty, error)
	// Remove chart (and save this configuration in the yaml config)
	RemoveChart(ctx context.Context, in *ChartName, opts ...grpc.CallOption) (*Empty, error)
	// Load table from data engine (and save this configuration in the yaml config)
	LoadTable(ctx context.Context, in *TableName, opts ...grpc.CallOption) (*TableCollection, error)
	// Unload table from backend (and save this configuration in the yaml config)
	UnloadTable(ctx context.Context, in *TableName, opts ...grpc.CallOption) (*TableCollection, error)
}

type backendClient struct {
	cc grpc.ClientConnInterface
}

func NewBackendClient(cc grpc.ClientConnInterface) BackendClient {
	return &backendClient{cc}
}

func (c *backendClient) Initialise(ctx context.Context, in *ConfigFile, opts ...grpc.CallOption) (*Empty, error) {
	out := new(Empty)
	err := c.cc.Invoke(ctx, "/boxes.Backend/Initialise", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *backendClient) GetCharts(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*ChartCollection, error) {
	out := new(ChartCollection)
	err := c.cc.Invoke(ctx, "/boxes.Backend/GetCharts", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *backendClient) GetPlotValues(ctx context.Context, in *PlotName, opts ...grpc.CallOption) (*PlotValues, error) {
	out := new(PlotValues)
	err := c.cc.Invoke(ctx, "/boxes.Backend/GetPlotValues", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *backendClient) GetLoadedTables(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*TableCollection, error) {
	out := new(TableCollection)
	err := c.cc.Invoke(ctx, "/boxes.Backend/GetLoadedTables", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *backendClient) GetAllTableNames(ctx context.Context, in *Empty, opts ...grpc.CallOption) (*TableNames, error) {
	out := new(TableNames)
	err := c.cc.Invoke(ctx, "/boxes.Backend/GetAllTableNames", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *backendClient) GetTableSchemas(ctx context.Context, in *TableNames, opts ...grpc.CallOption) (*TableSchemas, error) {
	out := new(TableSchemas)
	err := c.cc.Invoke(ctx, "/boxes.Backend/GetTableSchemas", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *backendClient) GetTable(ctx context.Context, in *TableName, opts ...grpc.CallOption) (*Table, error) {
	out := new(Table)
	err := c.cc.Invoke(ctx, "/boxes.Backend/GetTable", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *backendClient) AddChart(ctx context.Context, in *ChartInfo, opts ...grpc.CallOption) (*Empty, error) {
	out := new(Empty)
	err := c.cc.Invoke(ctx, "/boxes.Backend/AddChart", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *backendClient) RemoveChart(ctx context.Context, in *ChartName, opts ...grpc.CallOption) (*Empty, error) {
	out := new(Empty)
	err := c.cc.Invoke(ctx, "/boxes.Backend/RemoveChart", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *backendClient) LoadTable(ctx context.Context, in *TableName, opts ...grpc.CallOption) (*TableCollection, error) {
	out := new(TableCollection)
	err := c.cc.Invoke(ctx, "/boxes.Backend/LoadTable", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *backendClient) UnloadTable(ctx context.Context, in *TableName, opts ...grpc.CallOption) (*TableCollection, error) {
	out := new(TableCollection)
	err := c.cc.Invoke(ctx, "/boxes.Backend/UnloadTable", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// BackendServer is the server API for Backend service.
// All implementations must embed UnimplementedBackendServer
// for forward compatibility
type BackendServer interface {
	// Initialises the backend by loading charts/tables accoring to configuration
	Initialise(context.Context, *ConfigFile) (*Empty, error)
	// Get all charts (actual graph window) contaning all plots (each line/scat/bar-collection), excluding actual values
	GetCharts(context.Context, *Empty) (*ChartCollection, error)
	// Get x/y values for a certain plot
	GetPlotValues(context.Context, *PlotName) (*PlotValues, error)
	// Get information on the loaded plots
	GetLoadedTables(context.Context, *Empty) (*TableCollection, error)
	// Get table schemas available in data engine
	GetAllTableNames(context.Context, *Empty) (*TableNames, error)
	// Get table schemas from data engine
	GetTableSchemas(context.Context, *TableNames) (*TableSchemas, error)
	// Get table contents from loaded table or from one in data engine
	GetTable(context.Context, *TableName) (*Table, error)
	// Add chart (and save this configuration in the yaml config)
	AddChart(context.Context, *ChartInfo) (*Empty, error)
	// Remove chart (and save this configuration in the yaml config)
	RemoveChart(context.Context, *ChartName) (*Empty, error)
	// Load table from data engine (and save this configuration in the yaml config)
	LoadTable(context.Context, *TableName) (*TableCollection, error)
	// Unload table from backend (and save this configuration in the yaml config)
	UnloadTable(context.Context, *TableName) (*TableCollection, error)
	mustEmbedUnimplementedBackendServer()
}

// UnimplementedBackendServer must be embedded to have forward compatible implementations.
type UnimplementedBackendServer struct {
}

func (*UnimplementedBackendServer) Initialise(context.Context, *ConfigFile) (*Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Initialise not implemented")
}
func (*UnimplementedBackendServer) GetCharts(context.Context, *Empty) (*ChartCollection, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetCharts not implemented")
}
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

func RegisterBackendServer(s *grpc.Server, srv BackendServer) {
	s.RegisterService(&_Backend_serviceDesc, srv)
}

func _Backend_Initialise_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ConfigFile)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).Initialise(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/Initialise",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).Initialise(ctx, req.(*ConfigFile))
	}
	return interceptor(ctx, in, info, handler)
}

func _Backend_GetCharts_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).GetCharts(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/GetCharts",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).GetCharts(ctx, req.(*Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _Backend_GetPlotValues_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(PlotName)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).GetPlotValues(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/GetPlotValues",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).GetPlotValues(ctx, req.(*PlotName))
	}
	return interceptor(ctx, in, info, handler)
}

func _Backend_GetLoadedTables_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).GetLoadedTables(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/GetLoadedTables",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).GetLoadedTables(ctx, req.(*Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _Backend_GetAllTableNames_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).GetAllTableNames(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/GetAllTableNames",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).GetAllTableNames(ctx, req.(*Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _Backend_GetTableSchemas_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(TableNames)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).GetTableSchemas(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/GetTableSchemas",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).GetTableSchemas(ctx, req.(*TableNames))
	}
	return interceptor(ctx, in, info, handler)
}

func _Backend_GetTable_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(TableName)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).GetTable(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/GetTable",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).GetTable(ctx, req.(*TableName))
	}
	return interceptor(ctx, in, info, handler)
}

func _Backend_AddChart_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ChartInfo)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).AddChart(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/AddChart",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).AddChart(ctx, req.(*ChartInfo))
	}
	return interceptor(ctx, in, info, handler)
}

func _Backend_RemoveChart_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ChartName)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).RemoveChart(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/RemoveChart",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).RemoveChart(ctx, req.(*ChartName))
	}
	return interceptor(ctx, in, info, handler)
}

func _Backend_LoadTable_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(TableName)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).LoadTable(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/LoadTable",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).LoadTable(ctx, req.(*TableName))
	}
	return interceptor(ctx, in, info, handler)
}

func _Backend_UnloadTable_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(TableName)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BackendServer).UnloadTable(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/boxes.Backend/UnloadTable",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BackendServer).UnloadTable(ctx, req.(*TableName))
	}
	return interceptor(ctx, in, info, handler)
}

var _Backend_serviceDesc = grpc.ServiceDesc{
	ServiceName: "boxes.Backend",
	HandlerType: (*BackendServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Initialise",
			Handler:    _Backend_Initialise_Handler,
		},
		{
			MethodName: "GetCharts",
			Handler:    _Backend_GetCharts_Handler,
		},
		{
			MethodName: "GetPlotValues",
			Handler:    _Backend_GetPlotValues_Handler,
		},
		{
			MethodName: "GetLoadedTables",
			Handler:    _Backend_GetLoadedTables_Handler,
		},
		{
			MethodName: "GetAllTableNames",
			Handler:    _Backend_GetAllTableNames_Handler,
		},
		{
			MethodName: "GetTableSchemas",
			Handler:    _Backend_GetTableSchemas_Handler,
		},
		{
			MethodName: "GetTable",
			Handler:    _Backend_GetTable_Handler,
		},
		{
			MethodName: "AddChart",
			Handler:    _Backend_AddChart_Handler,
		},
		{
			MethodName: "RemoveChart",
			Handler:    _Backend_RemoveChart_Handler,
		},
		{
			MethodName: "LoadTable",
			Handler:    _Backend_LoadTable_Handler,
		},
		{
			MethodName: "UnloadTable",
			Handler:    _Backend_UnloadTable_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "boxes.proto",
}
