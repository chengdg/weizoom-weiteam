
'use strict';

var path = require('path');
var UglifyJsPlugin = require("./node_modules/webpack/lib/optimize/UglifyJsPlugin");

module.exports = {
	entry: {
		dev: [
			'webpack/hot/only-dev-server',
			'webpack-dev-server/client?http://localhost:4188',
			path.resolve(__dirname, 'static/index.js')
		],
		dist: [
			path.resolve(__dirname, 'static/index.js')
		]
	},
	output: {
		path: path.resolve(__dirname, 'build'),
		filename: '[name].bundle.js',
		publicPath: '/static/'
	},
	module: {
		loaders: [{
			test: /\.jsx?$/,
			loader: 'babel-loader'
		}, {
			test: /\.css$/, // Only .css files
			loader: 'style!css' // Run both loaders
		}]
	},
	plugins: [
        //使用丑化js插件
        new UglifyJsPlugin({
            compress: {
                warnings: false
            },
            mangle: {
                except: ['window', '$']
            }
        })
    ]
};
