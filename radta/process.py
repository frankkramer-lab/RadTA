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
import pandas as pd
import numpy as np

#-----------------------------------------------------#
#                  BOA Output Loader                  #
#-----------------------------------------------------#
def load_boa_results(path_boa_outcome):
    # Load BCA results from the BOA outcome Excel
    dt_bca = pd.read_excel(path_boa_outcome, sheet_name="bca-aggregated_measurements")
    # Load TotalSegmentator results from the BOA outcome Excel
    dt_ts = pd.read_excel(path_boa_outcome, sheet_name="regions-statistics")
    # Return dataframes
    return dt_bca, dt_ts

#-----------------------------------------------------#
#              Refine: Missing Body Parts             #
#-----------------------------------------------------#
def refine_ts_missing_bodyparts(dt):
    # delete all rows with no associated body region
    dt_refined = dt.dropna(subset=["BodyRegion"])
    # Return refined dataframe
    return dt_refined

def refine_bca_missing_bodyparts(dt):
    # Identify aggregation tpyes and BCA features
    aggtypes = dt[dt["Present"]==True]["AggregationType"].unique()
    bca_feats = list(set(dt.columns) - set(["BodyPart", "Present", "AggregationType"]))
    # Identify missing body parts
    missing_bps = dt[dt["Present"]==False]["BodyPart"]
    # Create new dataframe for missing body parts with dummy values
    dt_missbps_values = np.full(shape=(len(aggtypes) * len(missing_bps), 
                                       len(bca_feats)), 
                                fill_value=np.nan)
    dt_missbps_bp = missing_bps.repeat(len(aggtypes))
    dt_missbps_aggtypes = list(aggtypes) * len(missing_bps)
    # Reset indices of new dataframe parts
    dt_missbps_po = pd.DataFrame({
                        "BodyPart": dt_missbps_bp,
                        "Present": False,
                        "AggregationType": dt_missbps_aggtypes})
    dt_missbps_po.reset_index(drop=True, inplace=True)
    dt_missbps_pt = pd.DataFrame(dt_missbps_values, columns=bca_feats)
    dt_missbps_pt.reset_index(drop=True, inplace=True)
    # Combine missbp sub-dataframes together
    dt_missbps = pd.concat((dt_missbps_po, dt_missbps_pt), axis=1)
    # Combine with present body parts dataframe
    dt_refined = pd.concat((dt[dt["Present"]==True], dt_missbps),
                           axis=0, ignore_index=True)
    # Return refined dataframe
    return dt_refined

#-----------------------------------------------------#
#                    Restructuring                    #
#-----------------------------------------------------#
def restructure_ts(dt):
    # Delete unnecessary cols
    cols = ["Present"]
    dt = dt.drop(columns=cols)
    # Melt dataframework into Feature-Value
    dt_melted = pd.melt(dt, 
                        id_vars=["ModelName", "BodyRegion"], 
                        value_vars=None,
                        var_name="metric", 
                        value_name="value")
    # Rename columns
    dt_restructured = dt_melted.rename({"ModelName": "model",
                                       "BodyRegion": "feature"},
                                       axis=1)
    # Rename metric quantile naming for better filtering later
    dt_restructured["metric"].replace({"25thPercentileHU": "Q1_HU",
                                       "75thPercentileHU": "Q3_HU",
                                       "VolumeMl": "Volume_ml",
                                       "MeanHU": "Mean_HU",
                                       "StdHU": "Std_HU",
                                       "MinHU": "Min_HU",
                                       "MaxHU": "Max_HU",
                                       "MedianHU": "Median_HU"},
                                       inplace=True)
    # Return restructured dataframe
    return dt_restructured

def restructure_bca(dt):
    # Delete unnecessary cols
    cols = ["Present"]
    dt = dt.drop(columns=cols)
    # Melt dataframework into Feature-Value
    dt_melted = pd.melt(dt, 
                        id_vars=["BodyPart", "AggregationType"], 
                        value_vars=None,
                        var_name="type", 
                        value_name="value")
    # Combine body part and type
    dt_melted["feature"] = dt_melted["BodyPart"] + "-" + dt_melted["type"]
    # Rename columns
    dt_restructured = dt_melted.rename({"AggregationType": "metric"},
                                       axis=1)
    # Delete unnecessary cols
    cols = ["BodyPart", "type"]
    dt_restructured = dt_restructured.drop(columns=cols)
    # Restructure dataframe
    dt_restructured["model"] = "BCA"
    dt_restructured = dt_restructured[["model", "feature", "metric", "value"]]
    # Rename metric quantile naming for better filtering later
    dt_restructured["metric"] = dt_restructured["metric"].str.replace("mL", "ml")
    dt_restructured["metric"] = dt_restructured["metric"].str.replace("Sum", "Volume")
    # Return restructured dataframe
    return dt_restructured

#-----------------------------------------------------#
#               Merge BOA Feature Tables              #
#-----------------------------------------------------#
def merge_feature_tables(dt_pre_ts, dt_pre_boa,
                         dt_post_ts, dt_post_boa):
    # Combine TotalSegmentator and BOA results
    dt_pre = pd.concat([dt_pre_ts, dt_pre_boa], axis=0, ignore_index=True)
    dt_post = pd.concat([dt_post_ts, dt_post_boa], axis=0, ignore_index=True)
    # Combine pre and post datatables
    dt_pre.rename({"value": "volume_pre"}, axis=1, inplace=True)
    dt_post.rename({"value": "volume_post"}, axis=1, inplace=True)
    dt_merged = pd.merge(dt_pre, dt_post, on=["model", "feature", "metric"])
    # Return merged feature table
    return dt_merged

#-----------------------------------------------------#
#                 Compute Differences                 #
#-----------------------------------------------------#
def compute_differences(dt_merged):
    # compute absolute difference
    dt_merged["diff_absolute"] = dt_merged["volume_post"] - dt_merged["volume_pre"]
    # compute relative difference
    dt_merged["diff_relative"] = dt_merged["diff_absolute"] / dt_merged["volume_pre"]
    dt_merged["diff_relative"] = dt_merged["diff_relative"] * 100
    # Return feature table with differences
    return dt_merged

#-----------------------------------------------------#
#                 Process BOA Results                 #
#-----------------------------------------------------#
def process_boa_results(boa_pre, boa_post):
    # Load boa results
    dt_pre_bca, dt_pre_ts = load_boa_results(boa_pre)
    dt_post_bca, dt_post_ts = load_boa_results(boa_post)

    # Refine model: TotalSegmentator
    dt_pre_ts = refine_ts_missing_bodyparts(dt_pre_ts)
    dt_post_ts = refine_ts_missing_bodyparts(dt_post_ts)
    # Refine model: BCA
    dt_pre_bca = refine_bca_missing_bodyparts(dt_pre_bca)
    dt_post_bca = refine_bca_missing_bodyparts(dt_post_bca)

    # Restructure: TotalSegmentator
    dt_pre_ts = restructure_ts(dt_pre_ts)
    dt_post_ts = restructure_ts(dt_post_ts)
    # Restructure: BCA
    dt_pre_bca = restructure_bca(dt_pre_bca)
    dt_post_bca = restructure_bca(dt_post_bca)

    # Merge BOA feature tables 
    dt_merged = merge_feature_tables(dt_pre_ts, dt_pre_bca, 
                                     dt_post_ts, dt_post_bca)
    
    # Compute differences between pre and post radiomics
    dt_proc = compute_differences(dt_merged)

    # Return processed BOA results
    return dt_proc
