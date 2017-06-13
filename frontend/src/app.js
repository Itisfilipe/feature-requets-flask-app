/**
 * Feature model
 * @param data - Feature document provided by the API
 */
function Feature(data) {
    this.id = ko.observable(data.id);
    this.title = ko.observable(data.title);
    this.description = ko.observable(data.description);
    this.client = ko.observable(new Client(data.client));
    this.priority = ko.observable(data.priority);
    this.date = ko.observable(data.date);
    this.area = ko.observable(new ProductArea(data.productArea));
}
/**
 * Product Area model
 * @param data - Product Area document provided by the API
 */
function ProductArea(data) {
    this.id = data.id;
    this.name = data.name;
}
/**
 * Client model
 * @param data - Client document provided by the API
 */
function Client(data) {
    this.id = data.id;
    this.name = data.name;
    this.priorities = [];
    // generate priorities list for browser select
    for (var i = 1; i <= +data.maxPriorities; i++) {
        this.priorities.push(i);
    }
}
/**
 * check if some of inputs returns invalid data.
 * @param  inputs - raw inputs
 * @return {Boolean}   returns true is is valid and false if not
 */
function isFormValid(inputs) {
    return inputs.filter(function(input) {
        return !input;
    }).length === 0;
}

/**
 * Wrapper for ajax calls
 * @param  {string}   type - type of call (POST, GET, etc...)
 * @param  {strin}   url - URI for resource
 * @param  {object}   data - data or null if needed
 * @param  {Function} callback - Function to be executed after success
 * @return {Promise}
 */
function ajaxRequest(type, url, data, callback) {
    return $.ajax({
        type: type,
        url: url,
        datatype: 'json',
        contentType: "application/json",
        data: data !== null ? JSON.stringify(data) : null,
        success: callback
    });
}

/**
 * Clear a list of observables
 * @param  {Arra<Observable>} observables - List of observables
 */
function clearObservables(observables) {
    observables.forEach(function(observable) {
        observable(null);
    });
}

/**
 * App Model
 */
function FeaturesViewModel() {
    // variable to "hold" the scope
    var self = this;
    // some const values
    var URL = 'http://127.0.0.1:5000/api';
    self.isEdit = false;

    // loaded data from server
    self.productAreas = ko.observableArray([]);
    self.clients = ko.observableArray([]);
    self.features = ko.observableArray([]);
    self.featureDetails = ko.observable();

    // form data
    self.newAreaName = ko.observable();
    self.newClientName = ko.observable();
    self.newTitle = ko.observable();
    self.newDescription = ko.observable();
    self.newDate = ko.observable();
    self.selectedClient = ko.observable();
    self.selectedProductArea = ko.observable();
    self.selectedPriority = ko.observable();

    // Behaviours
    self.goToFeature = function(feature) { location.hash = feature.id(); };
    self.goHome = function() { location.hash = '#/'; };

    // Operations
    self.addClient = function() {
        if (!isFormValid([self.newClientName()])) {
            alert("All inputs are required");
            return;
        }
        var data = { name: self.newClientName() };
        var _url = URL + "/clients";
        ajaxRequest("POST", _url, data, function() {
            self.getClients();
            self.newClientName("");
        }).always(function() { $('#newClientModal').modal('hide'); });
    };
    self.addProductArea = function() {
        if (!isFormValid([self.newAreaName()])) {
            alert("All inputs are required");
            return;
        }
        var data = { name: self.newAreaName() };
        var _url = URL + "/product-areas";
        ajaxRequest("POST", _url, data, function() {
            self.getProductAreas();
            self.newAreaName("");
        }).always(function() { $('#newProductAreaModal').modal('hide'); });
    };
    self.addFeature = function() {
        if (!isFormValid([
                self.newTitle(),
                self.newDescription(),
                self.newDate(),
                self.selectedProductArea(),
                self.selectedClient(),
                self.selectedPriority()
            ])) {
            alert("All inputs are required");
            return;
        }
        var data = {
            title: self.newTitle(),
            description: self.newDescription(),
            date: self.newDate(),
            productAreaId: self.selectedProductArea().id,
            clientId: self.selectedClient().id,
            priority: self.selectedPriority()
        };
        var method = "POST";
        var URL_suffix = "";
        if (self.isEdit) {
            URL_suffix = '/' + self.featureDetails().id;
            method = "PATCH";
        }
        var _url = URL + "/features" + URL_suffix;
        ajaxRequest(method, _url, data, function() {
            clearObservables([self.newTitle, self.newDescription, self.newDate, self.selectedProductArea, self.selectedClient, self.selectedPriority]);
            if (self.isEdit) {
                self.getFeature(self.featureDetails().id)
                self.isEdit = false;
            } else {
                self.getFeatures();
                self.getClients();
                self.getProductAreas();
                self.goHome();
            }
        }).always(function() { $('#newFeatureModal').modal('hide'); });
    };
    self.deleteFeature = function(data) {
        if (!confirm("Are you sure?")) return;
        var _url = URL + "/features/" + data.id;
        ajaxRequest("DELETE", _url, null, function() {
            self.featureDetails(null);
            self.getFeatures();
            self.getProductAreas();
            self.getClients();
            self.goHome();
        });
    };
    self.editFeature = function(data) {
        self.isEdit = true;
        self.newTitle(data.title);
        self.newDescription(data.description);
        self.newDate(data.date);
        var client = self.clients().filter(function(client) {
            return client.id === +data.client.id;
        })[0];
        self.selectedClient(client);
        var area = self.productAreas().filter(function(area) {
            return area.id === +data.productArea.id;
        })[0];
        self.selectedProductArea(area);
        self.selectedPriority(data.priority);
        $('#newFeatureModal').modal('show');
    };
    self.getClients = function() {
        var _url = URL + "/clients";
        ajaxRequest("GET", _url, null, function(data) {
            var mappedClients = $.map(data, function(clientData) {
                return new Client(clientData);
            });
            self.clients(mappedClients);
        });
    };
    self.getProductAreas = function() {
        var _url = URL + "/product-areas";
        ajaxRequest("GET", _url, null, function(data) {
            var mappedAreas = $.map(data, function(areaData) {
                return new ProductArea(areaData);
            });
            self.productAreas(mappedAreas);
        });
    };
    self.getFeatures = function() {
        var _url = URL + "/features";
        ajaxRequest("GET", _url, null, function(data) {
            data.sort(function(a, b) {
                return a.priority - b.priority;
            })
            var mappedFeatures = $.map(data, function(featureData) {
                return new Feature(featureData);
            });
            self.features(mappedFeatures);
        });
    };
    self.getFeature = function(featureId) {
        var _url = URL + "/features/" + featureId;
        ajaxRequest("GET", _url, null, self.featureDetails);
    };

    // Routes
    Sammy(function() {
        // feature details
        this.get('#:featureId', function() {
            self.features(null);
            self.getFeature(this.params.featureId);
            self.getProductAreas();
            self.getClients();
        });
        // index (features list)
        this.get('', function() {
            self.featureDetails(null);
            self.getFeatures();
            self.getProductAreas();
            self.getClients();
        });
    }).run();

    // listenner that must be registred at initialization
    self.listeners = function() {
        $('#newFeatureModal').on('hidden.bs.modal', function() {
            self.isEdit = false;
            clearObservables([self.newTitle, self.newDescription, self.newDate, self.selectedProductArea, self.selectedClient, self.selectedPriority]);
        });
        // just show the page after everything is loaded
        $(document).ready(function() {
            $('body').show();
        });
        // just show feature modal again if it was open before a new modal appears
        var featureModalWasOpen = false;
        // New Client modal
        $('#newClientModal').on('show.bs.modal', function() {
            featureModalWasOpen = ($("#newFeatureModal").data('bs.modal') || {}).isShown;
            $('#newFeatureModal').modal('hide');
        });
        $('#newClientModal').on('hidden.bs.modal', function() {
            if (featureModalWasOpen) {
                featureModalWasOpen = false;
                $('#newFeatureModal').modal('show');
            }
        });
        // New Product Area Modal
        $('#newProductAreaModal').on('show.bs.modal', function() {
            featureModalWasOpen = ($("#newFeatureModal").data('bs.modal') || {}).isShown;
            $('#newFeatureModal').modal('hide');
        });
        $('#newProductAreaModal').on('hidden.bs.modal', function() {
            if (featureModalWasOpen) {
                featureModalWasOpen = false;
                $('#newFeatureModal').modal('show');
            }
        });
    }
}

var app = new FeaturesViewModel()
app.listeners();
ko.applyBindings(app);
