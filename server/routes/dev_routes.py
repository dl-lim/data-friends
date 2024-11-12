from quart import Blueprint
from db import get_docs, get_terms, get_term_frequencies

dev_routes = Blueprint('dev_routes', __name__)


@dev_routes.route('/docs')
async def docs():
    await get_docs()
    return "Done"


@dev_routes.route('/terms')
async def terms():
    await get_terms()
    return "Done"


@dev_routes.route('/term-frequencies')
async def term_frequencies():
    await get_term_frequencies()
    return "Done"