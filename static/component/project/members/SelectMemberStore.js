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
		'handleGetCandidateMembers': Constant.PROJECT_MEMBERS_GET_CANDIDATE_MEMBERS
	},

	init: function() {
		this.data = {
			selectedMembers: [],
			members: []
		};
	},

	handleGetCandidateMembers: function(action) {
		this.data.members = action.data.members.map(function(member) {
			return {
				text: member.name,
				value: member.id
			}
		});
		this.__emitChange();
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;