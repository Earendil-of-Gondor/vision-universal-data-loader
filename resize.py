from llff.poses.pose_utils import minify
import os
import subprocess

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--basedir', type=str,
                    help='base directory. should contain an images folder. \
                    resized images will be put into basedir/images_\{factor\}')
parser.add_argument('--factors', type=str,
                    help='resize factor separated by comma. e.g. 2,4,8')
args = parser.parse_args()


def resize(basedir, factors):
    # factors = args.factors.split(',')

    # def copy():

    # def resize_helper(factor):
    #     resize_args = [
    #         "pushd", f"{basedir}/images_{factor}",
    #         "ls", "|", ""
    #     ]
    #     resize_outputs = (subprocess.check_output(
    #         resize_args, universal_newlines=True))
    #     print(resize_outputs)

    resize_args = [
        # "DATASET_PATH", "=", basedir,
        "resize.sh",
    ]
    resize_outputs = (subprocess.check_output(
        resize_args, universal_newlines=True))
    print(resize_outputs)


if __name__ == '__main__':
    resize(args.basedir, args.factors)
