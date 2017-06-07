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
  this.id = ko.observable(data.id);
  this.name = ko.observable(data.name);
}
/**
 * Client model
 * @param data - Client document provided by the API
 */
function Client(data) {
  this.id = ko.observable(data.id);
  this.name = ko.observable(data.name);
}

function FeaturesViewModel() {
  // Data
  var self = this;
  self.features = ko.observableArray([]);
  self.featureDetails = ko.observable();
  self.areas = ko.observableArray([]);
  self.clients = ko.observableArray([]);
  // Behaviours
  self.goToFeature = function(feature) { location.hash = feature.id() };
  self.goHome = function() { location.hash = '#/' };
  // Operations
  self.addClient = function() {
    // save client to api
  };
  self.addProductArea = function() {
    // save product area to api
  };
  self.addFeature = function() {
    // save feature to api
  };
  self.getClients = function() {
    $.getJSON("http://localhost:3000/features?_expand=client&_expand=productArea", function(data) {
      var mappedClients = $.map(data, function(clientData) {
        return new Client(clientData)
      });
      self.clients(mappedClients);
    });
  }
  self.getProductAreas = function() {
    $.getJSON("http://localhost:3000/features?_expand=client&_expand=productArea", function(data) {
      var mappedAreas = $.map(data, function(areaData) {
        return new Area(areaData)
      });
      self.features(mappedAreas);
    });
  }
  self.getFeatures = function() {
    $.getJSON("http://localhost:3000/features?_expand=client&_expand=productArea", function(data) {
      var mappedFeatures = $.map(data, function(featureData) {
        return new Feature(featureData)
      });
      self.features(mappedFeatures);
    });
  }
  self.getFeature = function(featureId){
    $.getJSON("http://localhost:3000/features/" + featureId, self.featureDetails);
  }
  Sammy(function() {
    // feature details
    this.get('#:featureId', function() {
      self.features(null);
      self.getFeature(this.params.featureId);
    });
    // index/features list
    this.get('', function() {
      self.featureDetails(null);
      self.getFeatures();
    });
  }).run();
};
ko.applyBindings(new FeaturesViewModel());
