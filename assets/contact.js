// Preselect the service chosen on the homepage. Only known values are accepted.
(function () {
  var allowed = ["Property Cleanup", "Rental Turnover", "Recurring Property Care", "Other"];
  var chosen = new URLSearchParams(location.search).get("service");
  var field = document.getElementById("service");
  if (field && chosen && allowed.indexOf(chosen) !== -1) field.value = chosen;
})();
