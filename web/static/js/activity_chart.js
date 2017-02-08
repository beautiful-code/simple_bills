var ActivityChart = function(config) {
  var self = this;
  self.chartContainerPrefix = config.chartContainerPrefix;
  self.accountsActivity = config.accountsActivity;

  google.charts.load('current', {packages: ['corechart', 'bar']});

  self.drawBasic = function(config) {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'X');
    data.addColumn('number', 'Bills');

    data.addRows(config.seriesData);

    var options = {
      hAxis: {
        format: 'MMM dd',
        minValue: moment().subtract(15, 'days').toDate(),
        gridlines: {
          color: 'transparent'
        }
      },
      vAxis: {
        title: 'No. of Bills',
        minValue: 0,
        maxValue: config.maxValue,
        format: '#',
        gridlines: {
          color: 'transparent'
        }
      },
      bar: {groupWidth: '5'},
      legend: {position: 'none'}
    };

    var chart = new google.visualization.ColumnChart(config.drawArea);

    chart.draw(data, options);
  };

  self.drawAccountActivityGraph = function(account) {
    var config = {
        seriesData: [],
        maxValue: account.activity.length + 5,
        accountActivity: account.activity,
        drawArea: document.getElementById(self.chartContainerPrefix + account.accountId)
    };

    if(account.activity) {
      account.activity.forEach(function(activity) {
        config.seriesData.push([
            new Date(activity.date),
            parseInt(activity.num_bills)
        ]);
      });
    }

    google.charts.setOnLoadCallback(function(){ self.drawBasic(config); });

  };

  if(self.accountsActivity.data) {
    self.accountsActivity.data.forEach(function(account) {
      if (account.activity) {
        self.drawAccountActivityGraph(account);
      }
    });
  }
};
