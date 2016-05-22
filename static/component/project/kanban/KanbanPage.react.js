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

var KanbanPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function() {
		this.setState(Store.getData());
	},

	onChange: function(value, event) {
		debug(value);
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	onSubmit: function() {
		Action.saveProduct(Store.getData());
	},

	componentDidMount: function() {
		debug(ReactDOM.findDOMNode(this.refs.name));
	},

	render:function(){
		return (
		<div className="xui-project-kanbanPage xui-formPage">
			kanban page
		</div>
		)
	}
})
module.exports = KanbanPage;