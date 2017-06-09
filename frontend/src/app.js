/**
 * Control transitions between modals
 */
function modalControl() {
  // Events to control modal transitions
  // New Client modal
  $('#newClientModal').on('show.bs.modal', function(e) {
    $('#newFeatureModal').modal('toggle');
  });
  $('#newClientModal').on('hidden.bs.modal', function(e) {
    $('#newFeatureModal').modal('toggle');
  });
  // New Product Area Modal
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
  this.priorities = [];
  for (var i = 1; i <= +data.maxPriorities; i++) {
    this.priorities.push(i)
  }
}

function FeaturesViewModel() {
  var self = this;
  var URL = 'http://127.0.0.1:5000/api';
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
  self.goToFeature = function(feature) { location.hash = feature.id() };
  self.goHome = function() { location.hash = '#/' };
  // Operations
  self.addClient = function(client) {
    var data = { name: self.newClientName() }
    $.ajax({
      type: "POST",
      url: URL + "/clients",
      datatype: 'json',
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function() {
        self.getClients();
        self.newClientName("");
      }
    }).always(function() { $('#newClientModal').modal('hide'); });;
  };
  self.addProductArea = function() {
    var data = { name: self.newAreaName() }
    $.ajax({
      type: "POST",
      url: URL + "/product-areas",
      datatype: 'json',
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function() {
        self.getProductAreas();
        self.newAreaName("");
      }
    }).always(function() { $('#newProductAreaModal').modal('hide'); });
  };
  self.addFeature = function() {
    var data = {
      title: self.newTitle(),
      description: self.newDescription(),
      date: self.newDate(),
      productAreaId: self.selectedProductArea().id,
      clientId: self.selectedClient().id,
      priority: self.selectedPriority()
    };
    var method = "POST"
    URL_suffix = ""
    if (self.featureDetails() !== null) {
      URL_suffix = '/' + self.featureDetails().id;
      method = "PATCH"
    }
    $.ajax({
      type: method,
      url: URL + "/features" + URL_suffix,
      datatype: 'json',
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function(result) {
        self.newTitle("");
        self.newDescription("");
        self.newDate("");
        self.selectedProductArea("");
        self.selectedClient("");
        self.selectedPriority("");
        self.getFeatures();
      }
    }).always(function() { $('#newFeatureModal').modal('hide'); });
  };
  self.deleteFeature = function(data) {
    if (!confirm("Are you sure?")) return;
    $.ajax({
      type: "DELETE",
      url: URL + "/features/" + data.id,
      success: function(result) {
        self.featureDetails(null);
        self.getFeatures();
        self.getProductAreas();
        self.getClients();
        self.goHome();
      }
    });
  }
  self.editFeature = function(data) {
    self.newTitle(data.title);
    self.newDescription(data.description);
    self.newDate(data.date);
    var client = self.clients().filter(function(client) {
      return client.id === +data.client.id
    })[0];
    self.selectedClient(client);
    var area = self.productAreas().filter(function(area) {
      return area.id === +data.productArea.id
    })[0];
    self.selectedProductArea(area);
    self.selectedPriority(data.priority);
    $('#newFeatureModal').modal('show');
  }
  self.getPriorities = function() {
    $.getJSON(URL + "/clients", function(data) {
      var mappedClients = $.map(data, function(clientData) {
        return new Client(clientData)
      });
      self.clients(mappedClients);
    });
  }
  self.getClients = function() {
    $.getJSON(URL + "/clients", function(data) {
      var mappedClients = $.map(data, function(clientData) {
        return new Client(clientData)
      });
      self.clients(mappedClients);
    });
  }
  self.getProductAreas = function() {
    $.getJSON(URL + "/product-areas", function(data) {
      var mappedAreas = $.map(data, function(areaData) {
        return new ProductArea(areaData);
      });
      self.productAreas(mappedAreas);
    });
  }
  self.getFeatures = function() {
    $.getJSON(URL + "/features", function(data) {
      var mappedFeatures = $.map(data, function(featureData) {
        return new Feature(featureData)
      });
      self.features(mappedFeatures);
    });
  }
  self.getFeature = function(featureId) {
      $.getJSON(URL + "/features/" + featureId, self.featureDetails);
    }
    // Routes
  Sammy(function() {
    // feature details
    this.get('#:featureId', function() {
      self.features(null);
      self.getFeature(this.params.featureId);
      self.getProductAreas();
      self.getClients();
    });
    // index/features list
    this.get('', function() {
      self.featureDetails(null);
      self.getFeatures();
      self.getProductAreas();
      self.getClients();
    });
  }).run();
};
modalControl();
ko.applyBindings(new FeaturesViewModel());
