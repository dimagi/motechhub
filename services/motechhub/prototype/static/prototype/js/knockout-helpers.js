$.fn.koApplyBindings = function (context) {
    if (!this.length) {
        throw new Error("No element passed to koApplyBindings");
    }
    if (this.length > 1) {
        throw new Error("Multiple elements passed to koApplyBindings");
    }
    ko.applyBindings(context, this.get(0));
    this.removeClass('ko-template');
};
