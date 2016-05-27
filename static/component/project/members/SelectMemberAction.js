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
	getCandidateMembers: function(projectId) {
		Resource.get({
			resource: 'project.candidate_members',
			data: {
				project_id: projectId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PROJECT_MEMBERS_GET_CANDIDATE_MEMBERS
			}
		});
	}
};

module.exports = Action;