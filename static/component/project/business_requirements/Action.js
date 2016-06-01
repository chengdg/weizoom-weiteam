/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.requirements:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	deleteRequirement: function(projectId, requirementId) {
		Resource.delete({
			resource: 'project.business_requirement',
			data: {
				project_id: projectId,
				requirement_id: requirementId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PROJECT_REQUIREMENTS_DELETE_REQUIREMENT
			}
		});
	},

	pullToKanban: function(requirement) {
		debug(requirement);
		if (requirement.storyPoint === 0) {
			Reactman.PageAction.showHint('error', '请先设置任务的故事点');
			return;
		}

		Resource.put({
			resource: 'project.kanban_task',
			data: {
				id: requirement.id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.PROJECT_REQUIREMENTS_PULLTO_KANBAN
			}
		});
	},

	filterRequirements: function(filterOptions) {
		Dispatcher.dispatch({
			actionType: Constant.PROJECT_REQUIREMENTS_FILTER_REQUIREMENTS,
			data: filterOptions
		});
	},

	updateRequirementInServer: function(projectId, requirement, property, value) {
		Resource.post({
			resource: 'project.business_requirement',
			data: {
				project_id: projectId,
				requirement_id: requirement.id,
				field: property,
				value: value
			},
			success: function(data) {
				Reactman.PageAction.showHint('success', '更新需求成功');
			},
			error: function(resp) {
				Reactman.PageAction.showHint('error', resp.errMsg);
			}
		});
	},

	updateRequirement: function(requirement, newRequirement) {
		Dispatcher.dispatch({
			actionType: Constant.PROJECT_REQUIREMENTS_UPDATE_REQUIREMENT,
			data: newRequirement
		});
	}
};

module.exports = Action;