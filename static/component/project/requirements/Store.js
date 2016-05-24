/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.requirements:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateRequirement': Constant.PROJECT_REQUIREMENTS_UPDATE_REQUIREMENT,
		'handleFilterRequirements': Constant.PROJECT_REQUIREMENTS_FILTER_REQUIREMENTS,
	},

	init: function() {
		this.data = {
			projectId: Reactman.loadJSON('projectId')
		};
	},

	handleUpdateRequirement: function(action) {
		this.__emitChange();
	},

	handleFilterRequirements: function(action) {
		this.data.filterOptions = action.data;
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;