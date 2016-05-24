/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.kanban:KanbanPage');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

//var ProductModelList = require('./ProductModelList.react');
var Store = require('./Store');
var Action = require('./Action');

var KanbanHeader = React.createClass({
	getInitialState: function() {
		return null;
	},

	renderActionList: function(iteration) {
		if (iteration.id == -1) {
			return (
				<ul className="xa-actionMenu dropdown-menu" role="menu" aria-labelledby="actionDropdown">
					<li><a href="javascript:void(0);" className="xa-createIteration">创建迭代</a></li>
				</ul>
			)
		} else {
			return (
				<ul className="xa-actionMenu dropdown-menu" role="menu" aria-labelledby="actionDropdown">
					<li><a href="javascript:void(0);" className="xa-createBug">创建Bug</a></li>
				</ul>
			)
		}
	},

	render:function(){
		var iteration = this.props.iteration;
		var projectId = this.props.projectId;

		var cActionList = this.renderActionList(iteration);
		return (
		<div className="xui-kanbanHeader clearfix">
			<div className="fl">看板(Kanban)</div>

			<div className="dropdown fl ml20">
				<button className="btn btn-default dropdown-toggle" type="button" id="actionDropdown" data-toggle="dropdown">
					操作
					<span className="caret"></span>
				</button>
				{cActionList}
			</div>

			<div className="dropdown fl ml20">
				<button className="btn btn-default dropdown-toggle" type="button" id="userDropdown" data-toggle="dropdown">
					<span className="xa-userDropdownTitle">过滤成员</span>
					<span className="caret"></span>
				</button>
				<ul className="xa-userMenu dropdown-menu" role="menu" aria-labelledby="userDropdown">
				</ul>
			</div>

			<div className="fl ml20">
				<a href={"/project/iteration_tasks/?project_id"+projectId+"&iteration_id="+iteration.id} target="_blank">
					<button className="btn btn-default xa-showIterationTasks"><span className="glyphicon glyphicon-list-alt"></span> 全部需求</button>
				</a>
			</div>

			<div className="fl ml20">
				<button className="btn btn-primary xa-showAllTask xui-hide">显示全部任务</button>
			</div>
		</div>
		)
	}
})
module.exports = KanbanHeader;