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
        watch: {
          files: ['<%= jshint.files %>'],
          tasks: ['jshint']
        },
        concat: {
          options: {
            separator: ';',
          },
          dist: {
            src: ['src/intro.js', 'src/project.js', 'src/outro.js'],
            dest: 'dist/built.js',
          },
        },
      });
    
      grunt.loadNpmTasks('grunt-contrib-jshint');
      grunt.loadNpmTasks('grunt-contrib-watch');
    
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