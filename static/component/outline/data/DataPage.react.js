/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.data:DataPage');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var ProductModelList = require('./ProductModelList.react');
var Store = require('./Store');
var Action = require('./Action');

var OutlineDataPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		debug(Store.getData());
		return Store.getData();
	},

	onChangeStore: function() {
		this.setState(Store.getData());
	},

	onChange: function(value, event) {
		debug(value);
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	onSubmit: function() {
		Action.saveProduct(Store.getData());
	},

	componentDidMount: function() {
		debug(ReactDOM.findDOMNode(this.refs.name));
	},

	render:function(){
		var optionsForJoinPromotion = [{
			text: '参加',
			value: '1'
		}, {
			text: '不参加',
			value: '0'
		}];

		var optionsForChannel = [{
			text: '南京',
			value: 'nanjing'
		}, {
			text: '北京',
			value: 'beijing'
		}, {
			text: '上海',
			value: 'shanghai'
		}, {
			text: '无锡',
			value: 'wuxi'
		}];

		return (
		<div className="xui-outlineData-page xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<legend className="pl10 pt10 pb10">商品信息</legend>
					<Reactman.FormInput label="商品名:" name="name" validate="require-string" placeholder="" value={this.state.name} onChange={this.onChange} autoFocus={true} />
					<Reactman.FormInput label="重量:" name="weight" validate="require-int" placeholder="" value={this.state.weight} onChange={this.onChange} />
					<Reactman.FormInput label="价格:" name="price" validate="require-price" placeholder="输入价格" value={this.state.price} onChange={this.onChange} />
					<Reactman.FormRadio label="参与双11促销:" name="isJoinPromotion" value={this.state.isJoinPromotion} options={optionsForJoinPromotion} onChange={this.onChange} />
					<Reactman.FormDateTimeInput label="促销结束时间:" name="promotionFinishDate" placeholder="促销结束日期" value={this.state.promotionFinishDate} onChange={this.onChange} validate="require-string" />
					<Reactman.FormCheckbox label="渠道:" name="channels" value={this.state.channels} options={optionsForChannel} onChange={this.onChange} />
					<Reactman.FormImageUploader label="图片:" name="images" value={this.state.images} onChange={this.onChange} max={3} />
					<Reactman.FormFileUploader label="文档:" name="documents" value={this.state.documents} onChange={this.onChange} max={3} />
				</fieldset>

				<fieldset className="form-inline">
					<legend className="pl10 pt10 pb10">商品规格</legend>
					<ProductModelList name='models' value={this.state.models} onChange={this.onChange} />
				</fieldset>

				<fieldset className="form-inline">
					<legend className="pl10 pt10 pb10">其他信息</legend>
					<Reactman.FormRichTextInput label="商品详情" name="detail" width={800} validate="require-notempty" value={this.state.detail} onChange={this.onChange} />
				</fieldset>

				<fieldset>
					<Reactman.FormSubmit onClick={this.onSubmit} text="确 定"/>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = OutlineDataPage;