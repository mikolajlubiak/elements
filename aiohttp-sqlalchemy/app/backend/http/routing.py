from aiohttp.web import Application
from aiohttp import web

from backend.http.views import index
from backend.config import Config

def setup_routes(app: Application, config: Config = Config()) -> None:
    app.router.add_get('/', index)
    app.router.add_post('/register', register)
    app.router.add_post('/login', login)

    app.router.add_static('/static/', path=(config.static_files_dir), name='static')
