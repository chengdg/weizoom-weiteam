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