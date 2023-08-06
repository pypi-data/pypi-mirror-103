import numpy as np
import matplotlib.pyplot as plt

class Link(object):
    """A base class which all Links of an Image Chain must inherit from. This
    class provides basic functionality for fourier operations such as fft, ifft,
    magnitude or phase, as well as basic plotting, and analysis helpers which
    help in determining metrics (i.e. cutoff frequency) from the modulation
    transfer function.

    Attributes:
        filter(np.ndarray): effective filter (stack) to be applied to input
        mtf(np.ndarray): normalized frequency response of Link element
                            (a.k.a normalized filter)
        backend(str): denotes the backend to be used for computation. Currently,
                            supports numpy, and will support pytorch, cupy, or
                            numba backends for leveraging CUDA and CUDNN.

    Methods:

    Properties:
        in(np.ndarray): triggers reevaluation of Link data upon set, returns
                            last specified input upon get
        out(np.ndarray): returns result of all filtering and transformations
                            performed in Link
        state(bildkedde.State): Returns all state related information in a
                                    standard interface which can be returned as
                                    a JSON structure

    """
    def __init__(self, in_data, filter_data, backend="numpy", cache=True):
        self._in = in_data
        self._filter = filter_data

        # Check shapes
        # if in_data.shape != filter_data.shape:
        #     raise ValueError("input data and filter must be same 2D shape")

        # Intermediate cacheing objects (init as None UNLESS cacheing)
        self._in_fft = None # only cached when a non-frequency-space input is supplied
        self._filter_fft = None # only cached when a non-frequency-space filter is supplied
        self._in_filtered = None # always cached if cacheing is turned on

        self._out = np.zeros(in_data.shape)

        self.backend = backend # which compute backend to use
        self.cache = cache # whether or not to record intermediate data in dedicated cache

        self._cache = None # maybe use a formal object cache for this?

        self._changed = False # useful for cacheing

    def fft(self, obj):
        if self.backend == "numpy":
            if self.cache:
                self._in_fft = np.fft.fftshift(np.fft.fft2(obj))

            return np.fft.fftshift(np.fft.fft2(obj))

    def filt(self, obj_freq, mtf):
        if self.backend == "numpy":
            if self.cache:
                self._in_filtered = obj_freq * mtf

            return obj_freq * mtf

    def ifft(self, filtered):
        if self.backend == "numpy":
            if self.cache:
                self._in_filtered = np.fft.ifft2(np.fft.fftshift(filtered))

            return np.fft.ifft2(np.fft.fftshift(filtered))

    def update(self):
        """
        Run the filtering pipeline from start to finish
        """

        self._out = self.ifft((self.filt(self.fft(self._in), self._filter)))

    def mag(self, arr):
        return np.abs(arr)

    def show(self):
        fig, axes = plt.subplots(nrows=1, ncols=2)
        axes[0].imshow(self.mag(self._in), cmap="inferno")
        axes[1].imshow(self.mag(self._out), cmap="inferno")
        plt.show()

    @property
    def in(self):
        return self._in

    @property
    def out(self):
        return self._out
