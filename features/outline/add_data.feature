Feature: 添加商品
	Jobs能通过统计系统来添加商品

@outline @outline.data
Scenario: 创建不带规格的商品
	jobs能获得自己创建的商品列表，但不能获得tom创建的商品列表

	Given tom登录管理系统
	When tom添加商品
		"""
		[{
			"name": "红烧肉",
			"price": 11.1
		}]	
		"""
	Then tom能获得商品列表
		"""
		[{
			"name": "红烧肉",
			"price": 11.1
		}]	
		"""
	Given jobs登录管理系统
	When jobs添加商品
		"""
		[{
			"name": "东坡肘子",
			"price": 30.0
		}, {
			"name": "水晶虾仁",
			"price": 12.34
		}]	
		"""
	Then jobs能获得商品列表
		"""
		[{
			"name": "水晶虾仁",
			"price": 12.34
		}, {
			"name": "东坡肘子",
			"price": 30.0
		}]	
		"""


@outline @outline.data	
Scenario: 创建带规格的商品
	jobs能创建带规格的商品
	
	Given jobs登录管理系统
	When jobs添加商品
		"""
		[{
			"name": "东坡肘子",
			"price": 30.0,
			"models": [{
				"name": "大",
				"stocks": 1
			}, {
				"name": "小",
				"stocks": 2
			}]
		}, {
			"name": "水晶虾仁",
			"price": 12.34,
			"models": [{
				"name": "S",
				"stocks": 9
			}]
		}]	
		"""
	Then jobs能获得商品列表
		"""
		[{
			"name": "水晶虾仁",
			"price": 12.34,
			"models": [{
				"name": "S",
				"stocks": 9
			}]
		}, {
			"name": "东坡肘子",
			"price": 30.0,
			"models": [{
				"name": "大",
				"stocks": 1
			}, {
				"name": "小",
				"stocks": 2
			}]
		}]	
		"""