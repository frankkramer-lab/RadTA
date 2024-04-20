#==============================================================================#
#  Author:       Dominik Müller 1, Hannes Ulrich 2                             #
#  Copyright:    2024                                                          #
#                1 Research group: Reliable AI-driven Medical Image Analysis,  #
#                  University of Augsburg, University Hospital Augsburg        #
#                2 Junior research group: IMPETUS, University Hospital         #
#                  Schleswig-Holstein                                          #
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
from pathlib import Path
from body_organ_analysis.commands import analyze_ct

#-----------------------------------------------------#
#                    BOA Connector                    #
#-----------------------------------------------------#
def run_boa(vol_pre, vol_post, path_out):
    # create working directory if not existend
    if not path_out.exists() : os.mkdir(path_out)
    # define boa output directories for each volume
    name_pre = str(vol_pre).split("/")[-1].split(".")[0] + ".boa.pre"
    path_out_pre = Path(os.path.join(path_out, name_pre))
    name_post = str(vol_post).split("/")[-1].split(".")[0] + ".boa.post"
    path_out_post = Path(os.path.join(path_out, name_post))

    # Define nnU-Net config
    os.environ["nnUNet_USE_TRITON"] = "0"

    # Run BOA for volume pre
    analyze_ct(
        input_folder=vol_pre,
        processed_output_folder=path_out_pre,
        excel_output_folder=path_out_pre,
        models=["total","bca"],
        total_preview=False,
        bca_pdf=False
    )

    # Run BOA for volume post
    analyze_ct(
        input_folder=vol_post,
        processed_output_folder=path_out_post,
        excel_output_folder=path_out_post,
        models=["total","bca"],
        total_preview=False,
        bca_pdf=False
    )

    # Return pathes to BOA outcome excel files
    path_boa_out_pre = os.path.join(path_out_pre, "output.xlsx")
    path_boa_out_post = os.path.join(path_out_post, "output.xlsx")
    return path_boa_out_pre, path_boa_out_post