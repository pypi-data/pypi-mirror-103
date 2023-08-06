import numpy as np
import cupy as cp
import matplotlib as plt
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
from scipy.spatial.distance import cdist

class Grid:
    def __init__(self, *, x0, x1, xstep=1, y0, y1, ystep=1):
        """initializes 2D grid with x0<=x<=x1 and y0<=y<=y1; Creates a 1D numpy array of grid coordinates in self.x and self.y"""
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.xstep = xstep
        self.ystep = ystep
        xvals = np.arange(x0, x1+xstep, xstep)
        yvals = np.arange(y1, y0-ystep, -ystep)
        xgrid, ygrid = np.meshgrid(xvals, yvals)
        self.x = np.ravel(xgrid)
        self.y = np.ravel(ygrid)
        self.extent = (self.x0,self.x1,self.y0,self.y1)
        self.gshape = (1+int((x1-x0)/xstep), 1+int((y1-y0)/ystep))
        self.len = self.gshape[0]*self.gshape[1]
        assert(self.x.shape==(self.len,))
        assert(self.y.shape==(self.len,))

    def as_xy_vectors(self):
        """returns [x,y] vectors for all grid points"""
        return np.column_stack((self.x,self.y))

    def spatial_utilities(self, *, voter_ideal_points, metric='sqeuclidean', scale=-1):
        """returns utility function values for each voter at each grid point"""
        return scale*cdist(voter_ideal_points,self.as_xy_vectors(),metric=metric)

    def plot(self, z, *, cmap=cm.gray_r, alpha=0.6, alpha_points=0.3, log=True, points=None, border=1, zoom=False, figsize=(10,10)):
        """plots values z defined on the grid; optionally plots additional 2D points and zooms to fit the bounding box of the points"""
        plt.figure(figsize=figsize)
        plt.rcParams["font.size"] = "24"
        if zoom:
            assert(points.shape[0]>2)
            assert(points.shape[1]==2)
            [min_x,min_y] = np.min(points,axis=0)-border
            [max_x,max_y] = np.max(points,axis=0)+border
            inZoom = (self.x>=min_x) & (self.x<=max_x) & (self.y>=min_y) & (self.y<=max_y)
            zshape = (1+int((max_y-min_y)/self.ystep), 1+int((max_x-min_x)/self.xstep))
            extent = (min_x,max_x,min_y,max_y)
            zraw = np.copy(z[inZoom]).reshape(zshape)
            x = np.copy(self.x[inZoom]).reshape(zshape)
            y = np.copy(self.y[inZoom]).reshape(zshape)
        else:
            zshape = self.gshape
            extent = self.extent
            zraw = z.reshape(zshape)
            x = self.x.reshape(zshape)
            y = self.y.reshape(zshape)
        zplot = np.log10((1e-20)+zraw) if log else zraw
        contours = plt.contour(x, y, zplot, extent=extent, cmap=cmap)
        plt.clabel(contours, inline=True, fontsize=12, fmt='%1.2f')
        plt.imshow(zplot, extent=extent, cmap=cmap, alpha=alpha)
        if points is not None:
            plt.scatter(points[:,0],points[:,1],alpha=alpha_points, color='black')
        plt.show()

class MarkovChainGPU():
    def __init__(self, *, P, computeNow=True):
        """initializes a MarkovChainGPU instance by copying in the transition matrix P and calculating chain properties"""
        self.P = cp.asarray(P) # transition matrix -- move to cudapy if necessary
        assert(self.P.shape[0]==self.P.shape[1]) # make sure transition matrix is square
        self.absorbing_points = cp.equal(cp.diagonal(self.P),1.0)
        self.has_unique_stationary_distibution = not cp.any(self.absorbing_points)
        if computeNow and self.has_unique_stationary_distibution:
            self.find_unique_stationary_distribution()

    def find_unique_stationary_distribution(self, *, tolerance=1e-10, start_power=2):
        """finds the stationary distribution for a Markov Chain by taking a sufficiently high power of the transition matrix"""
        if cp.any(self.absorbing_points):
            self.stationary_distribution = None
            return None
        unconverged = True
        check1 = 0 # upper left when P is from a grid
        check2 = int(self.P.shape[0]/2)  # center when P is from a grid
        power=start_power
        cP = self.P
        cP_LT = cp.linalg.matrix_power(cP, start_power)
        diags = {'power': [], 'sum1minus1': [], 'sum2minus1': [], 'sad': [], 'diff1': [], 'diff2': []}
        while unconverged:
            cP_LT = cp.linalg.matrix_power(cP_LT,2)
            power = power * 2
            c1 = cP_LT[check1]
            c2 = cP_LT[check2]
            sum1 = cp.sum(c1)
            sum2 = cp.sum(c2)
            sum_absolute_differences = cp.sum(cp.abs(cp.subtract(c1,c2)))
            diff1 = cp.sum(cp.abs(cp.subtract(cp.dot(c1,cP),c1)))
            diff2 = cp.sum(cp.abs(cp.subtract(cp.dot(c2,cP),c2)))
            diags['power'].append(power)
            diags['sum1minus1'].append(sum1-1.0)
            diags['sum2minus1'].append(sum2-1.0)
            diags['diff1'].append(diff1)
            diags['diff2'].append(diff2)
            diags['sad'].append(sum_absolute_differences)
            unconverged = (sum_absolute_differences>tolerance)
        self.stationary_distribution = cp.copy(c1 if diff1<diff2 else c2)
        self.power = power
        self.stationary_diagnostics = diags
        del cP_LT
        return self.stationary_distribution

class VotingModel():
    def __init__(self,*,utility_functions,number_of_voters,number_of_feasible_alternatives,majority,zi):
        """initializes a VotingModel with utility_functions for each voter, the number_of_voters, the number_of_feasible_alternatives,
        the majority size, and whether to use zi (fully random) or intelligent challenges (random over winning set+status quo)"""
        assert(utility_functions.shape==(number_of_voters,number_of_feasible_alternatives))
        self.utility_functions = utility_functions
        self.number_of_voters = number_of_voters
        self.number_of_feasible_alternatives = number_of_feasible_alternatives
        self.majority=majority
        self.zi = zi
        self.analyzed = False

    def analyze(self):
        self.MarkovChain = MarkovChainGPU(P=self._get_transition_matrix())
        self.core_points = cp.asnumpy(self.MarkovChain.absorbing_points)
        self.core_exists = np.any(self.core_points)
        if not self.core_exists:
            self.stationary_distribution = cp.asnumpy(self.MarkovChain.stationary_distribution)
        self.analyzed = True

    def plots(self, *, grid, voter_ideal_points, diagnostics=False):
        if self.core_exists:
            print("core plot")
            grid.plot(self.core_points.astype('int'), points=voter_ideal_points, zoom=True)
            return
        if diagnostics:
            df = pd.DataFrame(self.MarkovChain.stationary_diagnostics)
            df.plot.scatter('power','sad',loglog=True)
            df.plot.scatter('power','diff1',loglog=True)
            df.plot.scatter('power','diff2',loglog=True)
            df.plot.scatter('power','sum1minus1')
            df.plot.scatter('power','sum2minus1')
        print('no core, stationary distribution follows')
        z = self.stationary_distribution
        grid.plot(z, points=voter_ideal_points)
        grid.plot(z, points=voter_ideal_points, zoom=True)

    def _get_transition_matrix(self):
        utility_functions = self.utility_functions
        majority = self.majority
        zi = self.zi
        l = self.number_of_feasible_alternatives
        cV = cp.zeros(shape=(l,l), dtype=int)
        cU = cp.asarray(utility_functions)
        for a in range(l):
            total_votes_for_challenger_when_status_quo_is_a = cp.greater(cU,cU[:,a,cp.newaxis]).astype('int').sum(axis=0)
            total_votes_shape = total_votes_for_challenger_when_status_quo_is_a.shape
            assert(total_votes_shape==(l,))
            cV[a] = cp.greater_equal(total_votes_for_challenger_when_status_quo_is_a, majority).astype('int')
        cp.testing.assert_array_equal(cp.diagonal(cV), cp.zeros(shape=(l), dtype=int))
        cV_sum_of_row = cV.sum(axis=1)
        assert(cV_sum_of_row.shape==(l,))
        # diagonal will be set to reflect count of the losing challengers, and self-challenge, equally likely with winning challengers
        if zi:
            cP = cp.divide(cp.add(cV, cp.diag(cp.subtract(l,cV_sum_of_row))), l)
        else:
            cP = cp.divide(cp.add(cV, cp.eye(l)), (1+cV_sum_of_row)[:,cp.newaxis])
        cp.testing.assert_array_almost_equal(cP.sum(axis=1), cp.ones(shape=(l)), decimal=10)
        return cP
