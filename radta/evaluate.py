#==============================================================================#
#  Author:       Dominik Müller 1, Hannes Ulrich 2                             #
#  Copyright:    2024                                                          #
#                1 Research group: Reliable AI-driven Medical Image Analysis,  #
#                  University of Augsburg, University Hospital Augsburg        #
#                2 Junior research group: IMPETUS, University Hospital Kiel    #
#                                                                              #
#  This program is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#==============================================================================#
#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import os
import pandas as pd
from scipy import stats

#-----------------------------------------------------#
#               Evaluation Function               #
#-----------------------------------------------------#
def run_eval(path_output):
    # Init merged radiomics table for all volume-pairs
    rt_merged = []
    # Iterate over all radiomics tables
    for rt_file in os.listdir(path_output):
        # Skip any non radiomics table file
        if not rt_file.endswith(".csv") : continue
        # Read radiomics table
        rt = pd.read_csv(os.path.join(path_output, rt_file))
        # Assign volume-pair name to radiomics table
        rt["volumes"] = rt_file.split(".")[0]
        # Append to list for merging
        rt_merged.append(rt)
    # Merge list of radiomics tables
    rt_merged = pd.concat(rt_merged, axis=0, ignore_index=True)
    # Compute multiple statistical measurements
    diffmean_rel = calc_diffmean(rt_merged, "diff_relative")
    diffmean_abs = calc_diffmean(rt_merged, "diff_absolute")
    ttest = calc_ttest(rt_merged)
    obs = calc_observations(rt_merged)
    # Merge evaluation list together
    dt_eval = pd.merge(diffmean_rel, ttest, on=["model", "feature", "metric"])
    dt_eval = pd.merge(diffmean_abs, dt_eval, on=["model", "feature", "metric"])
    dt_eval = pd.merge(dt_eval, obs, on=["model", "feature", "metric"])

    print(dt_eval)
    dt_eval.to_csv("test.csv")

#-----------------------------------------------------#
#               Statistical Measurements              #
#-----------------------------------------------------#
def calc_diffmean(rt_merged, feat):
    observations = rt_merged.groupby(["model", 
                                    "feature", 
                                    "metric"])[feat].mean(numeric_only=True)
    dt_diffmean = observations.to_frame().reset_index()
    dt_diffmean.rename({feat: "mean_" + feat}, axis=1, inplace=True)
    return dt_diffmean

def calc_ttest(rt_merged):
    print(rt_merged)
    feat_group = rt_merged.groupby(["model", 
                                    "feature", 
                                    "metric"])[["volume_pre", "volume_post"]]
    def apply_ttest(x):
        t_statistic, p_value = stats.ttest_rel(x["volume_pre"], 
                                               x["volume_post"],
                                               nan_policy="propagate")
        return pd.Series([t_statistic, p_value], index=["ttest_statistic",
                                                        "ttest_pvalue"])
    dt_ttest = feat_group.apply(apply_ttest)
    dt_ttest= dt_ttest.reset_index()
    return dt_ttest

def calc_observations(rt_merged):
    observations = rt_merged.groupby(["model", 
                                      "feature", 
                                      "metric"])["diff_relative"].count()
    dt_counts = observations.to_frame().reset_index()
    dt_counts.rename({"diff_relative": "observations"}, axis=1, inplace=True)
    return dt_counts


# wasserstein distance


# SUMMARY PLOT:
# HEATMAP plot per model
#   -> y-axis: feature
#   -> x-axis: metric
#   -> coloring : ttest-pvalue (boolean?? - continous would be cool too? maybe clip to 0-0.5)
#   -> text-value : mean_diff_relative

# For each feature individual:
#   -> facet_wrap plot for each metric
#   -> Title Description: ttest, ttest_statistic, observations
#   -> LEFT: boxplot of mean_diff_relative
#   -> RIGHT: boxplot of mean_diff_absolute
#   -> BOTTOM: Scatter plot of volume_a vs volume_b 

#-----------------------------------------------------#
#               Debugging               #
#-----------------------------------------------------#
if __name__ == "__main__":
    run_eval("radta.out2")
