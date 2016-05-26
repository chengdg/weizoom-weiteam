/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:account.users:Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleAddUser': Constant.ACCOUNT_USERS_ADD_USER,
		'handleUpdateUser': Constant.ACCOUNT_USERS_UPDATE_USER,
		'handleDeleteUser': Constant.ACCOUNT_USERS_DELETE_USER
	},

	init: function() {
		this.data = {
			"users": Reactman.loadJSON('users') || []
		};
	},

	handleAddUser: function(action) {
		var user = action.data.user;
		this.data.users.splice(0, 0, user);
		this.__emitChange();
	},

	handleUpdateUser: function(action) {
		var targetUser = action.data.user;
		var user = _.find(this.data.users, function(user) {
			return user.id === targetUser.id;
		});

		_.each(action.data.changed, function(value, key) {
			user[key] = value;
		});

		this.__emitChange();
	},

	handleDeleteUser: function(action) {
		var targetUserId = parseInt(action.data.id);
		this.data.users = _.filter(this.data.users, function(user) {
			return user.id !== targetUserId;
		});
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;