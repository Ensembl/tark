import tark.settings.env
# Make this unique, and don't share it with anybody.
SECRET_KEY = '(=tzgu^(%+h6g9q!e3t7ne-m_+w3i8=w#k$r2so0)tl56b##6y'

if tark.settings.env.TEST_ENV:
    DATABASE_USER = 'prem'
    DATABASE_PASSWORD = 'prem'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '3306'
else:
    DATABASE_USER = 'prem'
    DATABASE_PASSWORD = 'prem'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '3306'
