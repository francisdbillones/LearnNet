from learn_net import app

if __name__ == '__main__':
    import os

    dev = os.environ.get('DEV')

    # if DEV environment variable is set, run in debug mode
    if dev:
        app.run(debug=True)
    else:
        from gevent.pywsgi import WSGIServer
        server = WSGIServer(('', 5000), app)
        server.serve_forever()
