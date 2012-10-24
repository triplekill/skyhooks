"""Tornado web handlers for webhook POST requests.
"""

import logging
from tornado.web import RequestHandler
from tornado.escape import json_decode


class WebhookHandler(RequestHandler):
    """Handle webhook post backs from celery tasks and route to websockets
    via registered callbacks.
    """

    def post(self):
        payload = json_decode(self.request.body)
        data = payload['data']
        keys = payload['keys']

        logging.info("Received webhook postback for %s", keys)

        if not self.application.webhook_container.notify(keys, data):
            self.set_status(404)
            return

        # Celery compatible "hook" response, good enough for our purposes
        return '{"status": "ok"}'
