"""Use this script to explore other features other than
those that Loïc is using. 
"""
from scipy import signal
import numpy as np
from scipy.fftpack import fft

from todloop import Routine
from utils import nextregular


class JesseFeatures(Routine):
    def __init__(self, **params):
        Routine.__init__(self)
        self.inputs = params.get('inputs')
        self.outputs = params.get('outputs')

    def execute(self, store):
        # retrieve tod from data store
        tod = store.get(self.inputs.get('tod'))
        ndets = len(tod.info.det_uid)
        N = tod.nsamps
        
        # compute the feature 1 and 2
        print("Computing feature 1 and 2...")

        window = signal.hann(N)

        nf = nextregular(N)
        ywf = np.abs(fft(tod*window*2.0/N, nf))

        av = np.mean(ywf, axis=1)

        # initalize empty array for features
        pav_low = np.zeros(ndets)
        pav_high = np.zeros(ndets)

        # non-zero mask
        m = (av != 0)
        pav_low[m] = np.mean(ywf[m, :1000]) / av[m]
        pav_hi[m] = np.mean(ywf[m, 1100:3000]) / av[m]
        
        # compute the feature 3: rms 
        print("Computing feature 3...")
        rmx = np.std(tod.data, axis=1)

        # compute the feature 5: a 60 secs feature that jesse proposed
        print("Computing feature 5...")        
        # here we need to take into account that tod may be
        # down-sampled beforehand
        ds = tod.info.downsample_level
        shift = 24280. / ds
        ff5 = np.mean(tod.data[:,:shift]-tod.data[:,-shift:], axis=1)

        # summarize the features into a dictionary 
        results = {
            'feat1': pav_low,
            'feat2': pav_hi,
            'feat3': rmx,
            'feat5': ff5,
        }

        # share the results in the data store
        print(results)
        store.set(self.outputs.get('results'), results)
