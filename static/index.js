/*
Copyright (c) 2011-2016 Weizoom Inc
*/

'use strict';

var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
window.W = Reactman.W;

window.Debug = require("debug");

$(document).ready(function() {
	Debug.enable("reactman:*,m:*");

	var debug = window.Debug('reactman:main');
	var $page = $('.xa-pageContainer').eq(0);
	var pageNode = $page.get(0);

	ReactDOM.render(
		<Reactman.Page 
			sitename="WeManage" 
			userName={W.userName}
			topNavs={W.topNavs} 
			activeTopNav={W.activeTopNav} 
			secondNavs={W.secondNavs} 
			activeSecondNav={W.activeSecondNav}
			breadcrumb={W.breadcrumb}
			pageContentComponent={W.pageContentComponent}
		></Reactman.Page>, 
	pageNode);
});
