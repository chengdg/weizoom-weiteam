/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.projects:ProjectsPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

//var CommentDialog = require('./CommentDialog.react');
var TopNavActions = require('./TopNavActions.react');
var Project = require('./Project.react');

require('./style.css');

var ProjectsPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onClickDelete: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确认删除吗?',
			confirm: _.bind(function() {
				Action.deleteProduct(productId);
			}, this)
		});
	},

	onChangeStore: function(event) {
		this.setState(Store.getData());
	},

	onClickComment: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		var product = this.refs.table.getData(productId);
		Reactman.PageAction.showDialog({
			title: "创建备注", 
			component: CommentDialog, 
			data: {
				product: product
			},
			success: function(inputData, dialogState) {
				var product = inputData.product;
				var comment = dialogState.comment;
				Action.updateProduct(product, 'comment', comment);
			}
		});
	},

	render:function(){
		var cProjectList = this.state.projects.map(function(project, index) {
			return (
				<Project key={index} data={project} />
			)
		});

		return (
		<div className="mt15 xui-project-projectsPage">
			<div className="pt10">
			{cProjectList}
			</div>
		</div>
		)
	}
});

ProjectsPage.topNavActionsComponent = TopNavActions;

module.exports = ProjectsPage;