/*!
 * dorado
 *
 * Copyright(c) 2012-2015 weizoom
 * MIT Licensed
 */
'use strict';


var path = require('path');
var fs = require('fs');
var _string = require('underscore.string');

//增强js原生类型
(function() {
	/**
	 * 增强String
	 */
	String.prototype.splitLines = function() {
		return _string(this).trim().value().replace(/(\r\n)|\r|\n/g, '\n').split(/\n+/g);
	}

	String.prototype.trim = function() {
		return _string(this).trim().value();
	}

	String.prototype.ltrim = function() {
		return _string(this).ltrim().value();
	}

	String.prototype.rtrim = function() {
		return _string(this).rtrim().value();
	}

	String.prototype.startsWith = function(prefix) {
		return _string(this).startsWith(prefix);
	}

	String.prototype.endsWith = function(suffix) {
		return _string(this).endsWith(suffix);
	}

	String.prototype.contains = function(substring) {
		return this.indexOf(substring) !== -1;
	}

	String.prototype.substringBetween = function(prefix, suffix) {
		var beg = this.indexOf(prefix);
		if (beg === -1) {
			return '';
		}
		beg += prefix.length;
		var end = this.indexOf(suffix, beg);
		return this.substring(beg, end);
	}
})();






var getCopyFiles = function() {
	var filters = {
		".git": 1,
		"node_modules": 1,
		"build": 1,
		"outline": 1,
		"features": 1
	}
	var dir = '.';
	var files = fs.readdirSync(dir);
	var items = [];
	files.forEach(function(filePath) {
		filePath = path.join(dir, filePath);
		if (filters.hasOwnProperty(filePath)) {
			//需要过滤的，直接跳过
			return;
		}

		var stat = fs.statSync(filePath);
		if (stat.isDirectory()) {
			items.push(filePath + '/**');
			items.push('!' + filePath + '/**/*.pyc');
		}
	});
	return items;
}

var PruntTask = function() {
	this.taskLines = [];
	this.files = [];

	this.inRecordTaskMode = false;
}
PruntTask.prototype.addLine = function(line) {
	if (this.inRecordTaskMode) {
		if (line.contains('-->')) {
			this.inRecordTaskMode = false;
		} else {
			this.taskLines.push(line);
		}
	} else {
		if (line.contains('[prunt_task]')) {
			this.inRecordTaskMode = true;
		} else {
			if (line.contains('.css')) {
				var file = line.substringBetween('href="', '"');
				if (file.length === 0) {
					file = line.substringBetween("href='", "'");
				}
				this.files.push(file.substring(1, file.length));
			} else if (line.contains('.js')) {
				var file = line.substringBetween('src="', '"');
				if (file.length === 0) {
					file = line.substringBetween("src='", "'");
				}
				this.files.push(file.substring(1, file.length));
			}
		}
	}
}
PruntTask.prototype.getTask = function() {
	return JSON.parse(this.taskLines.join('\n').trim());
}
PruntTask.prototype.checkCompileFile = function(filePath) {
    var public_dir = '/static/mobile_v3/system';
    if (filePath.indexOf('public_dir') !== -1) {
        filePath = filePath.replace('public_dir', public_dir).replace(/[{|}]/g, '');
        filePath = filePath.substring(1, filePath.length)
        return filePath;
    }
    return filePath;
}


module.exports = function(grunt) {
	grunt.loadNpmTasks('grunt-shell');

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		prunt: {
			files: [
			'./templates/base.html'
			],
			cdn: 'weappstatic.b0.upaiyun.com',
			digestResult: {

			}
		},
		"weizoom-merge": {
			//this will be filled by task 'run_prunt_task'
		},
		uglify: {
			options: {
            },
            buildjs: {
            	options: {
	            	banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n',
	                footer:'\n/*! <%= pkg.name %> 最后修改于： <%= grunt.template.today("yyyy-mm-dd") %> */',
	            	compress: true,
	            	mangle: {
	            		except: ['jQuery', 'W', 'window']
	            	},
	            	report: 'gzip',
	            	sourceMap: false,
	            	beauty: false
	            },
	            files: {
	            	'build/cdn/vessels_static/js/vessels_lib.min.js': ['build/cdn/vessels_static/js/vessels_lib.js']
	            }
            }
		},
		cssmin: {
			buildcss: {
				options: {
					report: 'gzip',
					advanced: false,
					aggressiveMerging: false,
					shorthandCompacting: false,
					processImport: false,
					roundingPrecision: -1
				},
				files: {
					'build/cdn/vessels_static/css/vessels_all.min.css': ['build/cdn/vessels_static/css/vessels_all.css']
				}
			}
		},
		md5: {
		    digest_css: {
		    	files: {
		    		'build/cdn/vessels_static/css/': 'build/cdn/vessels_static/css/vessels_all.min.css'
		    	},
		    	options: {
		    		keepBasename: true,
		    		keepExtension: true,
		    		afterEach: function (fileChange, options) {
		    			grunt.config.set('prunt.digestResult.css', fileChange.newPath);
		    		}
		    	}
		    },
		    digest_js: {
		    	files: {
		    		'build/cdn/vessels_static/js/': 'build/cdn/vessels_static/js/vessels_lib.min.js'
		    	},
		    	options: {
		    		keepBasename: true,
		    		keepExtension: true,
		    		afterEach: function (fileChange, options) {
		    			grunt.config.set('prunt.digestResult.js', fileChange.newPath);
		    		}
		    	}
		    },
		},
		jshint: {
            options: {
            	'jshintrc': '.jshintrc'
                //'reporterOutput': 'jshint.text'
            },

            all: ['static/component/**/**.js']
        },
        copy: {
        	dist: {
        		files: [
        			{expand: true, src:getCopyFiles(), dest:'./dist/'},
        			{expand: false, src:['manage.py', 'rebuild.sh', 'rebuild_database.sql', 'start_service.sh', 'start_service.bat'], dest:'dist/'},
        			{expand: false, src:['dist/templates/base.html.merged.html'], dest:'dist/templates/base.html'},
        			{expand: true, cwd:'build/cdn', src:['vessels_static/**'], dest:'dist/static'},
        			{expand: true, cwd:'static/lib/font-awesome-4.5.0', src:['fonts/**'], dest:'dist/static/vessels_static'},
        			{expand: true, cwd:'static/lib/bootstrap-3.3.6', src:['fonts/**'], dest:'dist/static/vessels_static'},
        			{expand: false, src:['build/dist.bundle.js'], dest:'dist/static/bundle.js'}
        		]
        	}
        },
        shell: {
        	uploadCDN: {
        		command: 'python pytool/upload_cdn.py'
        	},
        	compileReactComponent: {
        		command: 'cnpm run build'
        	},
        	fixWebpackDynamicRequire: {
        		command: 'python pytool/fix_webpack_dynamic_require.py'
        	}
        }
	});

	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-md5');
	grunt.loadNpmTasks('grunt-jsxhint');
	grunt.loadNpmTasks('grunt-contrib-copy');
	

	grunt.registerTask('clean', function() {
		grunt.file.delete('./build');
		grunt.log.ok('delete ./build');
		grunt.file.delete('./dist');
		grunt.log.ok('delete ./dist');
		grunt.file.delete('./templates/base.html.merged.html');
		grunt.log.ok('delete ./templates/base.html.merged.html');
	});

	grunt.registerTask('weizoom-merge', function(id) {
		var destKey = _string.sprintf('weizoom-merge.%s.dest', id);
		var filesKey = _string.sprintf('weizoom-merge.%s.files', id);
		grunt.config.requires(destKey);
		//grunt.config.requires('weizoom-merge.pathMap');
		grunt.config.requires(filesKey);

		var files = grunt.config.get(filesKey);
		var dest = _string.sprintf('./build/%s', grunt.config.get(destKey))

		//make dirs
		var buf = [];
	    var pruntTask = new PruntTask();
		for (var i = 0; i < files.length; ++i) {
			var filePath = files[i];
			var isCssFile = (filePath.indexOf('.css') !== -1);

            // check compile flux js file by webpack
            filePath = pruntTask.checkCompileFile(filePath);

			grunt.log.writeln('process ' + filePath);
			if (!fs.existsSync(filePath)) {
				grunt.fail.fatal('[Error] file "' + filePath + '" is not EXISTS!');
			}

			var prefix = _string.sprintf("\n\n/* [SOURCE] %s */\n", filePath);
			if (isCssFile) {
				var suffix = '\n';
			} else {
				var suffix = "\n;\n";
			}
			var contents = grunt.file.read(filePath);
			buf.push(prefix+contents+suffix);
		}

		grunt.file.write(dest, buf.join('\n'));
		grunt.log.subhead("merge " + files.length + " files to " + dest);
	});


	grunt.registerTask('weizoom-replace-merge-result', function() {
		grunt.config.requires('prunt.files');
		var files = grunt.config.get('prunt.files');
		var cdnHost = grunt.config.get('prunt.cdn');

		for (var i = 0; i < files.length; ++i) {
			var filePath = files[i];
			if (!fs.existsSync(filePath)) {
				grunt.fail.fatal('[Error] file "' + filePath + '" is not EXISTS!');
			}
			var contents = grunt.file.read(filePath);
			var lines = [];
			var inTaskMode = false;
			var pruntTasks = [];
			var pruntTask = new PruntTask();
			contents.splitLines().forEach(function(line) {
				if (inTaskMode) {
					if (line.contains('*end_prunt_task*')) {
						var target = pruntTask.getTask().args.dest;
						if (target.indexOf('.css') !== -1) {
							//target = _string.sprintf('<link type="text/css" rel="stylesheet" href="http://%s/%s">', cdnHost, grunt.config.get('prunt.digestResult.css').replace('build/cdn/', ''));
							target = _string.sprintf('<link type="text/css" rel="stylesheet" href="/static/%s">', grunt.config.get('prunt.digestResult.css').replace('build/cdn/', ''));
							grunt.log.writeln("replace css files with " + target);
						} else {
							//target = _string.sprintf('<script type="text/javascript" src="http://%s/%s"></script>', cdnHost, grunt.config.get('prunt.digestResult.js').replace('build/cdn/', ''));
							target = _string.sprintf('<script type="text/javascript" src="/static/%s"></script>', grunt.config.get('prunt.digestResult.js').replace('build/cdn/', ''));
							grunt.log.writeln("replace js files with " + target);
						}

						lines.push(target);
						pruntTasks.push(pruntTask);
						pruntTask = new PruntTask();
						inTaskMode = false;
					} else {
						pruntTask.addLine(line);
					}
				} else {
					if (line.contains('*start_prunt_task*')) {
						inTaskMode = true;
					} else {
						lines.push(line);
					}
				}
			});
            grunt.file.write(filePath + '.merged.html', lines.join('\n'));
            grunt.log.ok('result file ' + filePath + '.merged.html');
		}
	});

	grunt.registerTask('modify-mode', function() {
		var filePath = './dist/wemanage/settings.py';
		var content = grunt.file.read(filePath);
		content = content.replace("MODE = 'develop'", "MODE = 'deploy'")
		grunt.file.write(filePath, content)
		grunt.log.ok("change MODE from 'develop' to 'deply'");
	});

	grunt.registerTask('run_prunt_task', function() {
		grunt.config.requires('prunt.files');
		var files = grunt.config.get('prunt.files');
		for (var i = 0; i < files.length; ++i) {
			var filePath = files[i];
			if (!fs.existsSync(filePath)) {
				grunt.fail.fatal('[Error] file "' + filePath + '" is not EXISTS!');
			}
			var contents = grunt.file.read(filePath);
			var lines = [];
			var inTaskMode = false;
			var pruntTasks = [];
			var pruntTask = new PruntTask();
			contents.splitLines().forEach(function(line) {
				if (inTaskMode) {
					if (line.contains('*end_prunt_task*')) {
						pruntTasks.push(pruntTask);
						pruntTask = new PruntTask();
						inTaskMode = false;
					} else {
						pruntTask.addLine(line);
					}
				} else {
					if (line.contains('*start_prunt_task*')) {
						inTaskMode = true;
					} else {
						lines.push(line);
					}
				}
			});
		}

		pruntTasks.forEach(function(pruntTask) {
			var taskInfo = pruntTask.getTask();
			var taskName = taskInfo.task;

			var id = taskInfo.id;
			var destKey = _string.sprintf('weizoom-merge.%s.dest', id);
			var filesKey = _string.sprintf('weizoom-merge.%s.files', id);
			grunt.config.set(destKey, taskInfo.args.dest);
			//grunt.config.set('weizoom-merge.pathMap', taskInfo.args.path_map);
			grunt.config.set(filesKey, pruntTask.files);
			
			grunt.task.run(taskName+":"+id);
		});

		grunt.task.run('uglify:buildjs');
		grunt.task.run('cssmin:buildcss');
		grunt.task.run('md5:digest_js');
		grunt.task.run('md5:digest_css');
		grunt.task.run('weizoom-replace-merge-result');
		grunt.task.run('copy:dist');
		grunt.task.run('modify-mode')
		//grunt.task.run('shell:uploadCDN');
	});


	grunt.registerTask('compile', function(){
		grunt.task.run('shell:fixWebpackDynamicRequire');
		grunt.task.run('shell:compileReactComponent');
    });

	grunt.registerTask('build', ['clean', 'jshint', 'compile', 'run_prunt_task']);
};
