(function(w, d) {
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
    app.status = data;
  });
  socket.on('client_info', function(data) {
    app.client = data;
  });
  socket.on('current_results', function(data) {
    app.result = data;
  });
  socket.on('speedtest_update', function(data) {
    app.status = data;
  });

  socket.on('speedtest_started', function(data) {
    console.log('speedtest started:', data);
  });
  socket.on('speedtest_finished', function(data) {
    app.result = data;
  });
})(document, window);
