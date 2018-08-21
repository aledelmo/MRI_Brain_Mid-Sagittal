import argparse
import os.path
import sys
from inspect import currentframe, getframeinfo
from time import time

from logic import get_left_right
from logic.utils import MidSagittalError, load_nii, save_nii, save_txt

__author__ = 'Alessandro Delmonte'
__email__ = 'delmonte.ale92@gmail.com'


def main():
    image_fname, out_fname = setup()
    img, affine, _ = load_nii(image_fname)

    plane, eq = get_left_right(img, affine)
    if out_fname:
        if out_fname.endswith('.nii') or out_fname.endswith('.nii.gz'):
            save_nii(out_fname, plane, affine)
        else:
            save_txt(out_fname, eq)
    else:
        print('Plane equation: {}'.format(eq))


def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('Image', help='Name of the input image file', type=check_nii)
    parser.add_argument('-o', '--output', help='Name of the output fuzzy space file', type=check_out)

    args = parser.parse_args()

    return args.Image, args.output


def check_nii(value):
    if value.endswith('.nii') or value.endswith('.nii.gz') and os.path.isfile(os.path.abspath(value)):
        return os.path.abspath(value)
    else:
        try:
            raise MidSagittalError('Invalid image file extension')
        except MidSagittalError as e:
            print('Caught this error: ' + repr(e))
            frame_info = getframeinfo(currentframe())
            print('Script: ' + frame_info.filename + ', Line: ' + str(frame_info.lineno))
            print('Suggestion: The image must follow the NIfTI1 format (.nii or .nii.gz)')
            sys.exit(1)


def check_out(value):
    if value.endswith('.nii') or value.endswith('.nii.gz') or value.endswith('.txt') and os.path.isfile(
            os.path.abspath(value)):
        return os.path.abspath(value)
    else:
        try:
            raise MidSagittalError('Invalid output file extension')
        except MidSagittalError as e:
            print('Caught this error: ' + repr(e))
            frame_info = getframeinfo(currentframe())
            print('Script: ' + frame_info.filename + ', Line: ' + str(frame_info.lineno))
            print(
                'Suggestion: The output must either follow the NIfTI1 format (.nii or .nii.gz) or be a plain text \
                file (.txt).')
            sys.exit(1)


if __name__ == '__main__':
    t0 = time()
    main()
    print('Execution time: {} s'.format(round((time() - t0), 2)))

    sys.exit(0)
