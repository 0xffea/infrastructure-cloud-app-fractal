# coding: utf-8

# --------------------------------------------------------------------------
# 2021
# --------------------------------------------------------------------------
"""
Classes and functions used in Fractal app.
"""

import json
import logging
import time

from common import queue_client
from common import container_client
from common import DEFAULT_ITERATIONS
from common import DEFAULT_RESOLUTION
from compute import Fractal


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


if __name__ == "__main__":
    while True:
        messages = queue_client.receive_messages()

        for message in messages:
            payload = message.content
            logger.info(f"Dequeueing message: {payload}")
            payload = json.loads(payload)
            request_id = payload["request_id"]
            iterations = payload.get("iterations", DEFAULT_ITERATIONS)
            resolution = payload.get("resolution")
            if resolution:
                resolution = (resolution.get("x"), resolution.get("y"))
            else:
                resolution = DEFAULT_RESOLUTION
            frame = payload.get("frame")
            if frame:
                frame = (frame.get("x"), frame.get("x1"), frame.get("y"), frame.get("y1"))
            else:
                frame = (-2, 0.5, -1.3, 1.3)

            logger.info(request_id)
            queue_client.delete_message(message.id, message.pop_receipt)
            fractal = Fractal(
                frame,
                iterations=iterations,
                resolution=resolution
            )
            logger.info("Generating image...")
            data = fractal.generate()
            logger.info("Uploading image to blob storage")
            blob_client = container_client.get_blob_client(request_id)
            blob_client.upload_blob(data, blob_type="BlockBlob")

        time.sleep(3)
