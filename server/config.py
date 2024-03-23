from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

SERIAL_PORT = environ.get("SERIAL_PORT", "/dev/ttyACM0")
SERIAL_BAUDRATE = int(environ.get("SERIAL_BAUDRATE", 9600))

CAMERA_WIDTH = int(environ.get("CAMERA_WIDTH", 176))
CAMERA_HEIGHT = int(environ.get("CAMERA_HEIGHT", 144))

DATABASE_FILE = environ.get("DATABASE_FILE", "database.json")
