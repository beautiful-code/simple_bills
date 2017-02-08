$(document).ready(function() {
  $('.datepicker').pickadate({
    selectMonths: true,
    selectYears: 30
  });

  $('.modal').modal();
  $('select').material_select();

  $('.dropdown-button').dropdown({
    inDuration: 300,
    outDuration: 225,
    constrain_width: false,
    hover: false ,
    gutter: 0,
    belowOrigin: true,
    alignment: 'right'
  });

  $('#flash_msg').fadeIn('fast').delay(4000).fadeOut('fast');
});

var SBUtils = {};

SBUtils.getQueryParams = function(queryString) {
  queryString = queryString.split('+').join(' ');

  var params = {},
    tokens,
    regex = /[?&]?([^=]+)=([^&]*)/g;

  while (tokens = regex.exec(queryString)) {
    params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
  }

  return params;
};

SBUtils.updateQueryParams = function(params) {
  var newUrl = window.location.pathname + params;

  window.history.replaceState(
    {},
    window.document.title,
    params
  );
};
