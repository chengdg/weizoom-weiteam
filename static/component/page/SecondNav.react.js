/**
 * reactman
 *
 */

var React = require('react');
var debug = require('debug')('m:page.SecondNav');
var classNames = require('classnames');

var SecondNav = React.createClass({
	render:function(){
		var activeNav = this.props.activeNav;
		var cLis = null;
		if (this.props.navs) {
			var cLis = this.props.navs.map(function(nav) {
				var liClasses = classNames({
					active: nav.name === activeNav
				});

				return (
					<li className={liClasses} key={"li-"+nav.name}><a href={nav.href}>{nav.displayName}</a></li>
				)
			});
		}

		return (
			<div className="xui-secondNav">
				<ul className="nav nav-pills">
					{cLis}
				</ul>
			</div>
		)
	}
})
module.exports = SecondNav;