/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleDeleteProject': Constant.PROJECT_PROJECTS_DELETE_PROJECT,
		'handleStarProject': Constant.PROJECT_PROJECTS_STAR_PROJECT,
		'handleUnStarProject': Constant.PROJECT_PROJECTS_UNSTAR_PROJECT
	},

	init: function() {
		var projects = Reactman.loadJSON('projects');
		if (projects) {
			this.data = {
				projects: this.__sortProject(projects)
			};
		} else {
			this.data = {};
		}
	},

	__getProject: function(id) {
		return _.find(this.data.projects, function(project) {
			return project.id === id;
		});
	},

	__sortProject: function(projects) {
		return _.sortBy(projects, function(project) {
			var index = 0;
			if (project.isStaredByUser) {
				index += 1000000;
			}

			index += project.id;

			return 0 - index;
		})
	},

	handleDeleteProject: function(action) {
		this.__emitChange();
	},

	handleStarProject: function(action) {
		var project = this.__getProject(action.data.projectId);
		project.isStaredByUser = true;
		//this.data.projects = this.__sortProject(this.data.projects);
		this.__emitChange();
	},

	handleUnStarProject: function(action) {
		var project = this.__getProject(action.data.projectId);
		project.isStaredByUser = false;
		//this.data.projects = this.__sortProject(this.data.projects);
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;