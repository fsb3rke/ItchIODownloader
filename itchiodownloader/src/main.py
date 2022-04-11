import infoInt
from sys import argv

client = infoInt.InfoClient("info")

game_id = client.get_game_id(argv[1])
game_name = client.get_game_file_name(game_id)
game_download_link = client.get_game_download_link(game_id)

client.download(game_id, game_name, game_download_link)
