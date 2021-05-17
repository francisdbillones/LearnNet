from learn_net import app
from werkzeug.exceptions import RequestEntityTooLarge


@app.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    return 'File could not be processed.'
