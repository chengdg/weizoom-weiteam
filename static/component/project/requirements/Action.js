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
	deleteRequirement: function(requirementId) {
		Resource.delete({
			resource: 'project.requirement',
			data: {
				id: requirementId
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.OUTLINE_DATAS_UPDATE_PRODUCT
			}
		});
	},

	filterRequirements: function(filterOptions) {
		Dispatcher.dispatch({
			actionType: Constant.OUTLINE_DATAS_FILTER_PRODUCTS,
			data: filterOptions
		});
	}
};

module.exports = Action;