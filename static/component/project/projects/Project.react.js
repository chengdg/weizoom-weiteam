/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.projects:Project');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');
var classNames = require('classnames');

var Reactman = require('reactman');

var Action = require('./Action');


var Project = React.createClass({
	componentDidMount: function() {
		var $project = $(ReactDOM.findDOMNode(this));
		var $actionBar = $project.find('.xa-actionBar').eq(0);
		$project.mouseenter(function() {
			$actionBar.removeClass('xui-invisible');
		}).mouseleave(function() {
			$actionBar.addClass('xui-invisible');
		});
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

	onClickEdit: function(event) {
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

	onClickStar: function(event) {
		var project = this.props.data;
		var isStared = project.isStaredByUser;
		if (!isStared) {
			Action.starProject(project);
		} else {
			Action.unstarProject(project);
		}
	},

	onClickProject: function(event) {
		var projectId = event.currentTarget.getAttribute('data-id');
		Action.gotoKanban(projectId);
	},

	render:function(){
		var project = this.props.data;

		var starClasses = classNames("fr", "fa", "fa-2x", "mt10", project.isStaredByUser ? "fa-star xui-i-stared" : "fa-star-o xui-i-notStared");
		return (
		<div className="xui-project mt20 xa-project" data-id={project.id} onClick={this.onClickProject}>
			<div className="xui-i-title clearfix">
				<h3 className="fl">
					{project.name}
				</h3>
				
				<i className={starClasses} onClick={this.onClickStar}></i>
				
			</div>
			<div className="xui-i-info">
				<div>{project.description}</div>
				<div className="xui-i-bottomBar">
					<span className="mr10 xui-invisible xa-actionBar">
						<button className="btn btn-default btn-xs mr5"><span className="glyphicon glyphicon-pencil"></span></button>
						<button className="btn btn-default btn-xs"><span className="glyphicon glyphicon-remove"></span></button>
					</span>
					{project.createdAt}创建
				</div>
			</div>
		</div>
		)
	}
});

module.exports = Project;