/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.business_requirements:NewRequirementDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');


var NewRequirementDialog = Reactman.createDialog({
	getInitialState: function() {
		return {
			title: '',
			importance: '3',
			content: ''
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onBeforeCloseDialog: function() {
		var data = _.clone(this.state);
		data['project_id'] = this.props.data.projectId;

		Reactman.Resource.put({
			resource: 'project.business_requirement',
			data: data,
			success: function() {
				this.closeDialog();
			},
			error: function() {
				Reactman.PageAction.showHint('error', '创建需求失败!');
			},
			scope: this
		})
	},

	render:function(){
		var importanceOptions = [{
			text: '1（最高）',
			value: '1'
		}, {
			text: '2',
			value: '2'
		}, {
			text: '3（普通）',
			value: '3'
		}, {
			text: '4',
			value: '4'
		}, {
			text: '5（最低）',
			value: '5'
		}];

		return (
		<div className="xui-formPage xui-project-newBusinessRequirementDialog">
			<form className="form-horizontal mt15">
				<fieldset>
					<Reactman.FormInput label="需求名:" name="title" validate="require-string" value={this.state.title} onChange={this.onChange} autoFocus={true} inDialog={true} />
					<Reactman.FormSelect label="重要度:" name="importance" options={importanceOptions} value={this.state.importance} onChange={this.onChange} />
					<Reactman.FormRichTextInput label="需求详情:" name="content" validate="require-string" value={this.state.content} onChange={this.onChange} width={730} height={300}/>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = NewRequirementDialog;