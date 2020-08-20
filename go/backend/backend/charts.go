package backend

import (
	pb "boxes/backend/protos"
	"sync"
)

type ChartsManager struct {
	chartCfgs []ChartCfg
}

var chartsManagerSingleton *ChartsManager
var chartsManagerOnce sync.Once

func GetChartsManager() *ChartsManager {
	chartsManagerOnce.Do(func() {
		chartsManagerSingleton = &ChartsManager{}
	})
	return chartsManagerSingleton
}

func (this *ChartsManager) Initialise(chartCfgs []ChartCfg) {
	this.chartCfgs = chartCfgs
}

func (this *ChartsManager) GetCharts() (*pb.ChartCollection, error) {
	/*
		for _, chartCfg := range this.chartCfgs {
			for _, plotCfg := range chartCfg.Plots {
				colorUint, _ := strconv.ParseUint(plotCfg.Color, 16, 32)

				TODO...

				pbPlot := &pb.Plot{Name: plotCfg.Table + "-" + plotCfg.Ycolumn,
					Kind:    plotCfg.Kind,
					Color:   uint32(colorUint),
					Filled:  plotCfg.Filled,
					Circles: plotCfg.Circles}
			}
		}
	*/
	return nil, nil
}
