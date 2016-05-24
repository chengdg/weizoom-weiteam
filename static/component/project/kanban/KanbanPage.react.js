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
var KanbanHeader = require('./KanbanHeader.react');
var Kanban = require('./Kanban.react');

require('./style.css');

var KanbanPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function() {
		this.setState(Store.getData());
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	onSubmit: function() {
		Action.saveProduct(Store.getData());
	},

	componentDidMount: function() {
		$('body').css('overflow-y', 'hidden');
		
		var $window = $(window);
		var height = $window.height() - 50;

		var $page = $(ReactDOM.findDOMNode(this));
		$page.height(height);

		var iteration = this.state.iteration;
		var windowWidth = $window.width();
		var width = 260 * iteration.stages.length + 100; //每个stage宽度为260
		if (width > windowWidth) {
			$page.width(width);
		}
		
	},

	render:function(){
		return (
		<div className="xui-project-kanbanPage xui-formPage">
			<KanbanHeader projectId={this.state.projectId} iteration={this.state.iteration}/>
			<Kanban stages={this.state.iteration.stages} />
		</div>
		)
	}
})
module.exports = KanbanPage;