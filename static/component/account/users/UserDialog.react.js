/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:account.users:UserDialog');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

// var Store = require('./Store');
// var Constant = require('./Constant');
var Action = require('./Action');

var UserDialog = Reactman.createDialog({
	getInitialState: function() {
		if (this.props.data.user) {
			var user = this.props.data.user;
			return {
				id: user.id,
				name: user.name,
				realName: user.realName,
				email: user.email,
				thumbnail: [{
					id: 0,
					path: user.thumbnail
				}]
			}
		} else {
			return {
				id: null,
				name: '',
				realName: '',
				password: '',
				email: '',
				thumbnail: []
			};
		}
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
		var user = _.clone(this.state);
		if (user && user.thumbnail.length > 0) {
			user.thumbnail = user.thumbnail[0]['path'];
		} else {
			user.thumbnail = '';
		}
		user.real_name = user.realName;

		if (this.state.id) {
			//更新user
			Reactman.Resource.post({
				resource: 'account.user',
				data: user,
				success: function(data) { 
					this.state.changed.thumbnail = user.thumbnail;
					this.closeDialog();
				},
				error: function() {
					Reactman.PageAction.showHint('error', '创建用户失败!');
				},
				scope: this
			});
		} else {
			//新建user
			Reactman.Resource.put({
				resource: 'account.user',
				data: user,
				success: function(data) {
					this.state = data; //将state替换为创建之后的数据
					this.closeDialog();
				},
				error: function() {
					Reactman.PageAction.showHint('error', '创建用户失败!');
				},
				scope: this
			});
		}
	},

	render:function(){
		var cPassword = '';
		if (!this.state.id) {
			//新建user，需要显示密码输入框
			cPassword = <Reactman.FormInput label="密码:" name="password" placeholder="不填写，默认密码为weizoom" value={this.state.password} onChange={this.onChange} />;
		}

		return (
		<div className="xui-formPage xui-account-userDialog">
			<form className="form-horizontal mt15">
				<fieldset>
					<Reactman.FormInput label="登录名:" name="name" validate="require-string" value={this.state.name} onChange={this.onChange} autoFocus={true} inDialog={true} />
					<Reactman.FormInput label="真实姓名:" name="realName" validate="require-string" value={this.state.realName} onChange={this.onChange} />
					{cPassword}
					<Reactman.FormInput label="邮箱:" name="email" validate="require-string" value={this.state.email} onChange={this.onChange} />
					<Reactman.FormImageUploader label="头像:" name="thumbnail" value={this.state.thumbnail} onChange={this.onChange} max={1} />
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = UserDialog;