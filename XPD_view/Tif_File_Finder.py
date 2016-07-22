"""
This class is what gets the .tif files from the directory when entered and returns the numpy arrays used
in XPD_view. This class is designed to ensure that files are ordered according to time signature, and that
all dark tifs and raw tifs are ignored as they are being read in.
"""

from tifffile import imread
import os


class TifFileFinder(object):

    def __init__(self):
        self._directory_name = ''
        self.dir_fil = []
        self.file_list = []
        self.pic_list = []

    @property
    def directory_name(self):
        return self._directory_name

    @directory_name.setter
    def directory_name(self, val):
        self._directory_name = val
        self.get_file_list()

    def get_file_list(self):
        self.dir_fil = os.listdir(self._directory_name)
        no1 = '.dark.tif'
        no2 = '.raw.tif'
        self.dir_fil.sort(key=lambda x: os.path.getmtime(self._directory_name + x))
        self.file_list = [el for el in self.dir_fil if el.endswith('.tif') and not el.endswith(no1) or el.endswith(no2)]
        self.get_image_arrays()
        
    def get_image_arrays(self):
        return
