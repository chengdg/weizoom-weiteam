# -*- coding: utf-8 -*-

import time
import copy
from datetime import datetime, timedelta

colours = ["#FFB300", "#0379C8", "#8F032C", "#2BF34B", "#8909F5", "#D75F22", "#0379C8", "#8F032C", "#2BF34B", "#8909F5", "#D75F22"]
empty_data_colours = ['#8F8F8F',]

y_value_lambda = lambda item : item['y']

line_chart_option = {
	'title' : {
		'text': ''
	},
	'tooltip' : {
		'trigger': 'axis'
	},
	'toolbox': {
		'show': True,
		'feature': {
			#'dataView' : {'show': True, 'readOnly': True},
			#'magicType' : {'show': True, 'type': ['line', 'bar']},
			'restore' : {'show': True},
			'saveAsImage' : {'show': True}
		}
	},
	'calculable' : True,
	'xAxis' : [
		{
			'type' : 'category',
			'boundaryGap' : False,
			'data' : []
		}
	],
	'yAxis' : [
		{
			'type' : 'value'
		}
	],
	'series' : [
		{
			'name':'',
			'type':'line',
			'smooth':True,
			'itemStyle': {'normal': {'areaStyle': {'type': 'default'}}},
			'data':[]
		}
	]
};

pie_chart_option = {
	'title' : {
		'text': '',
		'x':'center'
	},
	'tooltip' : {
		'trigger': 'item',
		'formatter': "{a} <br/>{b} : {c} ({d}%)"
	},
	'legend': {
		'orient' : 'vertical',
		'x' : 'left',
		'data':[]
	},
	'toolbox': {
		'show': True,
		'feature': {
			'dataView' : {'show': True, 'readOnly': True},
			'restore' : {'show': True},
			'saveAsImage' : {'show': True}
		}
	},
	'calculable' : True,
	'series' : [
		{
			'name':'',
			'type':'pie',
			'radius' : '55%',
			'center': ['50%', '60%'],
			'data': [
			]
		}
	]
};

scatter_chart_option =  {
    "title": {
        "text" : '',
        "subtext" : ''
    },
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": {
            "show": True,
            "type": 'cross',
            "lineStyle": {
                "type": 'dashed',
                "width": 1
            }
        }
    },
    "toolbox": {
        "show": True,
        "feature": {
            "saveAsImage": {"show": True}
        }
    },
    "legend": {
        "data": ['Bug', '需求']
    },
    "xAxis": [
        {
            "type": 'category',
            "data": ['05.26', '05.27', '05.28', '05.29', '05.30', '05.31', '06.01', '06.02', '06.03', '06.04']
        }
    ],
    "yAxis": [
        {
            "type": 'value'
        }
    ],
    "series": [
        {
            "name": 'Bug',
            "type": 'scatter',
            "tooltip": {
                "trigger": 'item',
                "formatter" : """function(params) {
                    return params.seriesName+params.value[2]+':'+ params.value[1]+'天';
                }""",
                "axisPointer":{
                    "show": True
                }
            },
            "symbolSize": 5,
            "itemStyle": {
            	"normal": {
            		"color": '#EF4B3F'
            	}
            },
            "data": [
                ['05.25', 1, 123],
                ['05.26', 2, 123],
                ['05.27', 3, 123],
                ['05.28', 4, 123],
                ['05.29', 5, 123],
                ['05.30', 4, 123],
                ['05.31', 3, 123],
              	['05.31', 5, 123],
                ['06.01', 6, 123],
                ['06.02', 9, 123],
                ['06.03', 7, 123],
                ['06.04', 3, 123]
            ]
        },
        {
            "name": '需求',
            "type": 'scatter',
            "tooltip": {
                "trigger": 'item',
                "formatter" : """function(params) {
                    return params.seriesName+params.value[2]+':'+ params.value[1]+'天';
                }""",
                "axisPointer":{
                    "show": True
                }
            },
            "symbolSize": 5,
            "itemStyle": {
            	"normal": {
            		"color": '#C87800'
            	}
            },
            "data": [
                ['05.31', 8, 123],
              	['05.31', 3, 123],
                ['06.01', 16, 123],
                ['06.02', 19, 123],
                ['06.03', 17, 123],
                ['06.04', 13, 123]
            ]
        }
    ]
}



#===============================================================================
# create_line_chart : 创建line chart
#===============================================================================
def create_line_chart(info):
	x = []
	y = []
	for value in info['values']:
		x.append(value[0])
		y.append(value[1])
	option = line_chart_option
	option['title']['text'] = info['title']
	option['series'][0]['name'] = info['data_name']
	option['xAxis'][0]['data'] = x
	real_y = [y_item for y_item in y if not y_item == None]
	option['series'][0]['data'] = real_y

	return option


#===============================================================================
# create_pie_chart : 创建pic chart
#===============================================================================
def create_pie_chart(info):
	x = []
	y = []
	for value in info['values']:
		x.append(value[0])
		y.append({
			'name': value[0],
			'value': value[1]
		})
	option = pie_chart_option
	option['title']['text'] = info['title']
	option['series'][0]['name'] = info['data_name']
	option['legend']['data'] = x
	option['series'][0]['data'] = y

	return option


#===============================================================================
# create_scatter_chart : 创建scatter chart
#===============================================================================
def create_scatter_chart(info):
	option = scatter_chart_option
	option['title']['text'] = info['title']
	option['title']['subtext'] = info['subtitle']

	x = []
	y = []
	for value in info['values']:
		x.append(value[0])
		y.append({

		})

	option['series'][0]['name'] = info['data_name']
	option['legend']['data'] = x
	option['series'][0]['data'] = y

	return scatter_chart_option









lines_chart_option = {
	'title' : {
		'text': ''
	},
	'tooltip' : {
		'trigger': 'axis'
	},
	'toolbox': {
		'show': True,
		'feature': {
			'dataView' : {'show': True, 'readOnly': True},
			'magicType' : {'show': True, 'type': ['line', 'bar']},
			'restore' : {'show': True},
			'saveAsImage' : {'show': True}
		}
	},
	'calculable' : True,
	'xAxis' : [
		{
			'type' : 'category',
			'boundaryGap' : False,
			'data' : []
		}
	],
	'yAxis' : [
		{
			'type' : 'value'
		}
	],
	'series' : []
};

#===============================================================================
# create_lines_chart : 创建line chart
#===============================================================================
def create_lines_chart(info):
	option = copy.deepcopy(lines_chart_option)
	option['title']['text'] = info['title']

	lines = info['lines']

	#确定x轴
	first_line = lines[0]
	x = []
	for value in first_line['values']:
		x.append(value[0])
	option['xAxis'][0]['data'] = x

	#填充数据
	for line in lines:
		y = []
		for value in line['values']:
			y.append(value[1])
		real_y = [y_item for y_item in y if not y_item == None]
		series = {
			"name": line["data_name"],
			"type": 'line',
			"tooltip": {
				"trigger": 'item',
				"formatter" : "",
				"axisPointer":{
					"show": True
				}
			},
			"smooth": True,
			"data": real_y
		}
		option['series'].append(series)

	return option