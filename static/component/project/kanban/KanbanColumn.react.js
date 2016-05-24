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

var KanbanColumn = React.createClass({
	getInitialState: function() {
		return null;
	},

	componentDidMount: function() {
		var $window = $(window);
		var height = $window.height() - 135;

		var $kanban = $(ReactDOM.findDOMNode(this));
		$kanban.height(height);
	},

	render:function(){
		var stage = this.props.stage;
		var tasks = stage.tasks;
		debug(tasks);
		debug(tasks.length);

		var wipCount = stage.wipCount === 0 ? stage.wipContainer : stage.wipCount;

		var cTasks = '';

		return (
		<div className="xui-kanban-column xa-kanban-column">
			<div className="xui-i-header clearfix">
				<div className="fl"><span className="xa-columnTitle">{stage.name}</span> · (<span className="xa-taskCount">{tasks.length}</span>/<span className="xa-wipCount">{wipCount}</span>)</div>
				<div className="dropdown fr mr10">
					<button className="btn btn-default btn-xs dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown">
						<span className="caret"></span>
					</button>
					<ul className="dropdown-menu">
						<li><a href="javascript:void(0);" className="xa-modifyColumn"><span className="glyphicon glyphicon-pencil"></span> 修改列</a></li>
						<li><a href="javascript:void(0);" className="xa-deleteColumn"><span className="glyphicon glyphicon-remove"></span> 删除列</a></li>
					</ul>
				</div>
			</div>
			<div className="xui-i-taskContainer">
				{cTasks}
			</div>
		</div>
		)
	}
})
module.exports = KanbanColumn;