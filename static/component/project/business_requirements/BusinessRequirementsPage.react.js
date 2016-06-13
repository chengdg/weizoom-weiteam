/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:project.business_requirements:BusinessRequirementsPage');
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

var BusinessRequirementsPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		this.importance2class = {
			1: 'label label-danger',
			2: 'label label-warning',
			3: 'label label-info',
			4: 'label label-success',
			5: 'label label-default'
		}
		return Store.getData();
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData().filterOptions;
		this.refs.table.refresh(filterOptions);
	},

	componentDidMount: function() {
		var $window = $(window);
		this.dialogHeight = $window.height() - 200;
		this.dialogWidth = $window.width() - 50;
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
			width: this.dialogWidth,
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
			title: "新建业务需求", 
			type: 'large',
			component: NewRequirementDialog, 
			data: {
				type: 'business-requirement',
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
		} else if (field == 'importance') {
			var className = this.importance2class[value];
			return <span className={className}>{value}</span>;
		} else if (field == 'storyPoint') {
			return (
				<span>
					<span className="label label-success">{value}({data.subRequirements})</span>
				</span>
			)
		} else if (field == 'creater') {
			var user = value;
			return (
				<span>{user.name}</span>
			)
		} else if (field === 'action') {
			return (
				<div>
					<button className="btn btn-default btn-xs" data-id={data.id} data-toggle="tooltip" data-placement="top" title="" data-original-title="删除" onClick={this.onClickDelete}><i className="glyphicon glyphicon-remove"></i></button>
				</div>
			);
		} else {
			return value;
		}
	},

	render:function(){
		var resource = {
			resource: 'project.business_requirements',
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

		return (
		<div className="p20 xui-project-businessRequirementsPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormSelect label="状态:" name="status" options={statusOptions} match="=" />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormInput label="需求名:" name="title" match="~" placeholder="支持部分匹配" />
					</Reactman.FilterField>
					<Reactman.FilterField>
					</Reactman.FilterField>
				</Reactman.FilterRow>
			</Reactman.FilterPanel>

			<Reactman.TablePanel>
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="添加需求" icon="plus" onClick={this.onClickAddRequirement} />
				</Reactman.TableActionBar>
				<Reactman.Table resource={resource} formatter={this.rowFormatter} pagination={true} ref="table">
					<Reactman.TableColumn name="#" field="id" width="40px" />
					<Reactman.TableColumn name="需求" field="title" />
					<Reactman.TableColumn name="重要度" field="importance" width="70px"/>
					<Reactman.TableColumn name="故事点" field="storyPoint" width="70px"/>
					<Reactman.TableColumn name="创建人" field="creater" width="70px" />
					<Reactman.TableColumn name="创建日" field="createdAt" width="90px" />
					<Reactman.TableColumn name="操作" field="action" width="60px" />
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = BusinessRequirementsPage;