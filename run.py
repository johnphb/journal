from app.app import create_app
import logging
import os

app = create_app()

if __name__ == "__main__":
    app.run()
elif "GUNICORN_CMD_ARGS" in os.environ:
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
