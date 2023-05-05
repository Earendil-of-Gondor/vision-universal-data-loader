import os
import subprocess

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--basedir', type=str,
                    help='base directory')
parser.add_argument('--match_type', type=str,
                    default='exhaustive_matcher', help='type of matcher used.  Valid options: \
					exhaustive_matcher sequential_matcher.  Other matchers not supported at this time')
parser.add_argument('--run_until', type=int, default=3,
                    help='1 for feature extractor, 2 for matcher, \
                        3 for sparse mapper, 4 for undistorter, 5 for patch matcher, \
                        6 for fusion, 7 for poisson mesher, 8 for delaunay mesher')
args = parser.parse_args()


def recon(basedir, match_type, run_until=6):
    '''
    run_until specifies where to stop colmap at. 1 for feature extractor, 2 for matcher,
    3 for sparse mapper, 4 for undistorter, 5 for patch matcher, 6 for fusion, 7 for poisson mesher, 
    8 for delaunay mesher
    '''
    logfile_name = os.path.join(basedir, 'colmap_output.txt')
    logfile = open(logfile_name, 'w')

    feature_extractor_args = [
        'colmap', 'feature_extractor',
        '--database_path', os.path.join(basedir, 'database.db'),
        '--image_path', os.path.join(basedir, 'images'),
        '--ImageReader.single_camera', '1',
        '--SiftExtraction.use_gpu', '0',
    ]
    feat_output = (subprocess.check_output(
        feature_extractor_args, universal_newlines=True))
    logfile.write(feat_output)
    print('Features extracted')

    if run_until >= 2:
        exhaustive_matcher_args = [
            'colmap', match_type,
            '--database_path', os.path.join(basedir, 'database.db'),
            '--SiftMatching.use_gpu', '0'
        ]

        match_output = (subprocess.check_output(
            exhaustive_matcher_args, universal_newlines=True))
        logfile.write(match_output)
        print('Features matched')

    if run_until >= 3:
        p = os.path.join(basedir, 'sparse')
        if not os.path.exists(p):
            os.makedirs(p)

        mapper_args = [
            'colmap', 'mapper',
            '--database_path', os.path.join(basedir, 'database.db'),
            '--image_path', os.path.join(basedir, 'images'),
            # --export_path changed to --output_path in colmap 3.6
            '--export_path', os.path.join(basedir, 'sparse'),
            '--Mapper.num_threads', '16',
            '--Mapper.init_min_tri_angle', '4',
            '--Mapper.multiple_models', '0',
            '--Mapper.extract_colors', '0',
        ]

        map_output = (subprocess.check_output(
            mapper_args, universal_newlines=True))
        logfile.write(map_output)
        print('Sparse map created')

    if run_until >= 4:
        p = os.path.join(basedir, 'dense')
        if not os.path.exists(p):
            os.makedirs(p)

        undistorter_args = [
            'colmap', 'image_undistorter',
            '--input_path', os.path.join(basedir, 'sparse', '0'),
            '--image_path', os.path.join(basedir, 'images'),
            '--output_path', os.path.join(basedir, 'dense'),
            '--output_type', 'COLMAP',
            '--max_image_size', '2000',
        ]

        undistorter_output = (subprocess.check_output(
            undistorter_args, universal_newlines=True))
        logfile.write(undistorter_output)
        print('Undistorted images created')

    if run_until >= 5:
        stereo_matcher_args = [
            'colmap', 'patch_match_stereo',
            '--workspace_path', os.path.join(basedir, 'dense'),
            '--workspace_format', 'COLMAP',
            '--PatchMatchStereo.geom_consistency', 'true',
        ]

        stereo_matcher_output = (subprocess.check_output(
            stereo_matcher_args, universal_newlines=True))
        logfile.write(stereo_matcher_output)
        print('stereo matched')

    if run_until >= 6:
        fusion_args = [
            'colmap', 'stereo_fusion',
            '--workspace_path', os.path.join(basedir, 'dense'),
            '--workspace_format', 'COLMAP',
            '--output_path', os.path.join(basedir, 'dense', 'fused.ply'),
            '--input_type', 'geometric',
        ]

        fusion_output = (subprocess.check_output(
            fusion_args, universal_newlines=True))
        logfile.write(fusion_output)
        print('fused')

    if run_until >= 7:
        poisson_args = [
            'colmap', 'poisson_mesher',
            '--input_path', os.path.join(basedir, 'dense', 'fused.ply'),
            '--output_path', os.path.join(basedir,
                                          'dense', 'meshed-poisson.ply'),
        ]

        poisson_output = (subprocess.check_output(
            poisson_args, universal_newlines=True))
        logfile.write(poisson_output)
        print('poisson mesh created')

    if run_until >= 8:
        delaunay_args = [
            'colmap', 'delaunay_mesher',
            '--input_path', os.path.join(basedir, 'dense'),
            '--output_path', os.path.join(basedir,
                                          'dense', 'meshed-delaunay.ply'),
        ]

        delaunay_output = (subprocess.check_output(
            delaunay_args, universal_newlines=True))
        logfile.write(delaunay_output)
        print('delaunay mesh created')

    logfile.close()
    print('Finished running COLMAP, see {} for logs'.format(logfile_name))


if __name__ == '__main__':
    recon(args.basedir, args.match_type, args.run_until)
