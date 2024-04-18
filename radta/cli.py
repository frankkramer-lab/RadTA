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
import argparse
from pathlib import Path
import os

#-----------------------------------------------------#
#               Command Line Interface                #
#-----------------------------------------------------#
def parse_arguments():
    # Initialize CLI
    parser = argparse.ArgumentParser(description="CLI for radTA: Radiomics Trend Analysis for CT scans")

    # Required arguments
    parser.add_argument("-va", "--vol_pre", 
                        type=Path,
                        help="Path to pre volume(s) file or directory with multiple volumes", 
                        required=True,
                        dest="vol_pre")
    parser.add_argument("-vb", "--vol_post", 
                        type=Path,
                        help="Path to post volume(s) file or directory with multiple volumes",
                        required=True,
                        dest="vol_post")

    # Optional arguments
    parser.add_argument("-o", "--output", 
                        type=Path,
                        help="Path to evaluation output directory",
                        default="out/",
                        dest="path_output")

    # Parse arguments
    args = parser.parse_args()

    # Check if both inputs exist
    if not args.vol_pre.exists() or not args.vol_post.exists():
        raise ValueError("radTA: One or both of the input pathes do not exist.")

    # Check if input volumes are files or directories
    if args.vol_pre.is_file() and args.vol_post.is_file():
        mode_single = True
    elif args.vol_pre.is_dir() and args.vol_post.is_dir():
        mode_single = False
    else : raise ValueError("radTA: Inputs must be both files or directories.")

    # Parse volume queue for single file and directory mode
    if mode_single:
        queue_vol_pre = [args.vol_pre]
        queue_vol_post = [args.vol_post]
    else:
        queue_vol_pre = []
        queue_vol_post = []
        for x in os.listdir(args.vol_pre):
            queue_vol_pre.append(Path(os.path.join(args.vol_pre, x)))
            queue_vol_post.append(Path(os.path.join(args.vol_post, x)))

    # Return arguments
    return queue_vol_pre, queue_vol_post, args.path_output, mode_single