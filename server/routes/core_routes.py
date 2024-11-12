from quart import Blueprint

core_routes = Blueprint('core_routes', __name__)

# Core Routes are all routes that have no specific endpoint url

# Default route
@core_routes.route('/')
def default():
    """
    The default route for the application.
    """
    return "Welcome to this Rag application!\n"