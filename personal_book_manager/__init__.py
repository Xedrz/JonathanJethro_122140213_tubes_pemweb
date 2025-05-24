from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import meta

def main(global_config, **settings):
    config = Configurator(settings=settings)
    engine = engine_from_config(settings, 'sqlalchemy.')
    meta.Base.metadata.bind = engine
    meta.DBSession.configure(bind=engine)

    config.include('pyramid_tm')
    config.include('.models')
    config.include('.routes')

    return config.make_wsgi_app()
