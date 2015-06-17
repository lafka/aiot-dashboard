var aiot = aiot || {};
aiot.events = {};

(function(ns) {

function EventManager(config) {
    this.config = config;
    this.source = null;
}

EventManager.prototype.build_url = function() {
    var params = [];

    // TODO: Put this all in a loop.
    if (this.config.graph_start !== undefined) {
        params.push('graph_start=' + encodeURIComponent(this.config.graph_start));
    }
    if (this.config.graph_end) {
        params.push('graph_end=' + encodeURIComponent(this.config.graph_end));
    }
    if (this.config.datetime_from) {
        params.push('datetime_from=' + encodeURIComponent(this.config.datetime_from));
    }
    if (this.config.datetime_to) {
        params.push('datetime_to=' + encodeURIComponent(this.config.datetime_to));
    }
    if (this.config.stream) {
        params.push('stream=true');
    }
    if (this.config.params !== undefined) {
    	$.each(this.config.params, function(k, v) {
    		params.push(k + '=' + encodeURIComponent(v));
    	});
    }

    var query_seperator = this.config.url.indexOf('?') >= 0 ? '&' : '?';
    return this.config.url + query_seperator + params.join('&');
};

EventManager.prototype.trigger_callback = function(callback_fn_name, args) {
    var callback_fn = this.config[callback_fn_name];
    if (callback_fn) {
        callback_fn.apply(this, args);
    }
};

EventManager.prototype.add_events = function(events) {
    var self = this;

    this.trigger_callback('on_before_events', [events]);
    this.trigger_callback('on_events' [events]);

    $.each(events, function(k, event) {
        self.trigger_callback('on_event', [event]);
    });

    this.trigger_callback('on_after_events', [events]);
};

EventManager.prototype.start = function() {
    var self = this;

    var url = this.build_url();

    var source = new EventSource(url);
    self.source = source;

    source.onmessage = function(e) {
        self.trigger_callback('on_message', [e]);
        var events = JSON.parse(e.data);
        self.add_events(events);

        if (!self.config.stream) {
            source.close();
        }
    };

    source.onerror = function(e) {
        self.trigger_callback('on_error', [e]);
    };

    source.onopen = function(e) {
        self.trigger_callback('on_open', [e]);
    };

    /* TODO: Handle errors gracefully here .. */
};

EventManager.prototype.stop = function() {
	if(this.source !== null) {
		this.source.close();
		this.source = null;
		console.log("Stopped source");
	}
};

ns.EventManager = EventManager;

})(aiot.events);
