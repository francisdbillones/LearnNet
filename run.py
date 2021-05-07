from learn_net import app

# if DEV environment variable is set, run in debug mode
if __name__ == '__main__':
    import os

    dev = os.environ.get('DEV')
    if dev:
        app.run(debug=True)
    else:
        from waitress import serve
        serve(app, host='0.0.0.0', port=8080)
