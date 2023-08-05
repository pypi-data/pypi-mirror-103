from .nn_utils import *
from . import active_subspaces as ac
import matplotlib.pyplot as plt
import os
import scipy
import matplotlib.tri as tri
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
import pickle


class ADS:
    """
    A utility class for creating Active Design Subspaces using a NeuralNet and a Dataset objects

    Attributes
    ----------
    dataset : Dataset
        a Dataset object containing the dataset employed for training the NeuralNet
    network : NeuralNet
        a NeuralNet object which must have been trained
    bounds : np.array
        an array containing the lower and upper boundaries of each input
    n_pts : int
        the number of points to be used for the construction of the ADS. If lower than
        dataset.n_samples, it defaults to dataset.n_samples
    n_dims : int
        the number of dimensions desired for the ADS 
    """
    def __init__(self, dataset, network, bounds, n_pts=2000, n_dims=-1):
        self.dataset = dataset
        self.network = network
        self.bounds = bounds
        self.n_pts = n_pts

        if n_dims < 0:
            self.n_dims = self.dataset.n_params
        else:
            self.n_dims = n_dims

        self.x = None
        self.qoi = None
        self.gradients = None

        self.x_normed = None
        self.grad_normed = None

        self.figures = os.path.join(os.getcwd(), 'figures')

        self.ss = ac.subspaces.Subspaces()
        self.W1 = None

        self.define_evaluations()
        self.evaluate_x()
        self.compute_gradients()

        self.normalise()

    def define_evaluations(self):
        added_points = self.n_pts - self.dataset.n_samples

        # adding remaining points uniformely distributed in the design space
        if added_points > 0:
            x = np.array([]).reshape(added_points, 0)
            for i in range(self.dataset.n_params):
                x = np.hstack(
                    (x, vectorize_random(np.linspace(self.bounds[i, 0], self.bounds[i, 1],
                                                     num=added_points,
                                                     dtype=float))))

            x = np.vstack((x, np.array(self.dataset.x)))

        else:
            x = np.array(self.dataset.x)

        self.x = x

    def evaluate_x(self):
        print('evaluating points')
        xpred = self.dataset.norm_x(pd.DataFrame(self.x, columns=self.dataset.x.columns))
        self.qoi = self.dataset.ret_qoi(self.network.predict(xpred))

    def compute_gradients(self):
        print('computing gradients')
        gcomp = GradientComputation(dataset=self.dataset, network=self.network, step=0.1)
        self.gradients = gcomp.central_diff(self.x)

    def normalise(self):
        # ADS requires inputs normalised in the range [-1,1]. So inputs, and gradients must be normalised
        self.x_normed = 2. * (self.x - self.bounds[:, 0]) / (self.bounds[:, 1] - self.bounds[:, 0]) - 1.0

        # Gradients were evaluated as df/dx. We need the gradients as df/dx_normed.
        # We need to multiply them by dx/dx_normed
        self.grad_normed = self.gradients * (self.bounds[:, 1] - self.bounds[:, 0]) / 2.0

    def compute(self):
        self.ss.compute(df=self.grad_normed, nboot=500)
        self.W1 = self.ss.eigenvecs[:, :self.n_dims]

    def plot(self, key=None, **kwargs):

        if not os.path.exists(self.figures):
            os.mkdir(self.figures)

        fig, ax = plt.subplots()

        if key == 'eigs':
            ids = np.arange(1, self.dataset.n_params + 1, 1)
            ax.plot(ids, self.ss.eigenvals.flatten(), marker='o', linewidth=1.5, mfc='none')
            ax.set_yscale('log')
            ax.set_xlabel('ID')
            ax.set_ylabel('Eigenvalue ID')
            ax.set_title('C matrix Eigenvalue Decay')
        elif key == 'cumsum':
            limit = kwargs.get('limit')
            cumsum = np.array([np.sum(self.ss.eigenvals[:i + 1]) * 100 / np.sum(self.ss.eigenvals) for i in
                               range(self.dataset.n_params)])
            ids = np.arange(1, self.dataset.n_params + 1, 1)
            ax.plot(ids[:limit], cumsum[:limit], marker='o', linewidth=1.5, mfc='none')
            ax.set_xlabel('ID')
            ax.set_ylabel('Energy (%)')
            ax.set_title('C matrix Cumulative Energy')

        elif key == 'zonotope':
            # forcing matrix W1 to be the first 2 eigenvectors of C
            W1 = self.ss.eigenvecs[:, :2]
            y = self.x_normed.dot(W1)

            u1_i = np.linspace(min(y[:, 0]), max(y[:, 0]), 500)
            u2_i = np.linspace(min(y[:, 1]), max(y[:, 1]), 500)

            triang = tri.Triangulation(y[:, 0], y[:, 1])
            interpolator = tri.LinearTriInterpolator(triang, self.qoi)
            U1, U2 = np.meshgrid(u1_i, u2_i)
            QOI = interpolator(U1, U2)

            plt.contourf(U1, U2, QOI)
            ax.set_xlabel('$\mathbf{U_{1}}$')
            ax.set_ylabel('$\mathbf{U_{2}}$')
            plt.colorbar()
            ax.set_title('QoI along $\mathbf{U_{1}}$ and $\mathbf{U_{2}}$')

        if key == 'eigs' or key == 'cumsum':
            ax.grid(color='black', lw=0.25)
            ax.tick_params(direction='in', which='both')
            ax.xaxis.set_major_locator(MaxNLocator(8))
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.xaxis.set_ticks_position('both')
            ax.yaxis.set_ticks_position('both')

        plt.savefig('%s/%s.png' % (self.figures, key))

    def save_data(self, name='ADS'):
        w1 = pd.DataFrame(self.ss.eigenvecs[:, :self.n_dims], columns=['e%s' % a for a in range(1, self.n_dims + 1)])
        w1.to_csv('%s_W1.csv' % name, index=False)
        np.savetxt('%s_eigs.dat' % name, self.ss.eigenvals)

    def map_input_data(self, fout='ADS_dataset'):

        y = self.forward_map(self.dataset.x)
        #x_normed = 2. * (self.dataset.x - self.bounds[:, 0]) / (self.bounds[:, 1] - self.bounds[:, 0]) - 1.0
        #y = np.array(x_normed).dot(self.W1) # must be done with the normalised inputs in [-1,1] range, since ADS is based on this!
        df = pd.DataFrame(y, columns=['y%s' % i for i in range(1, self.n_dims + 1)])
        df[self.dataset.qoi_label] = self.dataset.qoi
        if '.csv' not in fout:
            fout += '.csv'
        df.to_csv(fout)

    def forward_map(self, x):
        """performs the forward map for x.
        First it normalises x in the [-1,1] range since ADS is based on this
        Then it computes the dot product"""

        x_normed = 2. * (x - self.bounds[:, 0]) / (self.bounds[:, 1] - self.bounds[:, 0]) - 1.0

        if len(x_normed.shape) == 1:
            # x is a 1d array
            if len(x_normed) != self.dataset.n_params:
                raise ValueError('Dimensionality of x not correct')
            else:
                y = self.W1.T.dot(x_normed)
        else:
            if x_normed.shape[1] != self.dataset.n_params:
                raise ValueError('Dimensionality of x not correct')
            else:
                y = np.array(x_normed).dot(self.W1)

        return y

    def save(self, fout='ADS'):
        self.network = None
        if '.ads' not in fout:
            fout += '.ads'
        with open(fout, 'wb') as output:
            pickle.dump(self,output,pickle.HIGHEST_PROTOCOL)

    def load(fin='ADS.ads'):
        with open(fin, 'rb') as inps:
            return pickle.load(inps)
