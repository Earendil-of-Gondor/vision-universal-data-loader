import argparse
from glob import glob
import os
import sys
import shutil


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SCRIPTS_FOLDER = os.path.join(ROOT_DIR, "scripts")

def parse_args():
	parser = argparse.ArgumentParser(description="Convert a text colmap export to nerf format transforms.json; optionally convert video to images, and optionally run colmap in the first place.")
	parser.add_argument("--video_in", default="", help="Run ffmpeg first to convert a provided video file into a set of images. Uses the video_fps parameter also.")
	parser.add_argument("--video_fps", default=2)
	parser.add_argument("--images", default="images", help="Input path to the images.")
	parser.add_argument("--overwrite", action="store_true", help="Do not ask for confirmation for overwriting existing images and COLMAP data.")
	parser.add_argument("--time_slice", default="", help="Time (in seconds) in the format t1,t2 within which the images should be generated from the video. E.g.: \"--time_slice '10,300'\" will generate images only from 10th second to 300th second of the video.")
	args = parser.parse_args()
	return args


def do_system(arg):
	print(f"==== running: {arg}")
	err = os.system(arg)
	if err:
		print("FATAL: command failed")
		sys.exit(err)


def run_ffmpeg(args):
	ffmpeg_binary = "ffmpeg"

	# On Windows, if FFmpeg isn't found, try automatically downloading it from the internet
	if os.name == "nt" and os.system(f"where {ffmpeg_binary} >nul 2>nul") != 0:
		ffmpeg_glob = os.path.join(ROOT_DIR, "external", "ffmpeg", "*", "bin", "ffmpeg.exe")
		candidates = glob(ffmpeg_glob)
		if not candidates:
			print("FFmpeg not found. Attempting to download FFmpeg from the internet.")
			do_system(os.path.join(SCRIPTS_FOLDER, "download_ffmpeg.bat"))
			candidates = glob(ffmpeg_glob)

		if candidates:
			ffmpeg_binary = candidates[0]

	if not os.path.isabs(args.images):
		args.images = os.path.join(os.path.dirname(args.video_in), args.images)

	images = "\"" + args.images + "\""
	video =  "\"" + args.video_in + "\""
	fps = float(args.video_fps) or 1.0
	print(f"running ffmpeg with input video file={video}, output image folder={images}, fps={fps}.")
	if not args.overwrite and (input(f"warning! folder '{images}' will be deleted/replaced. continue? (Y/n)").lower().strip()+"y")[:1] != "y":
		sys.exit(1)
	try:
		# Passing Images' Path Without Double Quotes
		shutil.rmtree(args.images)
	except:
		pass
	do_system(f"mkdir {images}")

	time_slice_value = ""
	time_slice = args.time_slice
	if time_slice:
		start, end = time_slice.split(",")
		time_slice_value = f",select='between(t\,{start}\,{end})'"
	do_system(f"{ffmpeg_binary} -i {video} -qscale:v 1 -qmin 1 -vf \"fps={fps}{time_slice_value}\" {images}/%04d.jpg")

if __name__ == "__main__":
	args = parse_args()
	if args.video_in != "":
		run_ffmpeg(args)