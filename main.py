import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig, inv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--fake", action="store_true", help="Use fake data source")
args = parser.parse_args()

if args.fake:
    from fake_source import FakeDataSource
    data_source = FakeDataSource()
else:
    from serial_source import SerialDataSource
    data_source = SerialDataSource("/dev/ttyACM0", 115200)

raw_data = data_source.read()

def ellipsoid_fit(data):
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]

    D = np.column_stack([
        x*x,
        y*y,
        z*z,
        2*x*y,
        2*x*z,
        2*y*z,
        2*x,
        2*y,
        2*z,
        np.ones(len(x))
    ])

    # Solve normal system
    _, _, V = np.linalg.svd(D, full_matrices=False)
    v = V[-1,:]

    # Quadratic form matrix
    A = np.array([
        [v[0], v[3], v[4], v[6]],
        [v[3], v[1], v[5], v[7]],
        [v[4], v[5], v[2], v[8]],
        [v[6], v[7], v[8], v[9]]
    ])

    # Center of ellipsoid
    A3 = A[:3,:3]
    b = -inv(A3) @ v[6:9]

    # Translate to center
    T = np.eye(4)
    T[3,:3] = b

    R = T @ A @ T.T
    M = R[:3,:3] / -R[3,3]

    return b, M

bias, M = ellipsoid_fit(raw_data)

evals, evecs = eig(M)
D = np.diag(np.sqrt(evals))
A = evecs @ D @ inv(evecs)

print("Bias (Hard Iron Correction):")
print(bias)
print("Soft Iron Correction Matrix (A):")
print(A)
print("Inverse of A:")
print(inv(A))

calibrated = (raw_data - bias) @ A.T

def plot_3d(data, title):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(data[:,0], data[:,1], data[:,2], s=2)
    ax.set_box_aspect([1,1,1])
    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()

plot_3d(raw_data, "Raw Accelerometer Data (Ellipsoid)")
plot_3d(calibrated, "Calibrated Data (Sphere)")

def plot_2d_overlay(raw, calibrated, idx1, idx2, label1, label2, title):
    plt.figure()
    plt.scatter(raw[:, idx1], raw[:, idx2], s=5, alpha=0.6, label="Raw")
    plt.scatter(calibrated[:, idx1], calibrated[:, idx2], s=5, alpha=0.6,
        label="Calibrated")
    plt.gca().set_aspect('equal', 'box')
    plt.xlabel(label1)
    plt.ylabel(label2)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

plot_2d_overlay(raw_data, calibrated, 0, 1, "X", "Y", "XY Projection")
plot_2d_overlay(raw_data, calibrated, 0, 2, "X", "Z", "XZ Projection")
plot_2d_overlay(raw_data, calibrated, 1, 2, "Y", "Z", "YZ Projection")
