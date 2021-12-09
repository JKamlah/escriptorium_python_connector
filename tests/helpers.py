# region global setup

from dotenv import load_dotenv
import os
import sys

sys.path.append("../src")
from escriptorium_connector import EscriptoriumConnector

load_dotenv()
url = os.getenv("ESCRIPTORIUM_URL")
username = os.getenv("ESCRIPTORIUM_USERNAME")
password = os.getenv("ESCRIPTORIUM_PASSWORD")

if url is None or username is None or password is None:
    sys.exit()


def get_connector() -> EscriptoriumConnector:
    return EscriptoriumConnector(url, username, password)


# endregion
