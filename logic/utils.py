import numpy as np
import nibabel as nib


def load_nii(path):
    img = nib.load(path)
    canonical_img = nib.as_closest_canonical(img)
    canonical_data = canonical_img.get_data()
    canonical_affine = canonical_img.affine
    canonical_vox = canonical_img.header.get_zooms()
    return canonical_data, canonical_affine, canonical_vox


def save_nii(path, data, affine):
    img = nib.Nifti1Image(data.astype(np.int16), affine)
    nib.save(img, path)


def save_txt(path, data):
    data.tofile(path, ' ', format='%f')


def combinator(*args):
    args = list(args)
    n = args.pop()
    cur = np.arange(n)
    cur = cur[:, None]

    while args:
        d = args.pop()
        cur = np.kron(np.ones((d, 1)), cur)
        front = np.arange(d).repeat(n)[:, None]
        cur = np.column_stack((front, cur))
        n *= d

    return cur


class MidSagittalError(Exception):
    def __init__(self, message, errors=None):
        super(MidSagittalError, self).__init__(message)
        self.errors = errors
