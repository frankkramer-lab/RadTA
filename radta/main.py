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
from cli import parse_arguments
from boa import run_boa

#-----------------------------------------------------#
#                     radTA Runner                    #
#-----------------------------------------------------#
if __name__ == "__main__":
    # Parse arguments via CI
    path_vol_pre, path_vol_post, path_boa, path_output = parse_arguments()
    # Run TotalSegmentator and BOA
    run_boa(path_vol_pre, path_vol_post, path_boa, path_output)

    # proc: load results from boa
    # proc: transform them in better format
    # proc: store volA, volB formated results in output directory
    # proc: compute difference between volA, volB
    # proc: store difference in output directory
    # eval: compute plots (dynamically with plotly in which you can select the feature?)

