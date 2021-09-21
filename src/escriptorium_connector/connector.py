from io import BufferedReader
from typing import Union
import requests
import logging
import backoff
import websocket
import json

logger = logging.getLogger(__name__)


class EscriptoriumConnector:
    def __init__(
        self,
        base_url: str,
        api_url: str,
        token: str,
        cookie: str = None,
        project: str = None,
    ):
        # Make sure the urls terminates with a front slash
        self.api_url = api_url if api_url[-1] == "/" else api_url + "/"
        self.base_url = base_url if base_url[-1] == "/" else base_url + "/"

        self.headers = {"Accept": "application/json", "Authorization": f"Token {token}"}
        self.project = project
        self.cookie = cookie

    def __on_message(self, ws, message):
        logging.debug(message)

    def __on_error(self, ws, error):
        logging.debug(error)

    def __on_close(self, ws, close_status_code, close_msg):
        logging.debug("### websocket closed ###")
        logging.debug(close_status_code)
        logging.debug(close_msg)

    def __on_open(self, ws):
        logging.debug("### websocket opened ###")

        # def run(*args):
        #     for i in range(3):
        #         time.sleep(1)
        #         ws.send("Hello %d" % i)
        #     time.sleep(1)
        #     ws.close()
        #     print("thread terminating...")

        # thread.start_new_thread(run, ())

    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_time=60)
    def __get_url(self, url: str) -> requests.Response:
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r

    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_time=60)
    def __post_url(
        self, url: str, payload: object, files: object = None
    ) -> requests.Response:
        r = (
            requests.post(url, data=payload, files=files, headers=self.headers)
            if files is not None
            else requests.post(url, data=payload, headers=self.headers)
        )
        r.raise_for_status()
        return r

    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_time=60)
    def __put_url(
        self, url: str, payload: object, files: object = None
    ) -> requests.Response:
        r = (
            requests.put(url, data=payload, files=files, headers=self.headers)
            if files is not None
            else requests.put(url, data=payload, headers=self.headers)
        )
        r.raise_for_status()
        return r

    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_time=60)
    def __delete_url(self, url: str) -> requests.Response:
        r = requests.delete(url, headers=self.headers)
        r.raise_for_status()
        return r

    def get_documents(self):
        r = self.__get_url(f"{self.api_url}documents/")
        info = r.json()
        documents = info["results"]
        while info["next"] is not None:
            r = self.__get_url(info["next"])
            info = r.json()
            documents = documents + info["results"]

        return documents

    def get_document(self, pk: int):
        r = self.__get_url(f"{self.api_url}documents/{pk}/")
        return r.json()

    def get_document_parts(self, doc_pk: int):
        return self.get_document_images(doc_pk)

    def get_document_part(self, doc_pk: int, part_pk: int):
        r = self.__get_url(f"{self.api_url}documents/{doc_pk}/parts/{part_pk}/")
        return r.json()

    def get_document_part_line(self, doc_pk: int, part_pk: int, line_pk: int):
        r = self.__get_url(
            f"{self.api_url}documents/{doc_pk}/parts/{part_pk}/lines/{line_pk}/"
        )
        return r.json()

    def get_document_part_region(self, doc_pk: int, part_pk: int, region_pk: int):
        regions = self.get_document_part_regions(doc_pk, part_pk)
        region = [x for x in regions if x["pk"] == region_pk]
        return region[0] if region else None

    def get_document_part_line_transcription(
        self, doc_pk: int, part_pk: int, line_pk: int, line_transcription_pk: int
    ):
        transcriptions = self.get_document_part_line_transcriptions(
            doc_pk, part_pk, line_pk
        )
        transcription = [x for x in transcriptions if x["pk"] == line_transcription_pk]
        return transcription[0] if transcription else None

    def get_document_part_line_transcription_by_transcription(
        self, doc_pk: int, part_pk: int, line_pk: int, transcription_pk: int
    ):
        transcriptions = self.get_document_part_line_transcriptions(
            doc_pk, part_pk, line_pk
        )
        transcription = [
            x for x in transcriptions if x["transcription"] == transcription_pk
        ]
        return transcription[0] if transcription else None

    def get_document_part_line_transcriptions(
        self, doc_pk: int, part_pk: int, line_pk: int
    ):
        line = self.get_document_part_line(doc_pk, part_pk, line_pk)
        return line["transcriptions"]

    def get_document_part_regions(self, doc_pk: int, part_pk: int):
        r = self.__get_url(f"{self.api_url}documents/{doc_pk}/parts/{part_pk}")
        part = r.json()
        return part["regions"]

    def get_document_transcription(self, doc_pk: int, transcription_pk: int):
        r = self.__get_url(
            f"{self.api_url}documents/{doc_pk}/transcriptions/{transcription_pk}"
        )
        return r.json()

    def create_document_transcription(self, doc_pk: int, transcription_name: str):
        r = self.__post_url(
            f"{self.api_url}documents/{doc_pk}/transcriptions/",
            {"name": transcription_name},
        )
        return r.json()

    def get_document_transcriptions(self, doc_pk: int):
        r = self.__get_url(f"{self.api_url}documents/{doc_pk}/transcriptions/")
        return r.json()

    def download_part_alto_transcription(
        self,
        document_pk: int,
        part_pk: int,
        transcription_pk: int,
    ) -> Union[bytes, None]:
        if self.cookie is None:
            raise Exception("Must use websockets to download ALTO exports")

        download_link = None
        ws = websocket.WebSocket()
        ws.connect(
            f"{self.base_url.replace('http', 'ws')}ws/notif/", cookie=self.cookie
        )
        self.__post_url(
            f"{self.api_url}documents/{document_pk}/export/",
            {
                "task": "export",
                "document": document_pk,
                "parts": part_pk,
                "transcription": transcription_pk,
                "file_format": "alto",
            },
        )

        message = ws.recv()
        ws.close()
        logging.debug(message)
        msg = json.loads(message)
        if "export" in msg["text"].lower():
            for entry in msg["links"]:
                if entry["text"].lower() == "download":
                    download_link = entry["src"]

        if download_link is None:
            logging.warning(
                f"Did not receive a link to download ALTO export for {document_pk}, {part_pk}, {transcription_pk}"
            )
            return None

        alto_request = self.__get_url(f"{self.base_url}{download_link}")

        if alto_request.status_code != 200:
            return None

        return alto_request.content

    def upload_part_alto_transcription(
        self,
        document_pk: int,
        part_pk: int,
        transcription_name: str,
        filename: str,
        file_data: BufferedReader,
    ):
        return self.__post_url(
            f"{self.api_url}documents/{document_pk}/imports/",
            {
                "task": "import-xml",
                "name": transcription_name,
                "document": document_pk,
                "parts": part_pk,
            },
            {"upload_file": (filename, file_data)},
        )

    def get_document_part_lines(self, doc_pk: int, part_pk: int):
        r = self.__get_url(f"{self.api_url}documents/{doc_pk}/parts/{part_pk}/lines/")
        line_info = r.json()
        lines = line_info["results"]
        while line_info["next"] is not None:
            r = self.__get_url(line_info["next"])
            line_info = r.json()
            lines = lines + line_info["results"]

        return lines

    def delete_document_part_line(self, doc_pk: int, part_pk: int, line_pk: int):
        r = self.__delete_url(
            f"{self.api_url}documents/{doc_pk}/parts/{part_pk}/lines/{line_pk}"
        )
        return r

    def get_document_images(self, document_pk: int):
        r = self.__get_url(f"{self.api_url}documents/{document_pk}/parts/")
        image_info = r.json()
        image_names = image_info["results"]
        while image_info["next"] is not None:
            r = self.__get_url(image_info["next"])
            image_info = r.json()
            image_names = image_names + image_info["results"]

        return image_names

    def delete_document_parts(self, document_pk: int, start: int, end: int):
        parts = self.get_document_images(document_pk)
        for part in parts[start:end]:
            r = self.__delete_url(
                f'{self.api_url}documents/{document_pk}/parts/{part["pk"]}/'
            )

    def get_image(self, img_url: str):
        r = self.__get_url(f"{self.base_url}{img_url}")
        return r.content

    def create_document(self, doc_data: object):
        if self.project:
            doc_data["project"] = self.project
        return self.__post_url(f"{self.api_url}documents/", doc_data)

    def create_image(
        self, document_pk: int, image_data_info: object, image_data: bytes
    ):
        return self.__post_url(
            f"{self.api_url}documents/{document_pk}/parts/",
            image_data_info,
            {"image": (image_data_info["filename"], image_data)},
        )


if __name__ == "__main__":
    source_url = "https://www.escriptorium.fr/"
    source_api = f"{source_url}api/"
    source_token = ""
    source = EscriptoriumConnector(source_url, source_api, source_token)
    print(source.get_documents())
