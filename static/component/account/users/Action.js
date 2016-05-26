/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:account.users:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	deleteUser: function(id) {
		Resource.delete({
			resource: 'account.user',
			data: {
				id: id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.ACCOUNT_USERS_DELETE_USER,
				data: {
					id: id
				}
			}
		});
	},

	updateUser: function(user, changed) {
		Dispatcher.dispatch({
			actionType: Constant.ACCOUNT_USERS_UPDATE_USER,
			data: {
				user: user,
				changed: changed
			}
		});
	},

	addUser: function(user) {
		Dispatcher.dispatch({
			actionType: Constant.ACCOUNT_USERS_ADD_USER,
			data: {
				user: user
			}
		});
	}
};

module.exports = Action;