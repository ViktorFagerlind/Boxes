package backend

import (
	"io/ioutil"
	"log"

	"gopkg.in/yaml.v2"
)

type Configuration struct {
	Tables []TableCfg
	Charts []ChartCfg
}

type TableCfg struct {
	Name    string
	Query   string
	Columns []ColumnCfg
}

type ColumnCfg struct {
	Name string
	Type string
}

type ChartCfg struct {
	Name     string
	Category string
	Plots    []PlotCfg
}

type PlotCfg struct {
	Table   string
	Kind    string
	Xcolumn string `yaml:"x-column"`
	Ycolumn string `yaml:"y-column"`
	Color   string
	Circles bool
	Filled  bool
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
