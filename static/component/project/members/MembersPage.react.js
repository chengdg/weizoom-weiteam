/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.members:MembersPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var Member = require('./Member.react');
var SelectMemberDialog = require('./SelectMemberDialog.react');

require('./style.css');

var MembersPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		Reactman.W.reload();
	},

	onClickAddMember: function(event) {
		Reactman.PageAction.showDialog({
			title: "添加成员", 
			component: SelectMemberDialog, 
			data: {
				projectId: this.state.projectId
			},
			scope: this,
			success: function(inputData, dialogState) {
				Action.addMembers(this.state.projectId, dialogState.selectedMembers);
			}
		});
	},

	onClickDeleteMember: function(event) {
		var memberId = event.memberId;
		var projectId = this.state.projectId;
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确认删除吗?',
			confirm: _.bind(function() {
				Action.deleteMember(this.state.projectId, memberId);
			}, this)
		});
	},

	render:function(){
		var onClickDeleteMember = this.onClickDeleteMember;
		var cMembers = this.state.members.map(function(member, index) {
			return (
				<Member member={member} key={member.id} onDelete={onClickDeleteMember} />
			)
		});

		return (
		<div className="mt15 xui-project-membersPage">
			<div className="xui-i-user xui-i-addUserTrigger fl" onClick={this.onClickAddMember}>
				<i className="fa fa-plus xui-i-addUser"></i>	
			</div>
			{cMembers}
		</div>
		)
	}
})
module.exports = MembersPage;