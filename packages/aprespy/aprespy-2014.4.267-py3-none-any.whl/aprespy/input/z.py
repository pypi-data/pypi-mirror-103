import sys
from collections import namedtuple
from typing import List, Tuple

import numpy as np


class Data:

    def __init__(self):
        self.theta = 0
        self.rotations = [i for i in range(0, 91, 5)]
        self.periods = []
        self.data = []

    def append_then_sort(self, value):
        self.rotations.append(value)
        self.rotations = list(set(self.rotations))
        self.rotations = sorted(self.rotations)


def read(path: str) -> list:
    """Read in z file information.

    Read in the z file information and output a list of rotated rho, phi,
    and error parameters.

    Args:
        path: Z file path.

    Returns:
        data: List of Rotation class information.

    """
    data = Data()

    # Read in z file
    z_params = z_in(path)

    # Get the electrode orientations
    (xy, yx, hz, xy_pairs, dipole_setup) = ecomp(
        z_params['nch'], z_params['chid'])

    # Get the site declination
    data.theta = z_params['stdec'].dec
    data.periods = z_params['periods'][0]

    # Add in the measured angle
    data.append_then_sort(data.theta)

    # Assemble arrays
    (z2x2, sigs, sige) = z_to_imp(z_params['z'], z_params['sig_s'],
                                  z_params['sig_e'], z_params['nche'],
                                  xy_pairs, z_params['orient'])

    for r in data.rotations:
        tz, tz_se = z_to_tz(z_params['z'], z_params['sig_s'], z_params['sig_e'], len(
            z_params['periods'][0]), r - data.theta)
        # Apply rotations oriented to True North
        if z_params['dec_format'] is True:
            (z2x2r, sigsr, siger) = rot_z(z2x2, sigs, sige, r - data.theta)
        else:
            (z2x2r, sigsr, siger) = rot_z(z2x2, sigs, sige, r)
        # Convert to apparent resistivity and phase
        data.data.append(imp_ap(z2x2r, sigsr, siger,
                         z_params['periods'], tz, tz_se))

    return data


def z_in(path: str):
    """Read information in Z file and parse said information into a dict.

    Args:
        flepth: Z file path.

    Returns:
        z_params: Dictionary of z file information.

    """
    z_params = dict()

    # Read lines from file
    with open(path) as f:
        lines = f.readlines()

    # Parse *.z* file information
    station = lines[3]
    cordec = lines[4]
    nchans = lines[5]
    nch = int(nchans.split()[3])
    metdat = lines[7: 7 + nch]
    tfdata = lines[8 + nch:]

    # declare variables
    nche = nch - 2
    nbt = int(nchans.split()[7])
    z = np.zeros((2, nche * nbt), dtype=np.complex)
    sig_s = np.zeros((2, 2 * nbt), dtype=np.complex)
    sig_e = np.zeros((nche, nche * nbt), dtype=np.complex)
    periods = np.zeros((1, nbt), dtype=np.float64)
    ndf = np.zeros((nbt, 1), dtype=np.int64)
    Coordec = namedtuple('Coordec', 'lat long dec')
    orient = np.zeros((2, nch), dtype=np.float64)
    chid = []
    csta = []
    station = ''

    # get the station id
    station = station.split(":").pop()
    # Parse orientation, tilt, channel id, and channel station name
    for i, chan in enumerate(metdat):
        fields = chan.split()
        fields.pop(0)
        # Handle negative orientation
        for j in range(2):
            o = float(fields.pop(0))
            if o < 0:
                orient[j][i] = 180 + o
            else:
                orient[j][i] = o
        csta.append(fields.pop(0))
        chid.append(fields.pop(0))
    # get coordinates and declination
    fields = cordec.split()
    if fields[4] == '0.00':
        dec = orient[0][0]
        dec_format = False
    else:
        dec = float(fields[4])
        dec_format = True
    stdec = Coordec(lat=float(fields[1]),
                    long=float(fields[2]),
                    dec=dec)

    tfdata = lines[8 + nch:]
    # Cycle through periods and extract data
    for i in range(nbt):
        # read period
        periods[0, i] = float(tfdata.pop(0).split()[2])

        # read number of data points
        ndf[i] = int(tfdata.pop(0).split()[4])

        # pop line
        tfdata.pop(0)

        # Cycle nche transfer functions
        for n in range(nche):
            tf = to_complex(tfdata.pop(0).split(), 2)
            z[0][i * nche + n] = tf[0]
            z[1][i * nche + n] = tf[1]

        # Pop line
        tfdata.pop(0)

        # Loop through Inverse Coherent Signal Power Matrix
        ncht = 2
        icspm = np.zeros((ncht, ncht), dtype=np.complex)
        for n in range(ncht):
            icspm[n] = to_complex(tfdata.pop(0).split(), ncht)
        icspm = fill_matrix(icspm)

        for n in range(ncht):
            sig_s[n][i * ncht:i * ncht + ncht] = icspm[n]

        # Pop line
        tfdata.pop(0)

        # Read residual covariance
        rc = np.zeros((nche, nche), dtype=np.complex)
        for n in range(nche):
            rc[n] = to_complex(tfdata.pop(0).split(), nche)

        rc = fill_matrix(rc)
        for n in range(len(rc)):
            sig_e[n][i * nche:i * nche + nche] = rc[n]

    # Assign to dictionary
    z_params['z'] = z
    z_params['sig_s'] = sig_s
    z_params['sig_e'] = sig_e
    z_params['periods'] = periods
    z_params['ndf'] = ndf
    z_params['stdec'] = stdec
    z_params['dec_format'] = dec_format
    z_params['orient'] = orient
    z_params['nch'] = nch
    z_params['nche'] = nche
    z_params['nbt'] = nbt
    z_params['chid'] = chid
    z_params['csta'] = csta
    z_params['station'] = station

    return z_params


def to_complex(lst: list, length: int) -> np.array:
    """Convert read string into complex numbers."""
    cmplx = np.zeros(length, dtype=np.complex)
    for n in range(int(len(lst) / 2)):
        if lst[2 * n + 1].startswith('-'):
            cmplx[n] = complex(f'{lst[2*n]}{lst[2*n+1]}j')
        else:
            cmplx[n] = complex(f'{lst[2*n]}+{lst[2*n+1]}j')
    return cmplx


def fill_matrix(mtrx: np.array) -> np.array:
    """Convert read information into Hermitian matrix."""
    for n in range(len(mtrx) - 1):
        mtrx[n][n + 1:] = np.transpose(np.conj(mtrx))[n][n + 1:]
    return mtrx


def ecomp(nch: int, chid: list) -> Tuple[list, list, list, list, str]:
    """Sort pairs of off diagonal Ex, Ey.

    Sort out and pair off diagonal Ex, Ey components for construction
    of conventional impedance tensors.

    Args:
        nch (int): Number of electrode channels.
        nchid (list): List of channel ids.

    Returns:
        xy (list): Index of Ex channels.
        yx (list): Index of Ey channels.
        hz (list): Index of Hz channels.
        xy_pairs (list): List of pairs xy, yx(?)
        dipole_setup (string): Type of array, "MT", "TEMAP", or "EMAP".

    """
    xy = []
    yx = []
    hz = []
    xy_pairs = []
    dipole_setup = ''

    nxy = 0
    nyx = 0

    for k in range(2, len(chid)):
        if chid[k].upper().startswith('EX'):
            xy.append(k - 2)
        elif chid[k].upper().startswith('EY'):
            yx.append(k - 2)
        elif chid[k].upper().startswith('H'):
            hz.append(k - 2)

    nxy = len(xy)
    nyx = len(yx)

    # Test three cases:
    # 1. All dipoles are in one line, throw error
    # 2. Conventional MT installation
    # 3. Multiple dipoles in one direction
    if min(nxy, nyx) == 0:
        dipole_setup = 'EMAP'
        print("Error: One or both of Ex/Ey not found in this file.")
    elif nxy == 1 and nyx == 1:
        dipole_setup = 'MT'
        xy_pairs = [xy, yx]
    else:
        dipole_setup = 'TEMAP'
        # Find "nearest" pairing of the available Ex/Ey components
        dist = abs((xy * np.ones((nyx, nxy), dtype=np.int64)) -
                   (np.transpose(yx) * np.ones((nyx, nyx), dtype=np.int64)))
        if nxy >= nyx:
            yxu = []
            mindist = np.amin(dist, axis=0)
            if nyx == 1:
                mindist = dist
            for k in range(nxy):
                for l in range(nyx):
                    if dist[l][k] == mindist[k]:
                        while(len(yxu) < k):
                            yxu.append(0)
                        yxu[k].append(yx[l])
            xy_pairs = xy + yxu
        else:
            xyu = []
            while(len(xyu) <= nyx):
                xyu.append(0)
            mindist = np.amin(dist, axis=1)
            if nxy == 1:
                mindist = dist
            for k in range(nyx):
                for l in range(nyx):
                    if dist[k][l] == mindist[k]:
                        xyu[k] = xy[l]
            xy_pairs = xyu + yx

    return (xy, yx, hz, xy_pairs, dipole_setup)


def z_to_tz(z: np.array, sig_s: np.array, sig_e: np.array, nper: int, rot: float) -> Tuple[np.array, np.array]:
    """Summary

    Args:
        z (np.array): Impedance matrix
        nper (int): Number of periods
        rot (float): Rotation angle

    Returns:
        Tuple(np.array, np.array): Description
    """
    theta = np.deg2rad(rot)
    R = np.array([[np.cos(theta), np.sin(theta)],
                 [-np.sin(theta), np.cos(theta)]])
    R3 = np.array([[1, 0, 0], [0, R[0, 0], R[0, 1]], [0, R[1, 0], R[1, 1]]])
    S = np.zeros((nper, 4), dtype=np.complex)
    N = np.zeros((nper, 9), dtype=np.complex)
    tz = np.zeros((nper, 2), dtype=np.complex)
    tz_se = np.zeros((nper, 2), dtype=np.complex)

    for i, j in enumerate(range(0, sig_s.shape[1], 2)):
        tmp = np.matmul(R, sig_s[:, j:j + 2])
        S[i, :] = np.matmul(tmp, np.transpose(R)).reshape((1, 4))
        # S[i, :] = (R * sig_s[:, j:j + 2] * np.transpose(R)).reshape((1,4))
    for i, j in enumerate(range(0, z.shape[1] - 1, 3)):
        tz[i, :] = (np.matmul(R, z[:, j])).reshape((1, 2))
        tmp = np.matmul(R3, sig_e[:, j:j + 3])
        N[i, :] = np.matmul(tmp, np.transpose(R3)).reshape((1, 9))
        # N[i, :] = (R3 * sig_e[:, j:j + 3] * np.transpose(R3)).reshape((1,9))

    for i in range(nper):
        tz_se[i, 0] = np.sqrt(S[i, 0].real * N[i, 0])
        tz_se[i, 1] = np.sqrt(S[i, 3].real * N[i, 0])

    return tz, tz_se


def z_to_imp(z: np.array, sig_s: np.array, sig_e: np.array, nche: int,
             ixy: list, orient: list) -> Tuple[np.array, np.array, np.array]:
    """Translate input to one or more impedance matrices.

    The z_to_imp function translates input from general Z file to one or more
    impedance matrices with signal and noise covariance matrices
    necessary for full error computation in any coordinate system.

    Args:
        z (array): Complex transfer function.
        sig_s (array): Complex inverse signal covariance.
        sig_e (array): Complex residual error covariance.
        nche (int): Number of electrode channels.
        ixy (list): List of pairs xy, yx(?).
        orient (list): 2 x nche list of orientations and tilts.

    Returns:
        z2x2 (array): 4 x nbt impedance matrix, output order: Zxx, Zxy, Zyx, Zyy
        sigs (array): 4 x nbt signal covariance matrix.
        sige (array): 4 x nbt noise covariance matrix.

    """
    ntemp = np.shape(z)
    Nbt = int(ntemp[1] / nche)
    ntemp = np.shape(ixy)
    Nimp = ntemp[1]
    Nset = Nbt * Nimp
    orient = np.deg2rad(orient)

    # Make the rotaion matrix
    Th = np.array([[np.cos(orient[0][0]), np.cos(orient[0][1])],
                   [np.sin(orient[0][0]), np.sin(orient[0][1])]],
                  dtype=np.float64)
    Th = np.transpose(np.linalg.inv(Th))
    Uh = np.kron(Th, Th)

    z2x2 = np.zeros((4, Nset), dtype=np.complex)
    sige = np.zeros((4, Nset), dtype=np.complex)
    sigs = np.zeros((4, Nset), dtype=np.complex)

    for k in range(Nimp):
        a = k * Nset
        b = a + Nbt

        Te = np.array([[np.cos(orient[0][ixy[0][k] + 2]),
                        np.cos(orient[0][ixy[1][k] + 2])],
                       [np.sin(orient[0][ixy[0][k] + 2]),
                        np.sin(orient[0][ixy[1][k] + 2])]], dtype=np.float64)
        Ue = np.kron(Te, Te)
        Uz = np.kron(Te, Th)

        ztemp = np.vstack((z[:, ixy[0][k]::nche], z[:, ixy[1][k]::nche]))
        z2x2[:, a:b] = np.dot(Uz, ztemp)

        etemp = np.vstack((sig_e[ixy[0][k], ixy[0][k]::nche],
                           sig_e[ixy[0][k], ixy[1][k]::nche],
                           sig_e[ixy[1][k], ixy[0][k]::nche],
                           sig_e[ixy[1][k], ixy[1][k]::nche]))
        sige[:, a:b] = np.dot(Ue, etemp)

        stemp = np.vstack((sig_s[:, 0:2 * Nbt - 1:2], sig_s[:, 1:2 * Nbt:2]))
        sigs[:, a:b] = np.dot(Uh, stemp)

    return (z2x2, sigs, sige)


def rot_z(z2x2: np.array, sigs: np.array, sige: np.array, theta: float) \
        -> Tuple[np.array, np.array, np.array]:
    """Rotate array into theta.

    The rot_z function rotates the impedances, signal, and error covariance
    matrices into new coordinate system.

    Args:
        z2x2 (array): Impedance matrix, output order: Zxx, Zxy, Zyx, Zyy
        sigs (array): Signal covariance matrix
        sige (array): Noise covariance matrix
        theta (float): Rotation angle in degrees.

    Returns:
        z2x2r (array): Rotated impedance matix, output order:
                       Zxx, Zxy, Zyx, Zyy
        sigsr (array): Rotated signal covariance matrix
        siger (array): Rotate noise covariance matrix

    """
    c = np.cos(np.deg2rad(theta))
    s = np.sin(np.deg2rad(theta))

    U = np.array([[c * c, c * s, c * s, s * s],
                  [-c * s, c * c, -s * s, c * s],
                  [-c * s, -s * s, c * c, c * s],
                  [s * s, -c * s, -c * s, c * c]])

    z2x2r = np.dot(U, z2x2)
    sigsr = np.dot(U, sigs)
    siger = np.dot(U, sige)

    return (z2x2r, sigsr, siger)


def imp_ap(z: np.array, sigs: np.array, sige: np.array, periods: np.array, tz, tz_se) \
        -> Tuple[np.array, np.array, np.array, np.array]:
    """Compute apparent resistivity, phase, and errors.

    The imp_ap function computes the apparent resistivity, phase, and errors
    of the given impedance covariance matrices.  The output is in the final
    form of xy, yx pairs of rho and phi.

    Args:
        z (array): Impedance matrix, output order: Zxx, Zxy, Zyx, Zyy.
        sigs (array): Signal covariance matrix.
        sige (array): Noise covariance matrix.
        periods (array): Periods in
    Returns:
        rho (array): Impedance response: Rxx, Rxy, Ryx, Ryy.
        phi (array): Phase response.
        rho_se (array): Rho standard error.
        phi_se (array): Phi standard error.

    """
    data = namedtuple('data', 'rho rho_se phi phi_se tz tz_se')
    rad_deg = 180 / np.pi
    tmp = np.shape(periods)
    nbt = tmp[1]
    tmp = np.shape(z)
    nt = tmp[1]
    nimp = int(nt / nbt)
    ncmp = 4
    XX = 0
    XY = 1
    YX = 2
    YY = 3

    rho = np.zeros((nbt, ncmp * nimp), dtype=np.float64)
    phi = np.zeros((nbt, ncmp * nimp), dtype=np.float64)
    rho_se = np.zeros((nbt, ncmp * nimp), dtype=np.float64)
    phi_se = np.zeros((nbt, ncmp * nimp), dtype=np.float64)

    # Apparent resistivity
    rxx = np.zeros((nbt, nimp), dtype=np.float64)
    rxy = np.zeros((nbt, nimp), dtype=np.float64)
    ryx = np.zeros((nbt, nimp), dtype=np.float64)
    ryy = np.zeros((nbt, nimp), dtype=np.float64)
    # TODO: Need to properly calculate rxx_se, and ryy_se
    rxx_se = np.zeros((nbt, nimp), dtype=np.float64)
    rxy_se = np.zeros((nbt, nimp), dtype=np.float64)
    ryx_se = np.zeros((nbt, nimp), dtype=np.float64)
    ryy_se = np.zeros((nbt, nimp), dtype=np.float64)

    # Phase
    pxx = np.zeros((nbt, nimp), dtype=np.float64)
    pxy = np.zeros((nbt, nimp), dtype=np.float64)
    pyx = np.zeros((nbt, nimp), dtype=np.float64)
    pyy = np.zeros((nbt, nimp), dtype=np.float64)
    # TODO: Need to properly calculate pxx_se, and pyy_se
    pxx_se = np.zeros((nbt, nimp), dtype=np.float64)
    pxy_se = np.zeros((nbt, nimp), dtype=np.float64)
    pyx_se = np.zeros((nbt, nimp), dtype=np.float64)
    pyy_se = np.zeros((nbt, nimp), dtype=np.float64)

    for k in range(nimp):
        k1 = k * nbt
        k2 = k1 + nbt

        rxx[:, k] = np.square(np.abs(np.reshape(z[XX, k1:k2], (nbt))))
        rxy[:, k] = np.square(np.abs(np.reshape(z[XY, k1:k2], (nbt))))
        ryx[:, k] = np.square(np.abs(np.reshape(z[YX, k1:k2], (nbt))))
        ryy[:, k] = np.square(np.abs(np.reshape(z[YY, k1:k2], (nbt))))

        pxx[:, k] = np.dot(rad_deg, (np.arctan(
            np.reshape(np.imag(z[XX, k1:k2]), (nbt)) /
            np.reshape(np.real(z[XX, k1:k2]), (nbt)))))
        pxy[:, k] = np.dot(rad_deg, (np.arctan(
            np.reshape(np.imag(z[XY, k1:k2]), (nbt)) /
            np.reshape(np.real(z[XY, k1:k2]), (nbt)))))
        pyx[:, k] = np.dot(rad_deg, (np.arctan(
            np.reshape(np.imag(z[YX, k1:k2]), (nbt)) /
            np.reshape(np.real(z[YX, k1:k2]), (nbt)))))
        pyy[:, k] = np.dot(rad_deg, (np.arctan(
            np.reshape(np.imag(z[YY, k1:k2]), (nbt)) /
            np.reshape(np.real(z[YY, k1:k2]), (nbt)))))

        rxx_se[:, k] = np.real(np.reshape(sigs[XX, k1:k2], (nbt))) * \
            np.real(np.reshape(sige[XX, k1:k2], (nbt))) / 2
        rxy_se[:, k] = np.real(np.reshape(sigs[YY, k1:k2], (nbt))) * \
            np.real(np.reshape(sige[XX, k1:k2], (nbt))) / 2
        ryx_se[:, k] = np.real(np.reshape(sigs[XX, k1:k2], (nbt))) * \
            np.real(np.reshape(sige[YY, k1:k2], (nbt))) / 2
        ryy_se[:, k] = np.real(np.reshape(sigs[YY, k1:k2], (nbt))) * \
            np.real(np.reshape(sige[YY, k1:k2], (nbt))) / 2

    pxy_se = np.dot(rad_deg, np.sqrt(rxy_se / rxy))
    pyx_se = np.dot(rad_deg, np.sqrt(ryx_se / ryx))

    for l in range(nbt):
        rxx[l, :] = rxx[l, :] * periods[0, l] / 5
        rxy[l, :] = rxy[l, :] * periods[0, l] / 5
        ryx[l, :] = ryx[l, :] * periods[0, l] / 5
        ryy[l, :] = ryy[l, :] * periods[0, l] / 5

        rxx_se[l, :] = np.sqrt(rxx_se[l, :] * rxx[l, :]
                               * periods[0, l] * 4 / 5)
        rxy_se[l, :] = np.sqrt(rxy_se[l, :] * rxy[l, :]
                               * periods[0, l] * 4 / 5)
        ryx_se[l, :] = np.sqrt(ryx_se[l, :] * ryx[l, :]
                               * periods[0, l] * 4 / 5)
        ryy_se[l, :] = np.sqrt(ryy_se[l, :] * ryy[l, :]
                               * periods[0, l] * 4 / 5)

    for i in range(nimp):
        a = i * nimp
        b = a + ncmp

        rho[:, a:b] = np.stack((rxx[:, i], rxy[:, i], ryx[:, i], ryy[:, i]),
                               axis=-1)
        phi[:, a:b] = np.stack((pxx[:, i], pxy[:, i], pyx[:, i], pyy[:, i]),
                               axis=-1)
        rho_se[:, a:b] = 2 * np.stack((rxx_se[:, i], rxy_se[:, i],
                                       ryx_se[:, i], ryy_se[:, i]), axis=-1)
        phi_se[:, a:b] = 2 * np.stack((pxx_se[:, i], pxy_se[:, i],
                                       pyx_se[:, i], pyy_se[:, i]), axis=-1)

    return data(rho=rho, rho_se=rho_se, phi=phi, phi_se=phi_se, tz=tz, tz_se=tz_se)
