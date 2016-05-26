Feature: 更新Project
	Yangmi能通过系统更改"Project"


@weteam @weteam.project
Scenario: 更新Project
	yangmi添加多个project后，更新其中一个
	1. yangmi能获得更新后的project
	2. project列表顺序不受影响
	3. yangmi其他project不受影响
	3. zhouxun的同名project不受影响
	
	Given yangmi登录系统
	When yangmi添加Project
		"""
		[{
			"name": "Project1",
			"description": "yangmi project1 description"
		}, {
			"name": "Project2",
			"description": "yangmi project2 description"
		}]
		"""
	Given zhouxun登录系统
	When zhouxun添加Project
		"""
		[{
			"name": "Project1",
			"description": "zhouxun project1 description"
		}]
		"""
	Given yangmi登录系统
	When yangmi更新Project"Project1"
		"""
		{
			"name": "Project1*",
			"description": "yangmi project1* description"
		}
		"""
	Then yangmi能获得Project列表
		"""
		[{
			"name": "Project2",
			"description": "yangmi project2 description"
		}, {
			"name": "Project1*",
			"description": "yangmi project1* description"
		}]
		"""
	Then yangmi能获得Project"Project1*"
		"""
		{
			"name": "Project1*",
			"description": "yangmi project1* description"
		}
		"""
	Then yangmi能获得Project"Project2"
		"""
		{
			"name": "Project2",
			"description": "yangmi project2 description"
		}
		"""
	Given zhouxun登录系统
	Then zhouxun能获得Project列表
		"""
		[{
			"name": "Project1",
			"description": "zhouxun project1 description"
		}]
		"""