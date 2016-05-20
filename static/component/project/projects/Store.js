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
		'handleDeleteProduct': Constant.PROJECT_PROJECTS_DELETE_PROJECT,
		'handleStarProduct': Constant.PROJECT_PROJECTS_STAR_PROJECT
	},

	init: function() {
		var projects = Reactman.loadJSON('projects');
		if (projects) {
			this.data = {
				projects: projects
			};
		} else {
			this.data = {};
		}
	},

	handleDeleteProduct: function(action) {
		this.__emitChange();
	},

	handleStarProduct: function(action) {
		debug(action);
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;