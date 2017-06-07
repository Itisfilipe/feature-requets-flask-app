/**
 * Control transitions between modals
 */
function modalControl() {
  // Events to control modal transitions
  // Client modal
  $('#newClientModal').on('show.bs.modal', function(e) {
    $('#newFeatureModal').modal('toggle');
  });
  $('#newClientModal').on('hidden.bs.modal', function(e) {
    $('#newFeatureModal').modal('toggle');
  });
  // Product Area Modal
  $('#newProductAreaModal').on('show.bs.modal', function(e) {
    $('#newFeatureModal').modal('toggle');
  });
  $('#newProductAreaModal').on('hidden.bs.modal', function(e) {
    $('#newFeatureModal').modal('toggle');
  });
}
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
}

function FeaturesViewModel() {
  // Data
  var self = this;
  self.features = ko.observableArray([]);
  self.featureDetails = ko.observable();
  self.newAreaName = ko.observable("");
  self.newClientName = ko.observable("");
  self.productAreas = ko.observableArray([]);
  self.clients = ko.observableArray([]);
  this.selectedClient = ko.observable();
  this.selectedProductArea = ko.observable();

  // Behaviours
  self.goToFeature = function(feature) { location.hash = feature.id() };
  self.goHome = function() { location.hash = '#/' };
  // Operations
  self.addClient = function(client) {
    var data = {name: self.newClientName()}
    $.post("http://localhost:3000/clients", data).done(function(s) {
      self.getClients();
      self.newClientName("")
    }).always(function(){ $('#newClientModal').modal('hide'); });;
  };
  self.addProductArea = function() {
    var data = {name: self.newAreaName()}
    $.post("http://localhost:3000/productAreas", data).done(function(s) {
      self.getProductAreas();
      self.newAreaName("");
    }).always(function(){ $('#newProductAreaModal').modal('hide'); });
  };
  self.addFeature = function() {
    // save feature to api
  };
  self.getClients = function() {
    $.getJSON("http://localhost:3000/clients", function(data) {
      var mappedClients = $.map(data, function(clientData) {
        return new Client(clientData)
      });
      self.clients(mappedClients);
    });
  }
  self.getProductAreas = function() {
    $.getJSON("http://localhost:3000/productAreas", function(data) {
      var mappedAreas = $.map(data, function(areaData) {
        return new ProductArea(areaData);
      });
      self.productAreas(mappedAreas);
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
  self.getFeature = function(featureId) {
    $.getJSON("http://localhost:3000/features/" + featureId, self.featureDetails);
  }
  // Routes
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
      self.getProductAreas()
      self.getClients()
    });
  }).run();
};
modalControl();
ko.applyBindings(new FeaturesViewModel());
