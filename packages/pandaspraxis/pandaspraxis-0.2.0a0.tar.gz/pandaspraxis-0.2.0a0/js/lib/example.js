var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');
require('./style.css');
const wf = require('./widgetfunctions.js');

// See example.py for the kernel counterpart to this file.


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serializing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var HelloModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'HelloModel',
        _view_name : 'HelloView',
        _model_module : 'pandaspraxis',
        _view_module : 'pandaspraxis',
        _model_module_version : '0.2.0',
        _view_module_version : '0.2.0',
        value : 'SELECT a FROM z'
    })
});

// Custom View. Renders the widget model.
// code adapted from https://github.com/PierreMarion23/jupyter-widget-hello-world-binder
    // Defines how the widget gets rendered into the DOM

var HelloView = widgets.DOMWidgetView.extend({
    callback:function(inputEvent, formElement){
        // reflect user's query back at them
        this.query.textContent = formElement[0].value;

        // send the message to python kernel to be translated
        this.send({event: 'callback', message: formElement[0].value});
    },

    render: function() {
        // when messages come from the python kernel, direct them to js functions
        this.model.on('change:value', this.value_changed, this);
        this.model.on('msg:custom', this.handle_message, this);
          
        let view = this;
        
        // add the js functions as an import from widgetfunctions.js
        let head = document.head;
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.text = 'var pair_emphasize = ' + wf.pair_emphasize +'; var pair_deemphasize = ' + wf.pair_deemphasize +
                    '; var open_sidebar = ' + wf.open_sidebar +'; var close_sidebar = ' + wf.close_sidebar +
                    '; var switch_or = ' + wf.switch_or + '; var copy_clipboard = ' + wf.copy_clipboard;
        head.appendChild(script);
        // add the icons stylesheet #TODO: try to get into a require(), but the basic one didn't work
        var fa_stylesheet = document.createElement('link');
        fa_stylesheet.rel = 'stylesheet';
        fa_stylesheet.href = "https://use.fontawesome.com/releases/v5.15.2/css/all.css";
        head.appendChild(fa_stylesheet);

        // create each element of the widget: 
        // title of the translator
        let title = document.createElement('h3');
        title.textContent = 'SQL to Pandas translator';

        // general user input form
        let forminput = document.createElement("form");
        forminput.setAttribute('onsubmit', 'return false;'); // don't refresh
        let formtext = document.createElement('p');
        formtext.textContent = 'What do you want to translate?';

        // box user writes in inside the form
        let inputbox = document.createElement("input");    
        inputbox.type = 'text';
        inputbox.size = '100';

        // submit/go button inside the form
        let submit = document.createElement("input");
        submit.type = 'submit';
        submit.value = 'Translate!'

        forminput.appendChild(formtext);
        forminput.appendChild(inputbox);
        forminput.appendChild(submit);
        
        // echo the user's request back at them
        let querytext = document.createElement("p");
        querytext.textContent = 'Your query was:';
        let query = document.createElement("p"); 
        query.id = 'pp-query';

        // create space after form for user to receive result
        let resulttext = document.createElement("p");
        resulttext.textContent = 'Here are your translated commands:';
        let result = document.createElement("div"); 

        // append all elements to the page
        this.el.appendChild(title);
        this.el.appendChild(forminput);
        this.el.appendChild(document.createElement("br")); 
        this.el.appendChild(querytext);          
        this.el.appendChild(query);
        this.el.appendChild(document.createElement("br")); 
        this.el.appendChild(resulttext);          
        this.el.appendChild(result);
        this.el.appendChild(document.createElement("br")); 
        this.el.appendChild(document.createElement("br")); 
            
        // initializing the form input box just so the user sees something
        inputbox.value = this.model.get('value');
            
        // when the form is submitted, start the translation process via callback
        forminput.addEventListener("submit", (inputEvent => view.callback(inputEvent, forminput)), false);

        // allow us to access result + query (so we can change it) in this class' other js functions
        this.result = result;
        this.query = query;
    },

    value_changed: function() {
        this.result.innerHTML = this.model.get('value')
    },

    handle_message: function(content) {
        // received message from python: it's the translation of the user's input
        this.model.set({'value': content.msg});
        this.touch(); // let python kernel know its value has been updated
    },
});

module.exports = {
    HelloModel: HelloModel,
    HelloView: HelloView,
};
