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

require('./style.css');

var RequirementsPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		debug(Store.getData());
		return Store.getData();
	},

	onClickDelete: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确认删除吗?',
			confirm: _.bind(function() {
				Action.deleteProduct(productId);
			}, this)
		});
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData().filterOptions;
		this.refs.table.refresh(filterOptions);
	},

	rowFormatter: function(field, value, data) {
		if (field === 'models') {
			var models = value;
			var modelEls = models.map(function(model, index) {
				return (
					<div key={"model"+index}>{model.name} - {model.stocks}</div>
				)
			});
			return (
				<div style={{color:'red'}}>{modelEls}</div>
			);
		} else if (field === 'name') {
			return (
				<a href={'/outline/data/?id='+data.id}>{value}</a>
			)
		} else if (field === 'price') {
			return (
				<a onClick={this.onClickPrice} data-product-id={data.id}>{value}</a>
			)
		} else if (field === 'action') {
			return (
			<div>
				<button className="btn btn-default btn-xs" data-toggle="tooltip" data-placement="top" title="" data-original-title="删除">
<i className="glyphicon glyphicon-remove"></i></button>
			</div>
			);
		} else if (field === 'expand-row') {
			return (
				<div style={{paddingBottom:'20px'}}>
				<div className="clearfix" style={{backgroundColor:'#EFEFEF', color:'#FF0000', padding:'5px', borderBottom:'solid 1px #CFCFCF'}}>
					<div className="fl">促销结束日：{data.promotion_finish_time}</div>
					<div className="fr">总金额: {data.price}元</div>
				</div>
				</div>
			)
		} else {
			return value;
		}
	},

	onClickComment: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		var product = this.refs.table.getData(productId);
		Reactman.PageAction.showDialog({
			title: "创建备注", 
			component: CommentDialog, 
			data: {
				product: product
			},
			success: function(inputData, dialogState) {
				var product = inputData.product;
				var comment = dialogState.comment;
				Action.updateProduct(product, 'comment', comment);
			}
		});
	},

	onConfirmFilter: function(data) {
		Action.filterProducts(data);
	},

	onClickAddRequirement: function() {
		var projectId = this.state.projectId;
		Reactman.PageAction.showDialog({
			title: "新建需求", 
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
		}]

		return (
		<div className="p20 xui-project-requirementsPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormSelect label="状态:" name="status" options={statusOptions} match="=" />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormInput label="创建人:" name="name" match="=" />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormInput label="商品名3:" name="name3" match="=" />
					</Reactman.FilterField>
				</Reactman.FilterRow>
			</Reactman.FilterPanel>

			<Reactman.TablePanel>
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="添加需求" icon="plus" onClick={this.onClickAddRequirement} />
				</Reactman.TableActionBar>
				<Reactman.Table resource={resource} formatter={this.rowFormatter} pagination={true} ref="table">
					<Reactman.TableColumn name="#" field="index" width="40px" />
					<Reactman.TableColumn name="需求" field="title" />
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