/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.data::Store');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');
var window = window;

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateProduct': Constant.OUTLINE_DATA_UPDATE_PRODUCT,
		'handleSaveProduct': Constant.OUTLINE_DATA_SAVE_PRODUCT
	},

	init: function() {
		this.data = {};
		this.data['projectId'] = Reactman.loadJSON('projectId');
		this.data['iteration'] = {
			id: 1,
			stages: [{
				id: 1,
				name: 'TODO',
				isBufferStage: false,
				wipCount: 8,
				wipContainer: '',
				tasks: []
			}, {
				id: 2,
				name: '设计',
				isBufferStage: false,
				wipCount: 3,
				wipContainer: '',
				tasks: []
			}, {
				id: 3,
				name: '待开发',
				isBufferStage: true,
				wipCount: 0,
				wipContainer: '设计',
				tasks: []
			}, {
				id: 11,
				name: 'TODO',
				isBufferStage: false,
				wipCount: 8,
				wipContainer: '',
				tasks: []
			}, {
				id: 12,
				name: '设计',
				isBufferStage: false,
				wipCount: 3,
				wipContainer: '',
				tasks: []
			}, {
				id: 13,
				name: '待开发',
				isBufferStage: true,
				wipCount: 0,
				wipContainer: '设计',
				tasks: []
			}]
		}
	},

	handleUpdateProduct: function(action) {
		debug('update %s to %s', action.data.property, JSON.stringify(action.data.value));
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},

	handleSaveProduct: function() {
		Reactman.W.gotoPage('/outline/datas/');
	},

	getData: function() {
		return this.data;
	}
});

module.exports = Store;