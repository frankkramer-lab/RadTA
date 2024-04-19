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
from plotnine import *
import patchworklib as pw
import warnings

#-----------------------------------------------------#
#                 Evaluation Function                 #
#-----------------------------------------------------#
def run_eval(path_output):
    # Create evaluation directory
    path_eval = os.path.join(path_output, "evaluation")
    if not os.path.exists(path_eval) : os.mkdir(path_eval)
    # Init merged radiomics table for all volume-pairs
    rt_merged = []
    # Iterate over all radiomics tables
    for rt_file in os.listdir(path_output):
        # Skip any non radiomics table file
        if not rt_file.endswith(".csv") : continue
        # Read radiomics table
        rt = pd.read_csv(os.path.join(path_output, rt_file))
        # Assign volume-pair name to radiomics table
        rt["volume_pair"] = rt_file.split(".")[0]
        # Append to list for merging
        rt_merged.append(rt)
    # Merge list of radiomics tables
    rt_merged = pd.concat(rt_merged, axis=0, ignore_index=True)
    # Store merged radiomics tables
    rt_merged.to_csv(os.path.join(path_eval, "radiomics_table.csv"), index=False)
    # Compute multiple statistical measurements
    diffmean_rel = calc_diffmean(rt_merged, "diff_relative")
    diffmean_abs = calc_diffmean(rt_merged, "diff_absolute")
    ttest = calc_ttest(rt_merged)
    obs = calc_observations(rt_merged)
    # Merge evaluation list together
    dt_eval = pd.merge(diffmean_rel, ttest, on=["model", "feature", "metric"])
    dt_eval = pd.merge(diffmean_abs, dt_eval, on=["model", "feature", "metric"])
    dt_eval = pd.merge(dt_eval, obs, on=["model", "feature", "metric"])
    # Store evaluation table
    dt_eval.to_csv(os.path.join(path_eval, "evaluation_table.csv"), index=False)
    # Plot summary figure as heatmap
    plot_summary(dt_eval, path_eval)
    # # Plot individual analysis figures
    # plot_analysis(rt_merged, dt_eval, path_eval)

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
    feat_group = rt_merged.groupby(["model", 
                                    "feature", 
                                    "metric"])[["volume_pre", "volume_post"]]
    def apply_ttest(x):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x.dropna(axis=0, inplace=True)
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
    dt_counts.rename({"diff_absolute": "observations"}, axis=1, inplace=True)
    return dt_counts

#-----------------------------------------------------#
#                Summary Plot - Heatmap               #
#-----------------------------------------------------#
def plot_summary(dt_eval, path_eval):
    # iterate through models
    for model_name in dt_eval["model"].unique():
        # Create dataframe subset for corresponding model
        dt_model = dt_eval[dt_eval["model"]==model_name]

        # Create and configure significance levels for the ttest
        significance_bins = [0, 0.01, 0.05, 0.1, 1.0]
        significance_names = ["<= " + str(x) for x in significance_bins[1:]]
        significance_names[-1] = "reject"
        significance_colors = ["#4F7942", "#7FFFD4", "#088F8F", "#800020"]
        significance_color_map = {}
        for i, sl in enumerate(significance_names):
            significance_color_map[sl] = significance_colors[i]
        # Apply significance levels to the ttest pvalues
        dt_model["significance"] = pd.cut(dt_model["ttest_pvalue"], 
                                        significance_bins,
                                        labels=significance_names)
        dt_model["significance"] = dt_model["significance"].astype(str)

        # Round relative mean difference
        dt_model["mean_diff_relative"] = dt_model["mean_diff_relative"].round(2)
        dt_model["mean_diff_relative"] = dt_model["mean_diff_relative"].apply(lambda x: "+"+str(x) if x>0 else x)

        # Generate summary figure
        fig = (ggplot(dt_model, aes("metric", "feature", fill="significance"))
                    + geom_tile(color="white", size=1.5)
                    + geom_text(aes("metric", "feature", 
                                    label="mean_diff_relative"), 
                                color="black", size=5.0)
                    # + ggtitle("Radiomic Trend Analysis Evaluation Summary for Model: " + model_name)
                    + labs(title="Radiomic Trend Analysis\n" + \
                            "Evaluation Summary for Model: " + model_name,
                            subtitle="Label: Mean of Relative Difference (in %)\n" + \
                                    "Color: P-value of Paired t-Test")
                    + xlab("Measurement Metric")
                    + ylab("Feature")
                    + scale_fill_manual(values=significance_color_map)
                    + theme_bw()
                    + theme(axis_text_x=element_text(angle = 65, vjust = 1.0,
                                                    hjust = 0.99),
                            legend_title=element_blank(),
                            legend_direction="horizontal", 
                            legend_box="horizontal",
                            legend_position="top", 
                            legend_box_just="left"))

        # Compute height resolution
        n_feat = len(dt_model["feature"].unique()) 
        height = int(round(n_feat / 5.5)) # 5.5 is a magic number (every good tool need magic numbers)

        # Store figure to disk
        filename = "plot.summary." + model_name + ".png"
        fig.save(filename=filename, path=path_eval, 
                 width=8, height=height, dpi=300,
                 limitsize=False)

#-----------------------------------------------------#
#      Analysis Plot - Individual Box+Line Plots      #
#-----------------------------------------------------#
# def plot_analysis(rt_merged, dt_eval, path_eval):
#     # create evaluation analysis directory
#     path_eval_analysis = os.path.join(path_eval, "analysis_figures")
#     if not os.path.exists(path_eval_analysis) : os.mkdir(path_eval_analysis)
#     # Iterate over each feature
#     for feat in dt_eval["feature"].unique():
#         # create subset
#         dt_eval_feat = dt_eval[dt_eval["feature"]==feat]
#         dt_merged_feat = rt_merged[rt_merged["feature"]==feat]
#         # filter out nan rows
#         with warnings.catch_warnings():
#             warnings.simplefilter("ignore")
#             dt_eval_feat.dropna(subset=["mean_diff_absolute"], 
#                                 axis=0, 
#                                 inplace=True)
#             dt_merged_feat.dropna(subset=["volume_pre", "volume_post"], 
#                                   axis=0, 
#                                   inplace=True)
#         # Skip empty feature tables
#         if dt_merged_feat.empty : continue

#         # Generate feature analysis figure - TOP LEFT
#         figtopleft = (ggplot(dt_eval_feat, aes("metric", "mean_diff_relative"))
#                     + geom_boxplot()
#                     + labs(title="Boxplot - Mean Relative Difference: " + feat)
#                     + xlab("")
#                     + ylab("Mean Relative Difference")
#                     + facet_wrap("metric", scales = "free")
#                     + theme_bw()
#                     + theme(legend_text=element_text(size=1)))
#         # Generate feature analysis figure - TOP LEFT
#         figtopright = (ggplot(dt_eval_feat, aes("metric", "mean_diff_absolute"))
#                     + geom_boxplot()
#                     + labs(title="Boxplot - Mean Absolute Difference: " + feat)
#                     + xlab("")
#                     + ylab("Mean Absolute Difference")
#                     + facet_wrap("metric", scales = "free")
#                     + theme_bw()
#                     + theme(legend_text=element_text(size=1)))

#         # Generate feature analysis figure - BOTTOM
#         figbot = (ggplot(dt_merged_feat, aes("volume_pre", "volume_post"))
#                     + geom_point(size=0.5, color="royalblue")
#                     + geom_abline(intercept=1, linetype="dashed", size=0.5)
#                     + labs(title="Direct Comparison: " + feat)
#                     + xlab("Pre-Volume: Measurement")
#                     + ylab("Post-Volume: Measurement")
#                     + facet_wrap("metric", scales = "free")
#                     + theme_bw()
#                     + theme(legend_text=element_text(size=1)))

#         # Multi-plot Call
#         g1 = pw.load_ggplot(figtopleft, figsize=(4,4))
#         g2 = pw.load_ggplot(figtopright, figsize=(4,4))
#         gbot = pw.load_ggplot(figbot, figsize=(8,4))
#         g12b = (g1|g2)/gbot
#         path_fig = os.path.join(path_eval_analysis,
#                                 "plot.analysis." + feat + ".png")
#         g12b.savefig(path_fig)

#-----------------------------------------------------#
#               Debugging               #
#-----------------------------------------------------#
if __name__ == "__main__":
    run_eval("radta.out3")
