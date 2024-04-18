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
from pathlib import Path
from cli import parse_arguments
from boa import run_boa
from process import process_boa_results
from evaluate import run_eval

#-----------------------------------------------------#
#                     radTA Runner                    #
#-----------------------------------------------------#
if __name__ == "__main__":
    # Parse arguments via CI
    input_vol_pre, input_vol_post, path_output, mode_single = parse_arguments()
        
    # Process queue
    for i in range(0, len(input_vol_pre)):
        # Get next volumes from the queue
        path_vol_pre = input_vol_pre[i]
        path_vol_post = input_vol_post[i]

        # Run TotalSegmentator and BOA
        pboa_pre, pboa_post = run_boa(path_vol_pre, path_vol_post, path_output)
        # Load and parse BOA results into a feature table
        dt_ft = process_boa_results(pboa_pre, pboa_post)

        # Store radiomics table including differences
        name_pre = str(path_vol_pre).split("/")[-1].split(".")[0]
        name_post = str(path_vol_post).split("/")[-1].split(".")[0]
        if name_pre != name_post:
            path_out_diff = os.path.join(path_output, name_pre + "-" + name_post)
        else:
            path_out_diff = os.path.join(path_output, name_pre)
        dt_ft.to_csv(path_out_diff + ".csv", index=False)

    # If directory mode, run evaluation
    if not mode_single : run_eval(path_output)

    # eval: compute plots (dynamically with plotly in which you can select the feature?)

