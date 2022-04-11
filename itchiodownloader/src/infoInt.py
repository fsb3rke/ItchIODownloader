import json
import requests
import os
import time

class InfoClient:
    def __init__(self, info_file_name:str):
        self.__filename = info_file_name

    def __get_json(self, url:str):
        response = requests.get(url)
        return response.json()

    def get_api_key(self):
        file = open(f"info/{self.__filename}.json", "r").read()
        parsed_file = json.loads(file)
        return parsed_file["api_key"]

    def get_game_id(self, game_url:str):
        return InfoClient.__get_json(self, f"{game_url}/data.json")["id"]

    def get_game_download_link(self, game_id:str):
        upload_curl_json = InfoClient.__get_json(self, f"https://itch.io/api/1/{InfoClient.get_api_key(self)}/game/{game_id}/uploads")
        upload_id = upload_curl_json["uploads"][0]["id"]

        download_command = InfoClient.__get_json(self,  f"https://itch.io/api/1/{InfoClient.get_api_key(self)}/upload/{upload_id}/download")

        return download_command["url"]

    def get_game_file_name(self, game_id:str):
        info = InfoClient.__get_json(self, f"https://itch.io/api/1/{InfoClient.get_api_key(self)}/game/{game_id}/uploads")
        fileName = info["uploads"][0]["filename"]
        return fileName

    def download(self, game_id, game_name, downloadurl):
        response = requests.get(downloadurl)
        if response.status_code == 200:
            print(f"{game_name} downloading...")
            download_start_time = time.time()
            open(game_name, "wb").write(response.content)
            download_end_time = abs(download_start_time - time.time())
            print(f"{game_name} has been downloaded. ({download_end_time})")
