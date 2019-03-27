## Speedtest probe

The aim of this project is to create a probe application that measures your bandwidth,
and provide basic analysis tools, so you can determine if your ISP is giving you
the promised speeds. It's told that the [speedtest-cli library](https://github.com/sivel/speedtest-cli#inconsistency)
is not that consistent about real results, but with a lot of data you'll be able to
make your own conclusions.

This app is based on Flask, Flask-SocketIO (for realtime updates), and more stuff
to come when all of the planned features are developed. The frontend is based on 
VueJS, Socket.IO and charts lib to come.

### Running for development

- You need the last stable version of Python 3, pip and virtualenv.
- Create and enable a virtualenv on the root of the application.
- Install the requirements.
- Run `python app.py`. The `flask` is not recommended because it does not support
running websockets.
- Go to `http://127.0.0.1:5000/` on your browser.

What you'll see on the browser is the latest speedtest result. On the top bar
will be displayed the current speeds and status. On the main body, your network
information and other results informations are displayed.

### License
