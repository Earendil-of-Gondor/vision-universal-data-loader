from llff.poses.pose_utils import minify
import os
from subprocess import check_output
from pathlib import Path

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--imgdir', type=str,
                    help='image directory. resized images will be put into same parent directory')
parser.add_argument('--factors', type=str,
                    help='resize factor separated by comma. e.g. 2,4,8')
parser.add_argument('--overwrite', action='store_true',
                    help='whether to overwrite if directory of a certain factor exists')
args = parser.parse_args()


def resize(imgdir, factors, overwrite=True):
    '''
    '''
    factors = [int(x) for x in factors.split(',')]

    parentdir = Path(imgdir).parent.absolute()
    os.chdir(parentdir)
    print('changing cwd to:', parentdir)

    for f in factors:
        outdir = '{}_{}'.format(os.path.basename(
            os.path.normpath(imgdir)), f)  # masks_2
        outdir = os.path.join(parentdir, outdir)  # /dir/.../masks_2
        if not os.path.exists(outdir) or overwrite:
            os.makedirs(outdir, exist_ok=True)
            print('resize factor: ', f, '. to: ', outdir)

            resizearg = '{}%'.format(int(100./f))  # 50%
            check_output('cp {}/* {}'.format(imgdir, outdir), shell=True)

            ext = os.listdir(imgdir)[0].split('.')[-1]
            args = ' '.join(['mogrify', '-resize', resizearg,
                             '-format', 'png', '*.{}'.format(ext)])
            print(args)

            wd = os.getcwd()
            os.chdir(outdir)
            check_output(args, shell=True)
            os.chdir(wd)


if __name__ == '__main__':
    resize(args.imgdir, args.factors, args.overwrite)
