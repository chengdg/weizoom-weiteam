Feature: 删除用户
	manager能通过系统来删除用户

@weteam @weteam.manager
Scenario: 删除用户
	manager能删除用户

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
	When manager删除用户'guojing'
	Then manager能获得用户列表
		"""
		[{
			"name": "huangrong",
			"real_name": "黄蓉",
			"email": "huangrong@a.com",
			"thumbnail": "/static/img/huangrong.jpg"
		}]	
		"""
	When manager删除用户'huangrong'
	Then manager能获得用户列表
		"""
		[]	
		"""