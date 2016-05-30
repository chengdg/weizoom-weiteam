/**
 * reactman
 *
 */

var React = require('react');
var debug = require('debug')('m:page.TopNav');
var classNames = require('classnames');

var TopNav = React.createClass({
	onClickEdit: function(event) {
		alert('edit');
	},

	render:function(){
		var activeNav = this.props.activeNav;
		var lis = '';
		if (this.props.navs) {
			var lis = this.props.navs.map(function(nav) {
				var liClasses = classNames({
					active: nav.name === activeNav
				});

				if (nav.icon.contains('glyphicon-')) {
					var iconClasses = classNames('glyphicon', nav.icon);	
				} else if (nav.icon.contains('fa-')) {
					var iconClasses = classNames('fa', nav.icon, 'fa-3');
				} else {
					var iconClasses = classNames('glyphicon', 'glyphicon-'+nav.icon);
				}

				return (
					<li className={liClasses} key={"li-"+nav.name}><a href={nav.href}><span className={iconClasses}></span> {nav.displayName}</a></li>
				)
			});
		}

		return (
			<div id="header">
				<nav className="navbar navbar-default navbar-fixed-top xui-topNavbar">
					<div className="container-fluid">
						<div className="navbar-header mr20">
							<a className="navbar-brand" href="/">{this.props.name}</a>
						</div>

						<div className="collapse navbar-collapse" id="">
							<ul className="nav navbar-nav">
								{lis}
							</ul>

							<div className="btn-group navbar-form navbar-right">
								<button type="button" className="btn btn-default dropdown-toggle" data-toggle="dropdown">
									<span className="glyphicon glyphicon-user"></span> {this.props.userName} <span className="caret"></span>
								</button>

								<ul className="dropdown-menu" role="menu">
									<li><a onClick={this.onClickEdit}>编辑</a></li>
									<li className="divider"></li>
									<li><a href="/account/logout/">退出</a></li>
								</ul>
							</div>

							{this.props.children}
						</div>
					</div>
				</nav>
			</div>
		)
	}
})
module.exports = TopNav;