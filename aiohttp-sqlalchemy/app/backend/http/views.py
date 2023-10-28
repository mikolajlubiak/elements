import aiohttp
from aiohttp import web
import aiohttp_jinja2
import aiohttp_session
import aiohttp_csrf

from sqlalchemy import insert, select, update, exists
from sqlalchemy.orm import Session

from backend.database.storage import UserStorage
from backend.config import Config
import backend.security

config = Config()
routes = web.RouteTableDef()

def create_get_function(template: str, context = None):
    async def F(request: web.Request):
        if context is not None:
            if 'field_name' in context.keys():
                token = await aiohttp_csrf.generate_token(request)
                context['token'] = token
        response = aiohttp_jinja2.render_template(template, request, context=context)
        return response
    return F


index = create_get_function('index.html')

async def register(request: web.Request):
    form = await request.post()
    session = await aiohttp_session.get_session(request)
    login = form["login"]
    hashed_password = backend.security.generate_password_hash(form["password"])

    storage = UserStorage(request.app['db'])

    if storage.get_entity_by_attributes(login=login) is not None:
        return {'error_message': "User already exists"}

    entity_attributes = {
            "login": login,
            "password": hashed_password
            }

    storage.add_entity(**entity_attributes)

async def login(request: web.Request):
    form = await request.post()
    session = await aiohttp_session.get_session(request)
    login = form["login"]
    password = form["password"]

    storage = UserStorage(request.app['db'])
    entity = storage.get_entity_by_attributes(login=login)

    if entity and backend.security.check_password_hash(entity.password, password):
        session['login'] = login

