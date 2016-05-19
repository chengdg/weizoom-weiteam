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
		this.data = Reactman.loadJSON('product');
		if (this.data) {
			this.data['isJoinPromotion'] = this.data['is_join_promotion'] ? '1' : '0';
			this.data['promotionFinishDate'] = this.data['promotion_finish_date'];
			this.data['channels'] = JSON.parse(this.data['channels']);
		} else {
			this.data = {
				'id':-1, 
				'isJoinPromotion':'0', 
				'promotionFinishDate': '',
				'channels': [],
				'models': [],
				'images': [],
				'detail': '',
				'documents': []
			};
		}
		debug(this.data);
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