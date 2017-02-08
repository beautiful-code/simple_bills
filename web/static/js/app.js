var simpleBills = angular.module("SimpleBills", []);

simpleBills.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('#{').endSymbol('}');
});

simpleBills.controller("AddAccountController", function($scope) {
  $scope.formValidator = new CustomFormValidator({
    requiredFields: ['account_name'],
    submitBtnLoadingText: 'Creating ...'
  });
});

simpleBills.controller("SearchBillController", function($scope) {
  $scope.accountId = PageConfig ? PageConfig.accountId : "";
  $scope.accountTags = PageConfig ? PageConfig.accountTags : [];
  $scope.stats = PageConfig ? PageConfig.stats : {};
  $scope.bills = [];
  $scope.search_tags = {};

  var format_search_tags = function() {
    var tags = "";

    for (var tag in $scope.search_tags) {
      if ($scope.search_tags[tag] === true) {
        tags += "search_tags=" + tag + "&";
      }
    }

    return tags.slice(0, -1);
  };

  $scope.accountTags.forEach(function(tag) {
    $scope.search_tags[tag] = false;
  });

  $scope.fetchBills = function() {
    // Show the spinner
    $('#spinner-container').show();
    $.ajax({
      method: 'GET',
      url: "/account/" + $scope.accountId + "/search_bills?" + format_search_tags(),
      data: {
        search_query: $scope.search_query,
        search_start_date: $scope.search_start_date,
        search_end_date: $scope.search_end_date
      },
      success: function(data) {
        $scope.bills = data.results;
        $scope.$digest();
        $('#spinner-container').hide();
      },
      error: function() {
        location.reload();
      }
    });
  };

  $scope.imageThumbnail = function(file) {
    var thumbUrl = "/static/images/file256.png";

    switch(file.file_type) {
      case "application/pdf":
        thumbUrl = "/static/images/pdf256.png";
        break;
      case "image/png":
        thumbUrl = file.thumbnail;
        break;
      case "image/jpg":
        thumbUrl = file.thumbnail;
        break;
      case "image/jpeg":
        thumbUrl = file.thumbnail;
        break;

    }

    return thumbUrl;
  };

  $scope.searchOnEnterKey = function($event) {
    if ($event.keyCode == 13) {
      $scope.fetchBills();
    }
  };

  $scope.isTagSelected = function(tag) {
    return $scope.search_tags[tag];
  };

  var monthNames = moment.months();
  $scope.currentYear = moment().year();
  $scope.currentMonth = moment().month();
  $scope.currentMonthName = monthNames[$scope.currentMonth];

  $scope.setStartEndDates = function() {
    var startDay = moment([$scope.currentYear, $scope.currentMonth]).startOf('month').date();
    var endDay = moment([$scope.currentYear, $scope.currentMonth]).endOf('month').date();

    $scope.search_start_date = [$scope.currentYear, ($scope.currentMonth + 1), startDay].join('-');
    $scope.search_end_date = [$scope.currentYear, ($scope.currentMonth + 1), endDay].join('-');
  };

  $scope.selectedYearMonthsData = function() {
    return $scope.allYearsStats()[$scope.currentYear];
  };

  $scope.updateQueryParams = function() {
    var params = "?year=" + $scope.currentYear + "&month=" + ($scope.currentMonth + 1);
    SBUtils.updateQueryParams(params);
  };

  $scope.updateCurrentYearAndMonthsData = function(clearGetParams) {
    if (clearGetParams) {
      $scope.updateQueryParams();
      $scope.setStartEndDates();
      $scope.monthsData = $scope.selectedYearMonthsData();
      $scope.fetchBills();
    } else {
      $scope.determineTheMonthToShow();
    }
  };

  $scope.determineTheMonthToShow = function() {
    // Read getParams and update the currentYear and currentMonth
    var queryParams = SBUtils.getQueryParams(window.location.search);
    $scope.currentYear = parseInt(queryParams.year) || $scope.currentYear;
    $scope.currentMonth = (parseInt(queryParams.month) - 1) || $scope.currentMonth;

    $scope.monthsData = $scope.selectedYearMonthsData();

    // select the months that has bills
    var data = _.filter($scope.monthsData, function(m) { return m.billCount > 0; });
    var preSelectedMonth;

    if (data.length > 0) {
      if ($scope.monthsData[$scope.currentMonth].billCount > 0) {
        preSelectedMonth = $scope.currentMonth;
      } else {
        preSelectedMonth = moment().month(data[0].monthName).month();
      }
    } else {
      preSelectedMonth = moment().month();
    }

    $scope.updateCurrentMonth(preSelectedMonth, false);
  };

  $scope.updateCurrentMonth = function(month, disabled) {
    if(disabled) {} else {
      $scope.currentMonth = month;
      $scope.updateQueryParams();
      $scope.setStartEndDates();
      $scope.currentMonthName = monthNames[month];
      $scope.fetchBills();
    }
  };

  $scope.allYearsStats = function() {
    var data = {};

    _.each($scope.getStatsYears(), function(year) {
      data[year] = [];
      _.each(moment.monthsShort(), function(m) { data[year].push({monthName: m, billCount: 0}); });
    });

    _.each($scope.stats.year_stats, function(yearStat) {
      var year = parseInt(yearStat.year);

      _.each(yearStat.month_stats, function(monthStat) {
        var month = parseInt(monthStat.month) - 1;
        data[year][month].billCount = parseInt(monthStat.bill_count);
      });

    });

    return data;
  };

  $scope.getStatsYears = function() {
    var years = [];

    _.each($scope.stats.year_stats, function(yearStat) {
      years.push(parseInt(yearStat.year));
    });

    // Add current year by default
    years.push(moment().year());

    years = _.uniq(years);

    var minYear = _.min(years);
    var maxYear = _.max(years);
    var ret = [minYear];

    var diff = moment([maxYear,0]).diff(minYear + '-01-01', 'years');

    _.times(diff, function(i) {
      ret.push(minYear + (i + 1));
    });

    return ret;
  };

  // Invoke init methods manually for the first time
  $scope.updateCurrentYearAndMonthsData();
});

simpleBills.controller("AddBillController", function($scope) {
  $scope.accountId = PageConfig ? PageConfig.accountId : "";

  $scope.formValidator = new CustomFormValidator({
    requiredFields: ['bill_desc', 'bill_amount', 'bill_date']
  });
});

simpleBills.controller("EditBillController", function($scope) {
  $scope.bill = PageConfig ? PageConfig.bill : {};

  $scope.formValidator = new CustomFormValidator({
    requiredFields: ['bill.title', 'bill.amount', 'bill.date']
  });
});

simpleBills.controller("FeedbackController", function($scope) {
  $scope.formValidator = new CustomFormValidator({
    requiredFields: ['feedback_desc'],
    submitBtnLoadingText: 'Sending ...'
  });

  var defaultDesc = "Please type your feedback here ...";
  $scope.feedback_desc = defaultDesc;

  $scope.submitFeedback = function($event) {
    if ($scope.feedback_desc != defaultDesc) {
      $scope.formValidator.submitForm($event);
    } else {
      $('[ng-model="feedback_desc"]').addClass('invalid');
    }
  };
});
