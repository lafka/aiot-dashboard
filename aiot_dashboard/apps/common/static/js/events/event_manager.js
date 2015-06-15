var aiot = aiot || {};
aiot.events = {};

(function(ns) {

function EventManager(config) {
    this.config = config;
}

EventManager.prototype.build_url = function() {
    var params = [];
    if (this.config.datetime_from) {
        params.push('datetime_from=' + encodeURIComponent(this.config.datetime_from));
    }
    if (this.config.datetime_to) {
        params.push('datetime_to=' + encodeURIComponent(this.config.datetime_to));
    }
    if (this.config.stream) {
        params.push('stream=true');
    }

    return this.config.url + '?' + params.join('&');
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

ns.EventManager = EventManager;

})(aiot.events);
