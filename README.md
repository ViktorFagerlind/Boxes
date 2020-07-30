# Boxes
## Prerequisites
* Use OS X

### Consul installation
* Download consul: https://www.hashicorp.com/products/consul/
* Install consul
* run consul
  > cd /consul <br>
  > consul agent -dev -ui -datacenter zone1 -node host1 -config-dir ./consul.d/
* Monitor consul at http://localhost:8500/ui

https://thenewstack.io/implementing-service-discovery-of-microservices-with-consul/

### C++ installation
* Install gRPC according to https://grpc.io/docs/quickstart/cpp/. Use MY_INSTALL_DIR=~/.grpc
* clone this git repo

### Python installation
* Create python 3.7 virtual environment
  > conda create -n python37 python=3.7
* Activate environment
  > conda activate python37
* Install gRPC
  > python -m pip install grpcio <br>
  > python -m pip install grpcio-tools
  
### JavaScript installation
* Download and install Node.js from https://nodejs.org/en/download/
* Download and install Yarn package manager from: https://classic.yarnpkg.com/en/docs/install/

### Swift installation
* Install Xcode
* Open up Boxes.xcworkspace
* protoc -I ../protos/ --grpc-swift_out=. ../protos/boxes.proto
* protoc -I ../protos/ --swift_out=. ../protos/boxes.proto

### Go installation
* Install go according to https://golang.org/doc/install
* Install grpc for go according to https://grpc.io/docs/languages/go/quickstart/
* Install protoc-gen-go-grpc as well
  > google.golang.org/grpc/cmd/protoc-gen-go-grpc
* Add /usr/local/go/bin and $HOME/go/bin to your path
* go get gopkg.in/yaml.v2

## Build C++ programs
* Go to /cpp folder
* Create build dir
  > mkdir -p cmake/build
* Go to build dir 
  > cd cmake/build
* Create makefile
  > cmake -DCMAKE_PREFIX_PATH=~/.grpc ../..
* Build programs
  > make -j

## Run go backend (temp / TODO)
* go to go/backend/proto
  > protoc -I ../../protos/ --go_out=. --go-grpc_out=. --go_opt=paths=source_relative --go-grpc_opt=paths=source_relative ../../protos/boxes.proto

## Prepare Python program
* Generate Python RPC definitions
  > python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/boxes.proto

## Test data engine
Open up terminals and run the following
1. consul according to above
1. csv_connector_service
1. garmin_connector_sevice
1. data_engine_service
1. test_data_engine.py -p<br>
Run SQL queries from the prompt, examples in Queries.sql

## Build Electron (GUI) program
* Open a terminal and browse to the 'js' folder in this project.
* Install Node package dependencies:
  > yarn install
* Build and start the application:
  > yarn start

## Demo Architecure
See demo_architecture.png

## Nice links
* http://flagzeta.org/blog/a-python-microservice-stack/
* https://levelup.gitconnected.com/swift-grpc-577ce1a4d1b7
