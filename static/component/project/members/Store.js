/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.members:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleAddMembers': Constant.PROJECT_MEMBERS_ADD_MEMBERS,
		'handleDeleteMember': Constant.PROJECT_MEMBERS_DELETE_MEMBER
	},

	init: function() {
		this.data = {
			"members": Reactman.loadJSON('members') || [],
			"projectId": Reactman.loadJSON('projectId')
		};
	},

	handleAddMembers: function(action) {
		this.__emitChange();
	},

	handleDeleteMember: function(action) {
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;