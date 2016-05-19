/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.projects:NewProjectDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

// var Store = require('./Store');
// var Constant = require('./Constant');
var Action = require('./Action');

var NewProjectDialog = Reactman.createDialog({
	getInitialState: function() {
		return {
			name: '',
			description: ''
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onBeforeCloseDialog: function() {
		var project = this.state;
		Reactman.Resource.put({
			resource: 'project.project',
			data: project,
			success: function() {
				this.closeDialog();
			},
			error: function() {
				Reactman.PageAction.showHint('error', '创建团队失败!');
			},
			scope: this
		})
	},

	render:function(){
		return (
		<div className="xui-formPage xui-project-newProjectDialog">
			<form className="form-horizontal mt15">
				<fieldset>
					<Reactman.FormInput label="团队:" name="name" validate="require-string" value={this.state.name} onChange={this.onChange} autoFocus={true} inDialog={true} />
					<Reactman.FormText label="团队简介:" name="description" validate="require-string" value={this.state.description} onChange={this.onChange} width={330} height={200}/>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = NewProjectDialog;