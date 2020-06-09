'use strict'
export module Internals
{
    const grpc = require('grpc');
    const protoLoader = require('@grpc/proto-loader');

    interface IDataEngine {
        GetPlotData(tableName: string, onSuccess: (response: any) => void): void;
    }

    export class DummyDataEngine implements IDataEngine {
        
        public readonly server: string;
        
        constructor (server: string) {
            this.server = server;
        }

        public GetPlotData(tableName: string, onSuccess: (response: any) => void)
        {
            let response = { value: 10 };
            onSuccess(response);
        }
    }

    export class DataEngine implements IDataEngine {
        
        private readonly dataEngineService: any;

        public readonly server: string;

        constructor(server: string)
        {
            this.server = server;

            let protoPath = `${__dirname}/../../protos/table.proto`;
            let packageDefinition = protoLoader.loadSync(
                protoPath,
                {keepCase: true,
                 longs: String,
                 enums: String,
                 defaults: true,
                 oneofs: true
                });
            
            let protoPackage = grpc.loadPackageDefinition(packageDefinition).tableservices;
            this.dataEngineService = new protoPackage.DataEngine(this.server, grpc.credentials.createInsecure());
        }

        public GetPlotData(tableName: string, onSuccess: (response: any) => void)
        {
            let responseHandler = (error: any, response: any) => {

                if (error)
                {
                    console.log(`An error occured when getting plot data for table '${tableName}':\n`, error);
                    return;
                }

                console.log(`Successfully recieved data for table '${tableName}'`);
                onSuccess(response);
            }

            this.dataEngineService.GetPlotData({ name: tableName }, responseHandler);
        }
    }
}