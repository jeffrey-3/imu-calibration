import numpy as np
from data_source import DataSource

class FakeDataSource(DataSource):
    def read(self) -> list:
        n = 100 # Number of data points
        rng = np.random.default_rng(0)

        # Random points on sphere
        phi = rng.uniform(0, 2*np.pi, n)
        costheta = rng.uniform(-1, 1, n)
        theta = np.arccos(costheta)

        x = np.sin(theta)*np.cos(phi)
        y = np.sin(theta)*np.sin(phi)
        z = np.cos(theta)

        data = np.vstack((x,y,z)).T

        # Apply soft iron (scale + skew)
        soft = np.array([[1.2, 0.1, 0.05],
                         [0.1, 0.9, 0.02],
                         [0.05, 0.02, 1.1]])

        # Apply hard iron (bias)
        bias = np.array([0.3, -0.2, 0.1])

        distorted = (data @ soft.T) + bias

        noise = rng.normal(0, 0.01, distorted.shape)
        distorted += noise

        return distorted
