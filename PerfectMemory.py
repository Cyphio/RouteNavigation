from AnalysisToolkit import AnalysisToolkit
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
from collections import defaultdict

class PerfectMemory(AnalysisToolkit):

    def __init__(self, route, vis_deg, rot_deg):
        AnalysisToolkit.__init__(self, route, vis_deg, rot_deg)
        self.model_name = 'PERFECTMEMORY'

    # Perfect Memory Rotational Image Difference Function
    def RIDF(self, curr_view, route_view, route_view_heading=0):
        RIDF = {}
        for i in np.arange(0, self.vis_deg, step=self.rot_deg, dtype=int):
            rotated_view = np.roll(curr_view, int(curr_view.shape[1] * (i / self.vis_deg)), axis=1)
            mse = np.sum(self.image_difference(route_view, rotated_view))
            mse /= float(route_view.shape[0] * route_view.shape[1])
            RIDF[(i + route_view_heading) % self.vis_deg] = mse
        return RIDF

if __name__ == "__main__":
    pm = PerfectMemory(route="ant1_route3", vis_deg=360, rot_deg=4)

    # Database analysis
    # pm.database_analysis(spacing=10, bounds=[[600, 800], [650, 850]], save_data=False)
    # pm.database_analysis(spacing=30, save_data=False)

    # Route view analysis
    pm.route_analysis(step=100)

    # Grid view analysis
    # idx = 75
    # filename = pm.grid_data['Filename'].iloc[idx]
    # filename = "image_+005300_+005200_+001800.png"
    # grid_view = pm.downsample(cv2.imread(pm.grid_path + filename))
    # pm.view_analysis(curr_view=grid_view, save_data=False)

    # On-route view analysis
    idx = 0
    # filename = pm.route_filenames[idx]
    # route_view = pm.downsample(cv2.imread(pm.route_path + filename))
    # route_view_heading = pm.route_headings[idx]
    # pm.view_analysis(curr_view=route_view, curr_heading=route_view_heading, save_data=False)