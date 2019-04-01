(function(d, w) {
  let app = new Vue({
    el: '#app',
    data: {
      status: 'unknown',
      client: null,
      result: null,
    },
    filters: {
      humanbits: function(bits) {
        return filesize(bits/8, {bits: true})
      },
      humanbytes: function(bytes) {
        return filesize(bytes)
      }
    }
  });

  ///////////////////////////////////////////////////////////////////////////

  let socket = io.connect('http://' + document.domain + ':' + location.port);

  socket.on('client_connect', function(data) {
    app.status = data.status;
    app.client = data.client_info;
  });

  socket.on('current_results', function(data) {
    console.log('current results:', data);
    app.result = data;
  });

  socket.on('speedtest_update', function(data) {
    console.log('update', data);

    app.status = data.status;
    if (data.status === 'finished') {
      app.result = data.data;
    }
  });

  //////////////////////////////////////////////////////////////////////////
  let chartConfig = {
    type: 'line',
    data: {
      datasets: []
    },
    options: {
      responsive: true,
      title: {
        display: true,
        text: 'Download speeds chart'
      },
      tooltips: {
        mode: 'index',
        intersect: false,
      },
      hover: {
        mode: 'nearest',
        intersect: true
      },
      scales: {
        xAxes: [{
          type: 'time',
          time: {
            parser: 'DD/MM/YYYY HH:mm',
            // round: 'day'
            tooltipFormat: 'll HH:mm',
            unit: 'minute'
          },
          scaleLabel: {
            display: true,
            labelString: 'Timestamp'
          }
        }],
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'DL (bytes)'
          }
        }]
      },
    }
  };

  let ctx = d.getElementById('speed-chart').getContext('2d');

  axios.get('/results').then(function(data) {
    let datasets = {};
    let min = new Date();
    let max = new Date();

    data.data.forEach(result => {
      let name = `${result.server.sponsor} - ${result.server.name} - ${result.server.cc}`;
      if (!datasets.hasOwnProperty(name)) {
        datasets[name] = [];
      }

      let dateIns = new Date(result.batch_timestamp);
      min = new Date(Math.min(min, dateIns));
      max = new Date(Math.max(max, dateIns));

      let entry = {
        t: moment(result.batch_timestamp),
        y: result.download / 1048576
      };

      console.log(entry);
      datasets[name].push(entry);
    });

    let chartDatasets = [];
    Object.keys(datasets).forEach( ds => {
      datasets[ds].sort((a,b) => (a.t > b.t) ? 1 : ((b.t > a.t) ? -1 : 0));

      chartDatasets.push({
        label: ds,
        fill: false,
        data: datasets[ds]
      });
    });

    console.log(chartDatasets);

    let x = new Date();
    x.setHours(x.getHours()-4);
    chartConfig.options.scales.xAxes[0].time.min = x;
    chartConfig.options.scales.xAxes[0].time.max = new Date();

    chartConfig.data.datasets = chartDatasets;

    let chart = new Chart(ctx, chartConfig);
  });

})(document, window);
