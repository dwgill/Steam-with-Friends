"use strict";

module.exports = function(grunt) {
        require('load-grunt-tasks')(grunt);
        grunt.initConfig({
        jshint: {
          files: ['Gruntfile.js', 'src/**/*.js', 'test/**/*.js'],
          options: {
            globals: {
              jQuery: true
            }
          }
        },
        less: {
          default:{
            files:[
              {
                expand:false,
                src: 'app/styles/app.less',
                dest:'dist/app.css'
              }
            ]
          }
        },
        clean: {
          dist: {
            files: [
              {
                dot: true,
                src: ['dist']
              }
            ]
          }
        },
        watch: {
          js:{
            files: ['app/**/*.js', '!app/bower_components/**/*.js'],
            tasks: ['concat:source']
          },
          less: {
            files: ['app/**/*.less'],
            tasks: ['less']
          },
          html:{
            files: ['app/**/*.html', '!app/bower_components/**/*'],
            tasks: ['copy:dist']
          }
        },
        concat: {
          options: {
            sourceMap:true
          },
          vendor: {
            src: [
              './app/bower_components/angular/angular.min.js',
              './app/bower_components/angular-bootstrap/ui-bootstrap.min.js',
              './app/bower_components/angular-resource/angular-resource.min.js',
              './app/bower_components/angular-route/angular-route.min.js',
              './app/bower_components/angular-sanitize/angular-sanitize.min.js',
              './app/bower_components/lodash/dist/lodash.min.js',
            ],
            dest: 'dist/vendor.js',
          },
          source: {
            src: [
              './app/**/*.js',
              './app/**/.js',
            ],
            dest: 'dist/source.js',
          },
        },
        bower_concat: {
          all: {
            dest: 'dist/vendor.js',
            cssDest: 'dist/vendor.css',
            bowerOptions: {
              relative: false
            }
          }
        },
        copy:{
          dist:{
            files: [{
              expand:true,
              dot:true,
              cwd: './app',
              dest: 'dist',
              src: [
                '**/*.{ico,png,txt,html,json,woff,ttf,woff2}',
                '.htaccess',
                '!bower_components/**/*',
                'bower_components/**/*.{woff,ttf,woff2}',
                '!**/*.css'
              ]
            }]
          }
        }
      });
  
    
      grunt.registerTask('default', ['jshint']);
      grunt.registerTask('build', function(){
        grunt.task.run([
          'less',
          'bower_concat',
          'concat:source',
          'copy'
        ]);
      });
    
    };