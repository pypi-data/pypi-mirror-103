"""
This module produces a control heatmap for a chess game which shows which side
controls which squares how many times per ply/move in a Chess board
"""
from .chess_util import ChessUtil
from .chess_dask_cluster import ChessDaskCluster
import json
from .chess_image_generator import ChessImageGenerator
from distributed import wait, as_completed
import base64

class ChessControlHeatmap:
    "Class to generate the control heatmap based on the input PGN files"

    dask_cluster = ChessDaskCluster()
    image_futures = []

    def image_handler(self, game_dict):
        if self.dask_cluster.config_values["debug"]:
            print("Completed computation, starting image creation")
            with open('results.json', 'a', encoding='utf-8') as file_handle:
                json.dump(game_dict, file_handle, ensure_ascii=False, indent=4)

        image_future = self.dask_cluster.client.submit(ChessImageGenerator.create_gif, game_dict)
        self.image_futures.append(image_future)

    def generate_heatmap_images(self):
        "Fetches the input from files and starts to analyze the games"
        game_list = ChessUtil.get_games_from_pgn_files()
        self.dask_cluster.analyse_games_in_cluster(game_list, self.image_handler)

        for image_future in as_completed(self.image_futures):
            image_data = image_future.result()
            if image_data is None:
                pass
            with open(image_data["filename"], 'wb') as file_handle:
                file_handle.write(base64.decodebytes(image_data["bytes"]))
                file_handle.close
            print("Successfully created: " + image_data["filename"])


