/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.requirements:RequirementsPage:CommentList');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');
var classNames = require('classnames');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
var NewRequirementDialog = require('./NewRequirementDialog.react');
var EditRequirementDialog = require('./EditRequirementDialog.react');

require('./style.css');

var CommentList = React.createClass({
	getInitialState: function() {
		this.isDirty = false;
		return {
			isInEditMode: false,
			commentInEdit: '',
			comments: this.props.comments
		}
	},

	componentWillReceiveProps: function(nextProps) {
		if (!this.isDirty) {
			debug('receive props');
			debug(nextProps);
			this.setState({
				comments: nextProps.comments
			});
		}
	},

	componentDidUpdate: function() {
		var $el = $(ReactDOM.findDOMNode(this));
		$el.find('.xa-comment').each(function() {
			var $comment = $(this);
			var $actionBar = $comment.find('.xa-actionBar').eq(0);
			$comment.mouseenter(function() {
				$actionBar.removeClass('xui-hide');
			}).mouseleave(function() {
				$actionBar.addClass('xui-hide');
			});
		});
	},

	onClickAddComment: function(event) {
		event.preventDefault();
		event.stopPropagation();

		var projectId = this.props.projectId;
		var requirementId = this.props.requirementId;

		Reactman.Resource.put({
			resource: "project.requirement_comment",
			data: {
				project_id: projectId,
				requirement_id: requirementId,
				content: this.state.commentInEdit
			},
			scope: this,
			success: function(data) {
				var comments = this.state.comments;
				comments.push(data);
				this.isDirty = true;

				this.refs.input.clear();

				this.setState({
					isInEditMode: false,
					commentInEdit: '',
					comments: comments
				});
			}
		});
	},

	onClickEnterEditMode: function(event) {
		event.preventDefault();
		event.stopPropagation();
		this.setState({
			isInEditMode: true
		});

		_.delay(_.bind(function() {
			this.refs.input.focus();

			if (this.props.onEnterEditMode) {
				this.props.onEnterEditMode();
			}
		}, this), 100);
	},

	onClickCancelEditMode: function(event) {
		event.preventDefault();
		event.stopPropagation();

		this.refs.input.clear();

		this.setState({
			isInEditMode: false
		});
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onClickDeleteComment: function(event) {
		event.preventDefault();
		event.stopPropagation();
		var id = parseInt(event.currentTarget.getAttribute('data-id'));

		var projectId = this.props.projectId;
		var requirementId = this.props.requirementId;
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确认删除吗?',
			confirm: _.bind(function() {
				Reactman.Resource.delete({
					resource: 'project.requirement_comment',
					data: {
						project_id: projectId,
						requirement_id: requirementId,
						comment_id: id
					},
					scope: this,
					success: function() {
						Reactman.PageAction.showHint('success', '删除评论成功');
						var newComments = _.filter(this.state.comments, function(comment) {
							return comment.id !== id;
						});
						this.isDirty = true;
						this.setState({
							comments: newComments
						});
					},
					error: function() {
						Reactman.PageAction.showHint('error', '删除评论失败');
					}
				})
			}, this)
		});
	},

	renderActionArea: function() {
		var cButton = null;
		var richtextInputStyle = {};
		if (this.state.isInEditMode) {
			cButton = (
				<span className="fr">
					<button className="btn btn-danger btn-xs mr5" onClick={this.onClickCancelEditMode}><span className="glyphicon glyphicon-remove"></span> 取消</button>
					<button className="btn btn-primary btn-xs" onClick={this.onClickAddComment}><span className="glyphicon glyphicon-ok"></span> 提交</button>
				</span>
			)
		} else {
			richtextInputStyle = {
				'display': 'none'
			}
			cButton = <button className="btn btn-success btn-xs fr" onClick={this.onClickEnterEditMode}><span className="glyphicon glyphicon-plus"></span> 评论</button>;
		}

		return (
			<div className="xui-i-actionArea">
				<div style={richtextInputStyle}>
					<Reactman.FormRichTextInput name="commentInEdit" value={this.state.commentInEdit} label="" height={200} width={this.props.width-60} onChange={this.onChange} ref="input" />
				</div>
				{cButton}
			</div>
		);
	},

	render: function() {
		var _this = this;
		var cComments = this.state.comments.map(function(comment, index) {
			return (
				<div className="xui-i-comment xa-comment" key={index}>   
					<div className="clearfix">        
						<div className="fl"><img src={comment.creater.thumbnail} className="xui-i-thumbnail" /></div>
						<div className="fl ml10" dangerouslySetInnerHTML={{__html: comment.content}}></div>
					</div>
					<div className="xui-i-date">{comment.createdAt}</div>
					<div className="xui-i-actionBar xa-actionBar xui-hide">
						<button className="btn btn-default btn-xs ml5" data-id={comment.id} onClick={_this.onClickDeleteComment}><span className="glyphicon glyphicon-remove"></span></button>
					</div>
				</div>
			)
		});

		var cActionArea = this.renderActionArea();

		return (
		<div className="xui-project-requirementCommentList">
			{cComments}

			{cActionArea}
		</div>
		);
	}
});

module.exports = CommentList;