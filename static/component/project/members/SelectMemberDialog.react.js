/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:account.members:SelectMemberDialog');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Action = require('./Action');
var SelectMemberAction = require('./SelectMemberAction');
var SelectMemberStore = require('./SelectMemberStore');

var SelectMemberDialog = Reactman.createDialog({
	getInitialState: function() {
		var projectId = this.props.data.projectId;
		SelectMemberAction.getCandidateMembers(projectId);
		SelectMemberStore.addListener(this.onChangeStore);
		return SelectMemberStore.getData();
	},

	onChangeStore: function(event) {
		this.setState(SelectMemberStore.getData());
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);

		//在changed中记录改变的属性
		if (!this.state.changed) {
			this.state.changed = {};
		}
		this.state.changed[property] = value;
	},

	onBeforeCloseDialog: function() {
		this.closeDialog();
	},

	render:function(){
		return (
		<div className="xui-formPage xui-project-selectMemberDialog">
			<form className="form-horizontal mt15">
				<fieldset>
					<Reactman.FormCheckbox label="" name="selectedMembers" value={this.state.selectedMembers} options={this.state.members} onChange={this.onChange} />
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = SelectMemberDialog;