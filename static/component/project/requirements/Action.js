/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	deleteProduct: function(id) {
		Resource.delete({
			resource: 'outline.data',
			data: {
				id: id
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.OUTLINE_DATAS_UPDATE_PRODUCT
			}
		});
	},

	filterProducts: function(filterOptions) {
		Dispatcher.dispatch({
			actionType: Constant.OUTLINE_DATAS_FILTER_PRODUCTS,
			data: filterOptions
		});
	},

	updateProduct: function(product, field, data) {
		Dispatcher.dispatch({
			actionType: Constant.OUTLINE_DATAS_UPDATE_PRODUCT,
			data: {
				product: product,
				field: field,
				data: data
			}
		});
	}
};

module.exports = Action;