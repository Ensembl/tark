import os


ENV = os.getenv('DJANGO_ENVIRONMENT', 'development')
DEV_ENV = ENV == 'development'
TEST_ENV = ENV == 'staging'
PROD_ENV = ENV == 'production'
