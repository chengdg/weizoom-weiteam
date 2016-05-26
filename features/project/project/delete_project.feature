Feature: 删除Project
	Yangmi能通过系统删除"Project"


@weteam @weteam.project @wip
Scenario: 删除Project
	yangmi添加多个project后，删除其中一个
	1. project列表顺序不受影响
	2. yangmi其他project不受影响
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
		}, {
			"name": "Project3",
			"description": "yangmi project3 description"
		}]
		"""
	Given zhouxun登录系统
	When zhouxun添加Project
		"""
		[{
			"name": "Project2",
			"description": "zhouxun project2 description"
		}]
		"""
	Given yangmi登录系统
	When yangmi删除Project"Project2"
	Then yangmi能获得Project列表
		"""
		[{
			"name": "Project3",
			"description": "yangmi project3 description"
		}, {
			"name": "Project1",
			"description": "yangmi project1 description"
		}]
		"""
	Given zhouxun登录系统
	Then zhouxun能获得Project列表
		"""
		[{
			"name": "Project2",
			"description": "zhouxun project2 description"
		}]
		"""