/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.members:Member');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');
var classNames = require('classnames');

var Reactman = require('reactman');

var Action = require('./Action');

var Member = React.createClass({
	componentDidMount: function() {
	},

	onClickDelete: function(event) {
		var id = parseInt(event.currentTarget.getAttribute('data-id'));
		event.memberId = id;
		if (this.props.onDelete) {
			this.props.onDelete(event);
		}
	},

	render:function(){
		var member = this.props.member;

		debug(Reactman.User);

		var cActionBar = '';
		if (Reactman.User.hasPerm('manage_project')) {
			cActionBar = (
				<div className="xui-i-actionBar">
					<button className="btn btn-default btn-xs ml5" data-id={member.id} onClick={this.onClickDelete}><span className="glyphicon glyphicon-remove"></span></button>
				</div>
			)
		}

		if (member.isCreater) {
			member.name = member.name + '-创建者';
		}

		return (
		<div className="xui-i-user fl">
			<img src={member.thumbnail} className="img-circle" width="100" height="100" />
			<div className="mt10">{member.name}</div>
			{cActionBar}
		</div>
		)
	}
});

module.exports = Member;