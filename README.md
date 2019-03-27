## Speedtest probe

The aim of this project is to create a probe application that measures your bandwidth,
and provide basic analysis tools, so you can determine if your ISP is giving you
the promised speeds. It's told that the [speedtest-cli library](https://github.com/sivel/speedtest-cli#inconsistency)
is not that consistent about real results, but with a lot of data you'll be able to
make your own conclusions. 

It's intended to be run on your own computer, connected via ethernet, with the
right port speed, depending on the speed you're paying for, but you probably
should be using a gigabit ethernet port, and connected directly to the main router,
if possible. This settings will help to produce accurate results.

This app is based on Flask, Flask-SocketIO (for realtime updates), and more stuff
to come when all of the planned features are developed. The frontend is based on 
VueJS, Socket.IO and charts lib to come.

### Running for development

- You need the last stable version of Python 3, pip and virtualenv.
- Create and enable a virtualenv on the root of the application.
- Install the requirements.
- Run `python app.py`. The `flask` command is not recommended because it does not 
support exposing websockets.
- Go to `http://127.0.0.1:5000/` on your browser.

What you'll see on the browser is the latest speedtest result. On the top bar
will be displayed the current speeds and status. On the main body, your network
information and other results informations are displayed.

### TO-DO list

- [ ] Store results on a database (MongoDB)
- [ ] Display a basic graph with latest results
- [ ] Change Speedtest servers from the UI
- [ ] Set expected results from the UI (national and intl.)
- [ ] you tell me xd

### License

This project is under the [MIT license](LICENSE.txt).
