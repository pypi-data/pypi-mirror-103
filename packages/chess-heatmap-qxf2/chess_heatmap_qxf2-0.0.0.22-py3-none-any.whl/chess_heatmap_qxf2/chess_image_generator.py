"""
This module is used to represent the control logic data in 2-dimensional form.
The data values are represented as colors in the graph.
"""

import base64
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

class ChessImageGenerator:
    "Class to create the gif"

    @staticmethod
    def create_gif(game_data):
        "Prepare the rows and columns for the graph"
        matplotlib.use('agg')

        if game_data is None or len(game_data["white"])==0:
            print("Doing nothing for this game")
            return None

        gamedata_mapwhite = game_data["white"]
        gamedata_mapblack = game_data["black"]

        filename = game_data["filename"]

        gamemax_controlwhite = game_data["max_white_value"]
        gamemax_controlblack = game_data["max_black_value"]

        xlabels = ["a", "b", "c", "d", "e", "f", "g", "h"]
        ylabels = ["8", "7", "6", "5", "4", "3", "2", "1"]

        colors_full = ["#EFFAF1","#B5E3C5","#74C69D","#40916C",
        "#245640","#0C1D15","#081C15","#173A2C","#112C21","#0B1D16","#060F0B","#04100C"]

        boundaries_full = [0,1,2,3,4,5,6,7,8,9,10]

        colors = []
        boundaries = []

        i=0
        while i<=gamemax_controlwhite:
            colors.append(colors_full[i])
            boundaries.append(boundaries_full[i])
            i=i+1
        
        norm = matplotlib.colors.BoundaryNorm(boundaries=boundaries + [boundaries[-1]], ncolors=256)
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
        
        fig, (ax1, ax2) = plt.subplots(1, 2)

        sns.heatmap(gamedata_mapwhite[0],vmax = gamemax_controlwhite,
                    xticklabels=xlabels,yticklabels=ylabels,ax=ax1,cmap=cmap,norm=norm)
        sns.heatmap(gamedata_mapblack[0],vmax = gamemax_controlblack,
                    xticklabels=xlabels,yticklabels=ylabels,ax=ax2,cmap=cmap,norm=norm)

        def animate(i):
            """Create a single animated gif containing the heatmaps for all the
            different plys in a single game"""
            ax1.cla()
            ax2.cla()
            sns.heatmap(gamedata_mapwhite[i],vmax = gamemax_controlwhite,
                        xticklabels=xlabels,yticklabels=ylabels,ax=ax1,
                        cbar=None,cmap=cmap,norm=norm)
            sns.heatmap(gamedata_mapblack[i],vmax = gamemax_controlblack,
                        xticklabels=xlabels,yticklabels=ylabels,ax=ax2,
                        cbar=None,cmap=cmap,norm=norm)

        anim = animation.FuncAnimation(fig, animate, interval=1000,
                                        save_count=len(gamedata_mapwhite))
        anim.save(filename + ".gif", dpi=80, writer='imagemagick')
        file_handle = open(filename + ".gif", 'rb')
        return {"bytes": base64.b64encode(file_handle.read()), "filename": "resources/output/"
                        + filename + ".gif"}
