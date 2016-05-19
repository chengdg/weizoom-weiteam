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

var CommentDialog = Reactman.createDialog({
	getInitialState: function() {
		var product = this.props.data.product;
		return {
			comment: product.comment
		}
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
					<Reactman.FormText label="备注:" name="comment" validate="require-string" placeholder="输入'error'体验评论失败场景，其他内容体验评论成功场景" value={this.state.comment} onChange={this.onChange} autoFocus={true} inDialog={true} width={300} height={200}/>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = CommentDialog;