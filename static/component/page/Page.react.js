/**
 * reactman
 *
 */

var React = require('react');
var debug = require('debug')('m:page.Page');

var Reactman = require('reactman');
var TopNav = require('./TopNav.react');
var SecondNav = require('./SecondNav.react');

var dynamicRequire = require('../dynamic_require');

require('./style.css');

var Page = React.createClass({
	getInitialState: function() {
		return Reactman.PageStore.getData();
	},

	componentDidMount: function() {
		Reactman.PageStore.addListener(this.onChangePageStore);

		Reactman.Validater.init();

		$(document).click(function(event) {
			Reactman.PageAction.hidePopover();
		});

		$('[data-toggle="tooltip"]').tooltip();
	},

	onChangePageStore: function() {
		var data = Reactman.PageStore.getData();
		this.setState(data);
	},

	render:function(){
		var pageContent = '';
		if (this.props.pageContentComponent) {
			var pageContentComponent = dynamicRequire(this.props.pageContentComponent);
			var pageContent = React.createElement(pageContentComponent, {});
		}

		var cTopNavActions = '';
		if (pageContentComponent.topNavActionsComponent) {
			cTopNavActions = React.createElement(pageContentComponent.topNavActionsComponent, {});
		}

		var cSecondNavs = null;
		if (this.props.secondNavs) {
			cSecondNavs = <SecondNav navs={this.props.secondNavs} activeNav={this.props.activeSecondNav} />
		}
		return (
		<div>
			<Reactman.Confirm data={this.state.confirm} />
			<Reactman.Popover data={this.state.popover} />
			<Reactman.Dialog data={this.state.dialog} />
			<Reactman.GlobalLoader visible={this.state.isShowLoader} />
			<Reactman.GlobalHint type={this.state.hint.type} hint={this.state.hint.msg} />
			<TopNav name={this.props.sitename} navs={this.props.topNavs} activeNav={this.props.activeTopNav} userName={this.props.userName}>
				{cTopNavActions}
			</TopNav>
			<div id="main-panel">
				<div className="xui-contentPanel mt50">
					{cSecondNavs}
					<div className="xui-container" >
						{pageContent}
					</div>
				</div>
			</div>
		</div>
		)
	}
})
module.exports = Page;