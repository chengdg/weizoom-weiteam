/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:account.users:User');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');
var classNames = require('classnames');

var Reactman = require('reactman');

var Action = require('./Action');
var UserDialog = require('./UserDialog.react');


var User = React.createClass({
	componentDidMount: function() {
		var $user = $(ReactDOM.findDOMNode(this));
		var $actionBar = $user.find('.xa-actionBar').eq(0);
		$user.mouseenter(function() {
			$actionBar.removeClass('xui-hide');
		}).mouseleave(function() {
			$actionBar.addClass('xui-hide');
		});
	},

	onClickDelete: function(event) {
		var id = parseInt(event.currentTarget.getAttribute('data-id'));
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确认删除吗?',
			confirm: _.bind(function() {
				Action.deleteUser(id);
			}, this)
		});
	},

	onClickEdit: function(event) {
		var user = this.props.user;
		debug(user);
		Reactman.PageAction.showDialog({
			title: "添加用户", 
			component: UserDialog,
			data: {
				user: user
			},
			success: function(inputData, dialogState) {
				debug(dialogState.changed);
				Action.updateUser(user, dialogState.changed);
			}
		});
	},

	render:function(){
		var user = this.props.user;

		return (
		<div className="xui-i-user fl">
			<img src={user.thumbnail} className="img-circle" width="100" height="100" />
			<div className="mt10">{user.realName}</div>
			<div className="xui-i-actionBar xa-actionBar xui-hide">
				<button className="btn btn-default btn-xs" data-id={user.id} onClick={this.onClickEdit}><span className="glyphicon glyphicon-pencil"></span></button>
				<button className="btn btn-default btn-xs ml5" data-id={user.id} onClick={this.onClickDelete}><span className="glyphicon glyphicon-remove"></span></button>
			</div>
		</div>
		)
	}
});

module.exports = User;