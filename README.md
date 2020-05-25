# Boxes
## Prerequisites
* Use OS X

### C++ installation
* Install gRPC according to https://grpc.io/docs/quickstart/cpp/. Use MY_INSTALL_DIR=~/.grpc
* clone this git repo

### Python installation
* Create python 3.7 virtual environment
  > conda create -n python37 python=3.7
* Activate environment
  > conda activate python37
* Install gRPC
  > python -m pip install grpcio
  > python -m pip install grpcio-tools

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

## Demo Architecure
See demo_architecture.png
