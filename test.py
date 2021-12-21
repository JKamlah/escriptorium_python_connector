from escriptorium_connector import EscriptoriumConnector, copy_documents_monitored
import os
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    load_dotenv()
    url = "https://escriptorium.fr"
    username = "bronsonbdevost"
    password = "Huxtud-kyksak-jecbo8"
    conn1 = EscriptoriumConnector(url, username, password)

    load_dotenv()
    url = str(os.getenv("ESCRIPTORIUM_URL"))
    username = str(os.getenv("ESCRIPTORIUM_USERNAME"))
    password = str(os.getenv("ESCRIPTORIUM_PASSWORD"))
    conn2 = EscriptoriumConnector(url, username, password)

    copy_documents_monitored(conn1, conn2, [135], project_name="sofer-mahir-2")
