# MongoDB configuration
mongodb_config = {
    "host": "localhost",
    "port": 27017,
    "username": "",
    "password": "",
    "auth_source": "admin"
}

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False

    # MongoDB settings
    MONGO_HOST = mongodb_config["host"]
    MONGO_PORT = mongodb_config["port"]
    MONGO_USERNAME = mongodb_config["username"]
    MONGO_PASSWORD = mongodb_config["password"]
    MONGO_AUTH_SOURCE = mongodb_config["auth_source"]
    MONGO_DBNAME = "email_events"

    # Construct MongoDB URI from components
    @property
    def MONGO_URI(self):
        auth_part = ""
        if self.MONGO_USERNAME and self.MONGO_PASSWORD:
            auth_part = f"{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@"

        return f"mongodb://{auth_part}{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DBNAME}?authSource={self.MONGO_AUTH_SOURCE}"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    MONGO_DBNAME = "email_events_dev"


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MONGO_DBNAME = "email_events_test"


class ProductionConfig(Config):
    """Production configuration"""
    # Production might use different MongoDB settings
    MONGO_HOST = mongodb_config.get("prod_host", mongodb_config["host"])
    MONGO_PORT = mongodb_config.get("prod_port", mongodb_config["port"])
    MONGO_USERNAME = mongodb_config.get("prod_username", mongodb_config["username"])
    MONGO_PASSWORD = mongodb_config.get("prod_password", mongodb_config["password"])


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}