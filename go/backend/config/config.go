package config

import (
	"log"
	"io/ioutil"
	"gopkg.in/yaml.v2"
)


type Configuration struct {
	Tables []Table
  Charts []Chart
}

type Table struct {
	Name 		string
	Query 	string
	Columns []Column
}

type Column struct {
	Name string
	Type string
}

type Chart struct {
	Name 			string
	Category 	string
	Plots     []Plot
}

type Plot struct {
	Table 		string
	Kind  		string
	X_column	string `yaml:"x-column"`
	Y_column	string `yaml:"y-column"`
	Color			string
	Circles		bool
	Filled		bool
}


func LoadConfiguration(yamlPath string) (*Configuration, error) {
	yamlFile, err := ioutil.ReadFile(yamlPath)

  if err != nil {
  	log.Printf("yamlFile.Get err   #%v ", err)
  	return nil, err
  }

  config := Configuration{}
    
  err = yaml.Unmarshal(yamlFile, &config)
  if err != nil {
  	log.Fatalf("error: %v", err)
  	return nil, err
  }
  /*log.Printf("--- Values:\n%v\n\n", config)


  march, err := yaml.Marshal(&config)
	if err != nil {
		log.Fatalf("error: %v", err)
		return nil, err
	}
	log.Printf("--- Dump:\n%s\n\n", string(march))
	*/

  return &config, nil
}
