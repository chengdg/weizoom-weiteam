/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.data:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	updateProduct: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.OUTLINE_DATA_UPDATE_PRODUCT,
			data: {
				property: property,
				value: value
			}
		});
	},

	saveProduct: function(data) {
		var product = {
			name: data['name'],
			weight: data['weight'],
			price: data['price'],
			is_join_promotion: data['isJoinPromotion'],
			promotion_finish_date: data['promotionFinishDate'],
			channels: JSON.stringify(data['channels']),
			models: JSON.stringify(data['models']),
			images: JSON.stringify(data['images']),
			documents: JSON.stringify(data['documents']),
			detail: data['detail']
		};

		if (data.id === -1) {
			Resource.put({
				resource: 'outline.data',
				data: product,
				dispatch: {
					dispatcher: Dispatcher,
					actionType: Constant.OUTLINE_DATA_SAVE_PRODUCT
				}
			});
		} else {
			product['id'] = data.id;
			Resource.post({
				resource: 'outline.data',
				data: product,
				dispatch: {
					dispatcher: Dispatcher,
					actionType: Constant.OUTLINE_DATA_SAVE_PRODUCT
				}
			});
		}		
	}
};

module.exports = Action;