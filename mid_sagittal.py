#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
import argparse
from time import time
from inspect import currentframe, getframeinfo

from symmetry import get_symmetry_plane, split_img_with_plane
from symmetry.utils import MidSagittalError, load_nii, save_nii

__author__ = 'Alessandro Delmonte'
__email__ = 'delmonte.ale92@gmail.com'


def main():
    image_fname, out_fname = setup()
    img, affine = load_nii(image_fname)

    eq = get_symmetry_plane(img, affine)
    print('Plane equation: {}'.format(eq))
    if out_fname:
        save_nii(out_fname, split_img_with_plane(img, eq), affine)


def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('Image', help='Name of the input image file', type=check_nii)
    parser.add_argument('-o', '--output', help='Name of the output file', type=check_nii)

    args = parser.parse_args()

    return args.Image, args.output


def check_nii(value):
    if value.endswith('.nii') or value.endswith('.nii.gz'):
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


if __name__ == '__main__':
    t0 = time()
    main()
    print('Execution time: {} s'.format(round((time() - t0), 2)))

    sys.exit(0)
