/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.data:ProductModel');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var FormInput = Reactman.FormInput;

var Action = require('./Action');
var Constant = require('./Constant')

var ProductModel = React.createClass({
	getInitialState: function() {
		var model = this.props.model;
		return {
			index: this.props.index,
			name: model.name,
			stocks: model.stocks
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		this.state[property] = value;

		if (this.props.onChange) {
			this.props.onChange(this.state, event);
		}
	},

	onClickDelete: function(event) {
		if (this.props.onDelete) {
			this.props.onDelete(this.props.index);
		}
	},

	render:function(){
		var model = this.props.model;
		var autoFocus = !model.name;
		return (
			<div>
				<FormInput label="规格名:" type="text" name="name" validate="require-string" placeholder="" value={model.name} onChange={this.onChange} autoFocus={autoFocus} />
				<FormInput label="库存:" type="text" name="stocks" validate="require-int" placeholder="" value={model.stocks} onChange={this.onChange} />
				<a className="btn btn-default ml20" style={{'verticalAlign':'top'}} onClick={this.onClickDelete}><span className="glyphicon glyphicon-remove"></span></a>
			</div>
		)
	}
})
module.exports = ProductModel;