# Boxes
## Prerequisites
* Use OS X

### Consul installation
* Download consul: https://www.hashicorp.com/products/consul/
* Install consul
* run consul
  > consul agent -dev -ui -datacenter zone1 -node host1
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
  > python -m pip install grpcio<br>
  > python -m pip install grpcio-tools
  
### JavaScript installation
* Download and install Node.js from https://nodejs.org/en/download/
* Download and install Yarn package manager from: https://classic.yarnpkg.com/en/docs/install/

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

## Prepare Python program
* Generate Python RPC definitions
  > python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/table.proto

## Run C++ together with Python
* Open up two terminals and go to /cpp/ and /python/ respectively
* start the servers; algorithm_server and csv_connector_server.py
* run data_engine.py 

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
