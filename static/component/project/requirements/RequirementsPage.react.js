/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.requirements:RequirementsPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
var NewRequirementDialog = require('./NewRequirementDialog.react');
var EditRequirementDialog = require('./EditRequirementDialog.react');

require('./style.css');

var RequirementsPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData().filterOptions;
		this.refs.table.refresh(filterOptions);
	},

	componentDidMount: function() {
		var $window = $(window);
		this.dialogHeight = $window.height() - 200;
	},

	onClickDelete: function(event) {
		var requirementId = parseInt(event.currentTarget.getAttribute('data-id'));
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确认删除吗?',
			scope: this,
			confirm: function() {
				Action.deleteRequirement(this.state.projectId, requirementId);
			}
		});
	},

	onClickPullToKanban: function(event) {
		var requirementId = parseInt(event.currentTarget.getAttribute('data-id'));
		var requirement = this.refs.table.getData(requirementId);
		Action.pullToKanban(requirement);
	},

	onClickViewRequirement: function(event) {
		var requirementId = parseInt(event.currentTarget.getAttribute('data-id'));
		var requirement = this.refs.table.getData(requirementId);
		var projectId = this.state.projectId;
		
		Reactman.PageAction.showDialog({
			title: requirement.title, 
			type: 'large',
			height: this.dialogHeight,
			component: EditRequirementDialog, 
			data: {
				projectId: projectId,
				requirementId: requirementId
			},
			success: function(inputData, dialogState) {
				Action.updateRequirement(requirement, dialogState);
			}
		});
	},

	onConfirmFilter: function(data) {
		Action.filterRequirements(data);
	},

	onClickAddRequirement: function() {
		var projectId = this.state.projectId;
		Reactman.PageAction.showDialog({
			title: "新建故事", 
			type: 'large',
			component: NewRequirementDialog, 
			data: {
				projectId: projectId
			},
			success: function(inputData, dialogState) {
				Reactman.W.reload();
			}
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'title') {
			return (
				<a onClick={this.onClickViewRequirement} className="xui-i-title" data-id={data.id}>{value}</a>
			);
		} else if (field === 'action') {
			var cDeleteButton = null;
			if (Reactman.User.hasPerm('manage_project')) {
				cDeleteButton = (<button className="btn btn-default btn-xs" data-id={data.id} data-toggle="tooltip" data-placement="top" title="" data-original-title="删除" onClick={this.onClickDelete}><i className="glyphicon glyphicon-remove"></i></button>);
			}

			return (
				<div>
					<button className="btn btn-default btn-xs mr5" data-id={data.id} data-toggle="tooltip" data-placement="top" title="" data-original-title="进入看板" onClick={this.onClickPullToKanban}><i className="glyphicon glyphicon-list-alt"></i></button>
					{cDeleteButton}
				</div>
			);
		} else {
			return value;
		}
	},

	render:function(){
		var resource = {
			resource: 'project.requirements',
			data: {
				project_id: this.state.projectId,
				page: 1
			}
		};

		var statusOptions = [{
			text: '全部',
			value: -1
		}, {
			text: '未开始',
			value: '0'
		}, {
			text: '进行中',
			value: '1'
		}, {
			text: '已结束',
			value: '2'
		}];

		var importanceOptions = [{
				text: '加载中...',
				value: '-1'
			}];

		var storyPointOptions = [{
				text: '加载中...',
				value: '-1'
			}];

		return (
		<div className="p20 xui-project-requirementsPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormSelect label="状态:" name="status" options={statusOptions} match="=" />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormInput label="故事名:" name="title" match="~" placeholder="支持部分匹配" />
					</Reactman.FilterField>
					<Reactman.FilterField>
					</Reactman.FilterField>
				</Reactman.FilterRow>
			</Reactman.FilterPanel>

			<Reactman.TablePanel>
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="添加故事" icon="plus" onClick={this.onClickAddRequirement} />
				</Reactman.TableActionBar>
				<Reactman.Table resource={resource} formatter={this.rowFormatter} pagination={true} ref="table">
					<Reactman.TableColumn name="#" field="index" width="40px" />
					<Reactman.TableColumn name="用户故事" field="title" />
					<Reactman.TableColumn name="标签" field="tags" width="100px" />
					<Reactman.TableColumn name="重要度" field="importance" width="70px"/>
					<Reactman.TableColumn name="故事点" field="storyPoint" width="70px"/>
					<Reactman.TableColumn name="创建人" field="creater" width="70px" />
					<Reactman.TableColumn name="创建日" field="createdAt" width="90px" />
					<Reactman.TableColumn name="操作" field="action" width="160px" />
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = RequirementsPage;