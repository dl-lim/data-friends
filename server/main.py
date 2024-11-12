from quart import Quart
from db import create_tables
from routes import api_routes, core_routes, dev_routes


# Create engine (web-server)
app = Quart(__name__)

# Add routes
app.register_blueprint(core_routes)
app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(dev_routes, url_prefix='/dev')


# Start the app
if __name__ == "__main__":
    create_tables()
    app.run()