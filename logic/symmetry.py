import numpy as np
from dipy.align.imaffine import AffineMap
from .utils import combinator
from scipy.ndimage.measurements import center_of_mass
from scipy.optimize import minimize
from scipy.ndimage import generate_binary_structure, binary_dilation


def l2_images(a, b):
    return 1 - (np.linalg.norm(a - b) / (2 * np.linalg.norm(a)))


def symmetry(u, img, affine):
    u /= np.linalg.norm(u)

    transformation_matrix = np.array([[1 - 2 * (u[0] ** 2), -2 * u[0] * u[1], -2 * u[0] * u[2]],
                                      [-2 * u[0] * u[1], 1 - 2 * (u[1] ** 2), -2 * u[1] * u[2]],
                                      [-2 * u[0] * u[2], -2 * u[1] * u[2], 1 - 2 * (u[2] ** 2)]])
    affine_matrix = np.identity(4)
    affine_matrix[:3, :3] = transformation_matrix

    affine_map = AffineMap(affine_matrix,
                           img.shape, affine,
                           img.shape, affine)

    flipped = affine_map.transform(img)

    sim = l2_images(img, flipped)

    return sim


def minimizer(u, *args):
    m = symmetry(u, args[0], args[1])
    return -m


def covariance_matrix(img):
    cov = np.zeros((3, 3), dtype=object)
    cov[0, 0] = (2, 0, 0)
    cov[0, 1] = (1, 1, 0)
    cov[0, 2] = (1, 0, 1)
    cov[1, 0] = (1, 1, 0)
    cov[1, 1] = (0, 2, 0)
    cov[1, 2] = (0, 1, 1)
    cov[2, 0] = (1, 0, 1)
    cov[2, 1] = (0, 1, 1)
    cov[2, 2] = (0, 0, 2)

    mass = center_of_mass(img)
    voxels = combinator(*img.shape)
    flattened = img.flatten()

    for i in range(cov.shape[0]):
        for j in range(cov.shape[1]):
            cov[i, j] = ((((voxels[:, 0] - mass[0]) ** cov[i, j][0]) * ((voxels[:, 1] - mass[1]) ** cov[i, j][1]) * ((
                    voxels[:, 2] - mass[2]) ** cov[i, j][2])) * flattened).sum()
    cov = np.array(cov, dtype=float)
    _, v = np.linalg.eig(cov.astype('float'))

    return cov, v, mass


def get_left_right(img, affine):
    print('Initializing mid-sagittal plane...')
    _, v, mass = covariance_matrix(img)
    sym_eig = [symmetry(v[:, i], img, affine) for i in range(v.shape[1])]
    u_0 = v[:, sym_eig.index(max(sym_eig))]

    print('Optimizing mid-sagittal plane...')
    best_plane = minimize(minimizer, u_0[:3], args=(img, affine), method='SLSQP')
    eq = best_plane.x
    d = (eq * mass).sum()

    voxel = combinator(*img.shape)
    voxel = voxel[:, 0] * eq[0] + voxel[:, 1] * eq[1] + voxel[:, 2] * eq[2] - d
    voxel = np.reshape(np.array(voxel), img.shape)

    left_side = np.zeros_like(voxel)
    right_side = np.zeros_like(voxel)

    left_side[voxel < 0] = 1
    right_side[voxel >= 0] = 1

    struct = generate_binary_structure(3, 3)
    plane = np.logical_or(np.logical_and(left_side, binary_dilation(right_side, struct)),
                          np.logical_and(right_side, binary_dilation(left_side, struct)))

    eq = np.append(eq, d)

    return plane, eq
