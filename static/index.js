/*
Copyright (c) 2011-2016 Weizoom Inc
*/

'use strict';

var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
window.W = Reactman.W;

var Page = require('./component/page/Page.react');

window.Debug = require("debug");

$(document).ready(function() {
	Debug.enable("reactman:*,m:*");

	var debug = window.Debug('reactman:main');
	var $page = $('.xa-pageContainer').eq(0);
	var pageNode = $page.get(0);

	ReactDOM.render(
		<Page 
			sitename="WeTeam" 
			userName={W.userName}
			topNavs={W.topNavs} 
			activeTopNav={W.activeTopNav} 
			pageContentComponent={W.pageContentComponent}
		></Page>, 
	pageNode);
});
