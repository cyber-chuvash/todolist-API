import tempfile

TESTING = True

DB_CONNECT_URL = "sqlite:///" + tempfile.NamedTemporaryFile(suffix='.sqlite').name
DB_ECHO = False
