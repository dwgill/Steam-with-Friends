"use strict";

module.exports = function(grunt) {
        require('time-grunt')(grunt);
        var rewrite = require('connect-modrewrite');

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
        watch: {
          files: ['<%= jshint.files %>'],
          tasks: ['jshint']
        },
        connect: {
            server: {
                options:{
                    port:9001,
                    hostname: 'localhost',
                    liverload: true,
                    base: ['dist'],
                    middleware: function(connect, options, middlewares){
                        var rules =[

                        ];
                        middlewares.unshift(rewrite(rules));
                        return middlewares;
                    }
                }
            }
        }
      });
    
      grunt.loadNpmTasks('grunt-contrib-jshint');
      grunt.loadNpmTasks('grunt-contrib-watch');
    
      grunt.registerTask('default', ['jshint']);
    
    };