/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:DatasPage');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var OutlinePage = React.createClass({
	getInitialState: function() {
		return {};
	},

	render:function(){
		return (
		<div className="mt15 xui-outline-outlinePage">
			<div className="row clearfix">
				<div className="xui-col-3">
					<Reactman.Widget fa="users" theme="navy">
						粉丝总数<br/>
						20408<br/>
						昨日新增<br/>
						10
					</Reactman.Widget>
				</div>

				<div className="xui-col-3">
					<Reactman.Widget fa="pencil-square-o" theme="lazur">
						反馈总数<br/>
						16466<br/>
						昨日新增<br/>
						123
					</Reactman.Widget>
				</div>

				<div className="xui-col-3">
					<Reactman.Widget fa="credit-card" theme="yellow">
						微众卡总数<br/>
						2507
					</Reactman.Widget>
				</div>
			</div>

			<div className="row clearfix">
				<Reactman.Chart id="fansIncrementTrend" resource={{resource:"outline.fans_increment_trend", data:{}}} title="粉丝增量趋势图" />
				<Reactman.Chart id="fansTrend" resource={{resource:"outline.fans_trend", data:{}}} title="粉丝总量趋势图" />
			</div>
			<div className="row clearfix">
				<Reactman.Chart id="taskFinishTime" resource={{resource:"outline.task_finish_time", data:{base:50}}} title="任务完成时间分布图" />
			</div>
		</div>
		)
	}
})
module.exports = OutlinePage;