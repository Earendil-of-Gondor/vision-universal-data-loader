import argparse
from glob import glob
import os
import sys
import shutil
from video2images import run_ffmpeg
from llff.poses.pose_utils import gen_poses


def parse_args():
    parser = argparse.ArgumentParser(description=".")

    parser.add_argument("--basedir")
    parser.add_argument("--outdir", default="")
    parser.add_argument("--output_type", default=0,
                        help="0 for nerf; 1 for nerd; 2 for instant-npg")

    parser.add_argument("--video_fps", default=2)
    parser.add_argument("--time_slice", default="", help="Time (in seconds) in the format t1,t2 within which the images should be generated from the video. E.g.: \"--time_slice '10,300'\" will generate images only from 10th second to 300th second of the video.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Do not ask for confirmation for overwriting existing images and COLMAP data.")

    parser.add_argument('--match_type', type=str,
                        default='exhaustive_matcher', help='type of matcher used.  Valid options: \
					exhaustive_matcher sequential_matcher.  Other matchers not supported at this time')

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    if args.match_type != 'exhaustive_matcher' and args.match_type != 'sequential_matcher':
        print('ERROR: matcher type ' + args.match_type +
              ' is not valid.  Aborting')
        sys.exit()

    if args.basedir == "":
        print('ERROR: base folder is not specified. Aborting')
        sys.exit()

    if args.outdir == "":
        args.outdir = args.basedir
    img_folder = os.path.join(args.basedir, "images")

    if not os.path.exists(img_folder):
        print("no images found, looking for video")
        videos = [os.path.join(args.basedir, f) for f in sorted(
            os.listdir(args.basedir))]  # paths sorted by name
        videos = [f for f in videos if any(
            [f.endswith(ex) for ex in ['mov', 'mp4']])]  # filter video format

        if len(videos):
            video = videos[0]
            print('Found video: ', video, ". running ffmpeg")
            args.video_in = video
            args.images = img_folder
            run_ffmpeg(args)
        else:
            print('ERROR: no video found. Aborting')
            sys.exit()

    gen_poses(args.basedir, args.match_type)
