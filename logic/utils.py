import numpy as np
import nibabel as nib
from scipy.ndimage import generate_binary_structure, binary_dilation


def load_nii(path):
    img = nib.load(path)
    canonical_img = nib.as_closest_canonical(img)
    return canonical_img.get_fdata(), canonical_img.affine


def save_nii(path, data, affine):
    img = nib.Nifti1Image(data.astype(np.int16), affine)
    nib.save(img, path)


def split_img_with_plane(img, eq):
    voxel = combinator(*img.shape)
    voxel = voxel[:, 0] * eq[0] + voxel[:, 1] * eq[1] + voxel[:, 2] * eq[2] - eq[3]
    voxel = np.reshape(np.array(voxel), img.shape)

    left_side = np.zeros_like(voxel)
    right_side = np.zeros_like(voxel)

    left_side[voxel < 0] = 1
    right_side[voxel >= 0] = 1

    struct = generate_binary_structure(3, 3)
    plane = np.logical_or(np.logical_and(left_side, binary_dilation(right_side, struct)),
                          np.logical_and(right_side, binary_dilation(left_side, struct)))

    return plane


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
