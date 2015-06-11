var aiot = aiot || {};
aiot.events = {};

(function(ns) {

function EventManager(config) {
    this.config = config;
}

EventManager.prototype.initialize_stream = function() {
    var self = this;

    var source = new EventSource(this.config.url);
    source.onmessage = function(event) {
        var events = JSON.parse(event.data);
        self.add_events(events);
    };

    /* TODO: Handle errors gracefully here .. */
};

EventManager.prototype.trigger_callback = function(callback_fn_name, args) {
    var callback_fn = this.config[callback_fn_name];
    if (callback_fn) {
        callback_fn.apply(this, args);
    }
};

EventManager.prototype.add_events = function(events) {
    var self = this;

    this.trigger_callback('on_before_events');
    this.trigger_callback('on_events' [events]);

    $.each(events, function(k, event) {
        self.trigger_callback('on_event', [event]);
    });

    this.trigger_callback('on_after_events');
};

EventManager.prototype.start = function() {
    if (this.config.initial_events) {
        this.add_events(this.config.initial_events);
    }

    if (this.config.url) {
        this.initialize_stream();
    }
};

ns.EventManager = EventManager;

})(aiot.events);
