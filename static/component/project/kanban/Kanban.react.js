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

var KanbanColumn = require('./KanbanColumn.react');

var Kanban = React.createClass({
	getInitialState: function() {
		return null;
	},

	componentDidMount: function() {
		var $window = $(window);
		var height = $window.height() - 100;

		var $kanban = $(ReactDOM.findDOMNode(this));
		$kanban.height(height);

		// var width = 260 * this.props.stages.length + 50; //每个stage宽度为260
		// $kanban.width(width);
	},

	render:function(){
		var stages = this.props.stages;
		var cStages = stages.map(function(stage) {
			return (
				<KanbanColumn stage={stage} key={stage.id} />
			)
		})
		
		return (
		<div className="xui-kanbanContainer">
			<div className="xui-kanban clearfix">
				{cStages}
			</div>
		</div>
		)
	}
})
module.exports = Kanban;