class config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://vijay:2553@localhost/flask"
    JWT_SECRET_KEY = "secret"
    JWT_TOKEN_LOCATION= ["cookies"]  # Use cookies instead of headers
    JWT_ACCESS_COOKIE_NAME = "access_token"  # Name of the cookie
    JWT_COOKIE_SECURE = False  # Set True in production (HTTPS only)
    JWT_COOKIE_CSRF_PROTECT = False