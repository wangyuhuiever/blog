import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    pass

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    pass

class TestConfig(Config):
    pass

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production':ProductionConfig,
    'default': DevelopmentConfig
}