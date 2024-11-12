from quart import Quart
from db import create_tables
from routes import api_routes, core_routes, dev_routes
from system_tools import HOST, PORT, logger_config
import logging

# Create engine (web-server)
app = Quart(__name__)

# Add routes
app.register_blueprint(core_routes)
app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(dev_routes, url_prefix='/dev')


def create_app() -> None:
    """
    Initialize the quart application.

    :return: None
    """
    try:
        logger_config.create_logger()
    except Exception as e:
        print(f"Logger could not be created... proceeding with logging: {e}")
    finally:
        create_tables()
        logging.info(f"Database initialized")
        logging.info(f"server initialising on {HOST}:{PORT}")
        app.run(host=HOST, port=PORT)

# Start the app
if __name__ == "__main__":
    create_app()