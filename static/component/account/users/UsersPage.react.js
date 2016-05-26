/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:account.users:UsersPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var User = require('./User.react');
var UserDialog = require('./UserDialog.react');

require('./style.css');

var UsersPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		this.setState(Store.getData());
	},

	onClickCreateUser: function(event) {
		Reactman.PageAction.showDialog({
			title: "添加用户", 
			component: UserDialog, 
			data: {
				user: null
			},
			success: function(inputData, dialogState) {
				Action.addUser(dialogState);
			}
		});
	},

	render:function(){
		var cUsers = this.state.users.map(function(user, index) {
			return (
				<User user={user} key={user.id} />
			)
		});

		return (
		<div className="mt15 xui-account-usersPage">
			<div className="xui-i-user xui-i-addUserTrigger fl" onClick={this.onClickCreateUser}>
				<i className="fa fa-plus xui-i-addUser"></i>	
			</div>
			{cUsers}
		</div>
		)
	}
})
module.exports = UsersPage;