import logging
import os
from app.app import create_app

# Create Flask instance
app = create_app()

if __name__ == "__main__":
    # Run app
    app.run()
elif "GUNICORN_CMD_ARGS" in os.environ:
    # Configure logging to integrate with Gunicorn
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)