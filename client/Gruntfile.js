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
          files: ['<%= jshint.files %>'],
          tasks: ['jshint']
        },
        concat: {
          options: {
            sourceMap:true
          },
          vendor: {
            src: [
              'app/bower_components/*/*.min.js',

            ],
            dest: 'dist/vendor.js',
          },
          source: {
            src: [
              'app/app.js',

            ],
            dest: 'dist/source.js',
          },
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
          'clean',
          'less',
          'concat',
          'copy'
        ]);
      });
    
    };