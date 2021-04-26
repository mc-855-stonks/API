import os
from redis import from_url
from app.main.config import config_by_env

redis = from_url(config_by_env[os.getenv('STONKS_ENV') or 'dev'].REDIS_URL)