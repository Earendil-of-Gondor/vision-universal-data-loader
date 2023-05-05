from llff.poses.pose_utils import minify
import os
from subprocess import check_output
from pathlib import Path

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--basedir', type=str,
                    help='base directory. resized images will be put into basedir_\{factor\}')
parser.add_argument('--factors', type=str,
                    help='resize factor separated by comma. e.g. 2,4,8')
args = parser.parse_args()


def resize(basedir, factors):
    factors = [int(x) for x in args.factors.split(',')]

    parentdir = Path(basedir).parent.absolute()
    os.chdir(parentdir)
    print('changing cwd to:', parentdir)

    for f in factors:
        outdir = '{}_{}'.format(os.path.basename(basedir), f)  # masks_2
        outdir = os.path.join(parentdir, outdir)  # /dir/.../masks_2
        os.makedirs(outdir, exist_ok=True)
        resizearg = '{}%'.format(int(100./f))  # 50%

        check_output('cp {}/* {}'.format(basedir, outdir), shell=True)

        ext = os.listdir(basedir)[0].split('.')[-1]
        args = ' '.join(['mogrify', '-resize', resizearg,
                         '-format', 'png', '*.{}'.format(ext)])
        print(args)
        wd = os.getcwd()
        os.chdir(outdir)
        check_output(args, shell=True)
        os.chdir(wd)


if __name__ == '__main__':
    resize(args.basedir, args.factors)
