Feature: 添加Project
	Yangmi能通过系统添加"Project"

@weteam @weteam.project
Scenario: 首次登录后，Project列表为空
	Yangmi登录系统后，查看project列表为空
	
	Given yangmi登录系统
	Then yangmi能获得Project列表
		"""
		[]
		"""

@weteam @weteam.project
Scenario: 添加Project
	yangmi添加多个project后
	1. yangmi能获得project
	2. project列表按添加顺序倒序排列
	3. yangmi添加的project不影响zhouxun
	
	Given yangmi登录系统
	When yangmi添加Project
		"""
		[{
			"name": "Project1",
			"description": "project1 description"
		}, {
			"name": "Project2",
			"description": "project2 description"
		}]
		"""
	Then yangmi能获得Project列表
		"""
		[{
			"name": "Project2",
			"description": "project2 description"
		}, {
			"name": "Project1",
			"description": "project1 description"
		}]
		"""
	Then yangmi能获得Project"Project1"
		"""
		{
			"name": "Project1",
			"description": "project1 description"
		}
		"""
	Then yangmi能获得Project"Project2"
		"""
		{
			"name": "Project2",
			"description": "project2 description"
		}
		"""
	Given zhouxun登录系统
	Then zhouxun能获得Project列表
		"""
		[]
		"""