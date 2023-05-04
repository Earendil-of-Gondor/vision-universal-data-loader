from llff.poses.pose_utils import minify
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--basedir', type=str,
                    help='base directory. should contain an images folder. \
                    resized images will be put into basedir/images_\{factor\}')
parser.add_argument('--factors', type=str,
                    help='resize factor separated by comma. e.g. 2,4,8')
args = parser.parse_args()


def resize(basedir, factors):
    factors = args.factors.split(',')
    minify(basedir, factors)


if __name__ == '__main__':
    resize(args.basedir, args.factors)
