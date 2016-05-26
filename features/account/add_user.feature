Feature: 添加用户
	manager能通过系统添加用户

@weteam @weteam.manager
Scenario: 添加用户
	manager能获得添加的用户的列表

	Given manager登录系统
	When manager添加用户
		"""
		[{
			"name": "guojing",
			"real_name": "郭靖",
			"email": "guojing@a.com"
		}, {
			"name": "huangrong",
			"real_name": "黄蓉",
			"email": "huangrong@a.com",
			"thumbnail": "/static/img/huangrong.jpg"
		}]	
		"""
	Then manager能获得用户列表
		"""
		[{
			"name": "huangrong",
			"real_name": "黄蓉",
			"email": "huangrong@a.com",
			"thumbnail": "/static/img/huangrong.jpg"
		}, {
			"name": "guojing",
			"real_name": "郭靖",
			"email": "guojing@a.com"
		}]	
		"""