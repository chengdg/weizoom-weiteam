/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.business_requirements:EditRequirementDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Action = require('./Action');

var EditRequirementDialog = Reactman.createDialog({
	getInitialState: function() {
		this.loadRequirement();
		return {
			id: null,
			content: '',
			importance: -1,
			changed: {}
		};
	},

	loadRequirement: function() {
		Reactman.Resource.get({
			resource: 'project.business_requirement',
			data: {
				project_id: this.props.data.projectId,
				requirement_id: this.props.data.requirementId
			},
			scope: this,
			success: function(data) {
				this.setState(data);
			}
		})
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);

		this.state.changed[property] = value;

		Action.updateRequirementInServer(this.props.data.projectId, this.state, property, value);
	},

	onBeforeCloseDialog: function() {
		this.closeDialog();
	},

	render:function(){
		if (this.state.id) {
			var importanceOptions = [{
				text: '1（最高）',
				value: 1
			}, {
				text: '2',
				value: 2
			}, {
				text: '3（普通）',
				value: 3
			}, {
				text: '4',
				value: 4
			}, {
				text: '5（最低）',
				value: 5
			}];
		} else {
			importanceOptions = [{
				text: '加载中...',
				value: '-1'
			}]
		}

		return (
		<div className="xui-formPage xui-project-editBusinessRequirementDialog">
			<form className="form-horizontal mt0">
				<div className="form-line xui-i-bar pt10 pb10 mb10">
					<Reactman.FormSelect label="重要度:" name="importance" options={importanceOptions} value={this.state.importance} onChange={this.onChange} />
				</div>
				<div className="xui-i-content" dangerouslySetInnerHTML={{__html: this.state.content}}></div>
			</form>
		</div>
		)
	}
})
module.exports = EditRequirementDialog;