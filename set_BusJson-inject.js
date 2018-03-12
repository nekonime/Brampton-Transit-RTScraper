Orbital.Atis.Maps.Behavior.prototype.set_BusJson = function(value) {
    if (this._StopsJson !== value && value != '[]') {
        Sys.WebForms.PageRequestManager.getInstance().extender = this;

        try {
            this._BusJson = JSON.parse(value);
            _mapInstance.Buses = this._BusJson;
            console.log(value)
        }
        catch (e) { };

        this.raisePropertyChanged('BusJson');
    }
}