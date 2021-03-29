from AnalysisToolkit import AnalysisToolkit
import numpy as np
import cv2
from collections import defaultdict
import matplotlib.pyplot as plt

class PerfectMemory(AnalysisToolkit):

    def __init__(self, route, vis_deg, rot_deg):
        AnalysisToolkit.__init__(self, route, vis_deg, rot_deg)
        self.model_name = 'PERFECTMEMORY'

    # Rotational Image Difference Function for two views
    def get_view_rIDF(self, view_1, view_2, view_1_heading=0):
        view_1_preprocessed = self.preprocess(view_1)
        view_2_preprocessed = self.preprocess(view_2)
        rIDF = {}
        for i in np.arange(0, self.vis_deg, step=self.rot_deg, dtype=int):
            view_1_rotated = self.rotate(view_1_preprocessed, i)
            mse = np.sum(self.image_difference(view_1_rotated, view_2_preprocessed)**2)
            mse /= float(view_1_preprocessed.shape[0] * view_1_preprocessed.shape[1])
            rIDF[(i + view_1_heading) % self.vis_deg] = mse
        return rIDF

    # Rotational Image Difference Function for a view over a route representation
    def get_route_rIDF(self, view, view_heading=0):
        route_rIDF = defaultdict(list)
        for idx, filename in enumerate(self.route_filenames):
            route_view = cv2.imread(self.route_path + filename)
            [route_rIDF[k].append(v) for k, v in self.get_view_rIDF(view, route_view, view_heading).items()]
        return route_rIDF

    # get the index of the best matching route view to a view given an rIDF for that view
    def get_matched_route_view_idx(self, route_rIDF):
        min_RIDF_idx = {k: (np.amin(v), np.argmin(v)) for k, v in route_rIDF.items()}
        return min(min_RIDF_idx.values())[1]

    # Calculates the signal strength of an rIDF
    def get_signal_strength(self, rIDF):
        return -(min(rIDF.values()) / np.array(list(rIDF.values())).mean())

    # Rotational Familiarity Function
    def get_rFF(self, route_rIDF):
        return {k: -np.amin(v) for k, v in route_rIDF.items()}

    # Get the most familiar heading given an rIDF for a view
    def get_most_familiar_heading(self, rFF):
        return max(rFF, key=rFF.get)


if __name__ == "__main__":
    pm = PerfectMemory(route="ant1_route1", vis_deg=360, rot_deg=2)

    # Database analysis
    # pm.database_analysis(spacing=20, save_data=True)
    # pm.database_analysis(spacing=10, bounds=[[490, 370], [550, 460]], save_data=True)
    # pm.database_analysis(spacing=20, corridor=30, save_data=True)
    one_px_data_path = "DATABASE_ANALYSIS/PERFECTMEMORY/1_deg_px_res/16-3-2021_21-1-3_ant1_route1_140x740_20.csv"
    two_px_data_path = "DATABASE_ANALYSIS/PERFECTMEMORY/2_deg_px_res/16-3-2021_19-52-18_ant1_route1_140x740_20.csv"
    four_px_data_path = "DATABASE_ANALYSIS/PERFECTMEMORY/4_deg_px_res/16-3-2021_17-36-29_ant1_route1_140x740_20.csv"
    eight_px_data_path = "DATABASE_ANALYSIS/PERFECTMEMORY/8_deg_px_res/16-3-2021_19-18-9_ant1_route1_140x740_20.csv"
    sixteen_px_data_path = "DATABASE_ANALYSIS/PERFECTMEMORY/16_deg_px_res/16-3-2021_18-58-18_ant1_route1_140x740_20.csv"
    pm.error_boxplot([one_px_data_path, two_px_data_path, four_px_data_path, eight_px_data_path, sixteen_px_data_path],
                     ["1 degree resolution", "2 degree resolution", "4 degree resolution", "8 degree resolution", "16 degree resolution"],
                     save_data=True)
    four_px_enviro_data_path = "DATABASE_ANALYSIS/PERFECTMEMORY/4_deg_px_res/15-3-2021_22-1-36_ant1_route1_140x740_20.csv"
    pm.error_boxplot([four_px_data_path, four_px_enviro_data_path],
                     ["Within route corridor", "Across environment"],
                     save_data=True)

    # Route view analysis
    # pm.route_analysis(step=100)

    # Off-route view analysis
    # filename = pm.grid_filenames.get((500, 500))
    # grid_view = cv2.imread(pm.grid_path + filename)
    # pm.view_analysis(view_1=grid_view, view_2=grid_view, save_data=False)

    # On-route view analysis
    # idx = 405
    # filename = pm.route_filenames[idx]
    # route_view = cv2.imread(pm.route_path + filename)
    # route_heading = pm.route_headings[idx]
    # pm.view_analysis(view_1=route_view, view_2=route_view, view_1_heading=route_heading, save_data=False)

    # Off-route best matched view analysis
    # pm.best_matched_view_analysis(view_x=610, view_y=810, save_data=True)

    # Off-route real match view analysis
    # pm.ground_truth_view_analysis(view_x=610, view_y=810, save_data=True)