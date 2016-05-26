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
var ProjectDialog = require('./ProjectDialog.react');


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
		var project = this.props.data;
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确认删除吗?',
			confirm: _.bind(function() {
				Action.deleteProject(project.id);
			}, this)
		});
		event.stopPropagation();
	},

	onClickEdit: function(event) {
		var project = this.props.data;
		Reactman.PageAction.showDialog({
			title: "更改团队信息", 
			component: ProjectDialog, 
			data: {
				project: project
			},
			success: function(inputData, dialogState) {
				var product = inputData.product;
				Action.updateProject(product, dialogState.changed);
			}
		});
		event.stopPropagation();
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
						<button className="btn btn-default btn-xs mr5" onClick={this.onClickEdit}><span className="glyphicon glyphicon-pencil"></span></button>
						<button className="btn btn-default btn-xs" onClick={this.onClickDelete}><span className="glyphicon glyphicon-remove"></span></button>
					</span>
					{project.createdAt}创建
				</div>
			</div>
		</div>
		)
	}
});

module.exports = Project;