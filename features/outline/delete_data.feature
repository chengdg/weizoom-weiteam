Feature: 删除商品
	Jobs能通过统计系统来删除商品

@outline @outline.data
Scenario: 删除商品
	jobs能删除自己创建的商品，但不能删除tom创建的商品

	Given jobs登录管理系统
	Given tom登录管理系统
	When tom添加商品
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
			"name": "红烧肉",
			"price": 30.0
		}, {
			"name": "水晶虾仁",
			"price": 12.34
		}]	
		"""
	When jobs删除商品'红烧肉'
	Then jobs能获得商品列表
		"""
		[{
			"name": "水晶虾仁",
			"price": 12.34
		}]	
		"""
	When jobs删除商品'水晶虾仁'
	Then jobs能获得商品列表
		"""
		[]	
		"""
	Given tom登录管理系统
	Then jobs能获得商品列表
		"""
		[{
			"name": "红烧肉",
			"price": 11.1
		}]	
		"""