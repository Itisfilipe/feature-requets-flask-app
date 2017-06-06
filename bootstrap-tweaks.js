(function($, window, document) {
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
}(window.jQuery, window, document));
