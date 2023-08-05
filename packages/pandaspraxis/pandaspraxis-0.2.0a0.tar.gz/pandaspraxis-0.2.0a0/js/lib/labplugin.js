var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'pandaspraxis:plugin',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'pandaspraxis',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

