/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.members:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	deleteMember: function(projectId, memberId) {
		Resource.delete({
			resource: 'project.member',
			data: {
				project_id: projectId,
				member_id: memberId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PROJECT_MEMBERS_DELETE_MEMBER
			}
		});
	},

	addMembers: function(projectId, userIds) {
		Resource.put({
			resource: 'project.member',
			data: {
				project_id: projectId,
				user_ids: JSON.stringify(userIds)
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PROJECT_MEMBERS_ADD_MEMBERS
			}
		});
	}
};

module.exports = Action;