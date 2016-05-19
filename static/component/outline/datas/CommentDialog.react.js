/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:CommentDialog');
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
		if (this.state.comment === 'error') {
			Reactman.PageAction.showHint('error', '不能关闭对话框');
		} else {
			var product = this.props.data.product;
			Reactman.Resource.post({
				resource: 'outline.data_comment',
				data: {
					product_id: product.id,
					comment: this.state.comment
				},
				success: function() {
					this.closeDialog();
				},
				error: function() {
					Reactman.PageAction.showHint('error', '评论失败!');
				},
				scope: this
			})
		}
	},

	render:function(){
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<Reactman.FormInput label="项目名:" name="name" validate="require-string" value={this.state.name} onChange={this.onChange} autoFocus={true} inDialog={true} />
					<Reactman.FormInput label="简介:" name="description" validate="require-string" value={this.state.description} onChange={this.onChange} />
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = NewProjectDialog;