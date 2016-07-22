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

        def home(self):
            btn = QtGui.QPushButton("Plot", self)

            btn.clicked.connect(self.plot_analysis)
            btn.resize(100, 100)
            btn.move(100, 100)

        def close_application(self):
            print("application closed succesfully")
            sys.exit()

        def set_path(self):
            popup = QtGui.QFileDialog()
            self.file_path = str(popup.getExistingDirectory())
            print(self.file_path)

        def set_type_mean(self):
            self.analysis_type = "mean"
            print("mean")

        def set_type_min(self):
            self.analysis_type = "min"
            print("min")

        def set_type_stddev(self):
            self.analysis_type = "sigma"
            print("sigma")

        def set_type_max(self):
            self.analysis_type = "max"
            print("max")

        def set_type_total(self):
            self.analysis_type = "total intensity"
            print("total intensity")

        def plot_analysis(self):
            try:
                rpp = reducedRepPlot(self.file_path, 200, 600, 200, 600, self.analysis_type)
                rpp.plot()
            except NotADirectoryError:
                print("exception excepted")
                err_msg_file = QtGui.QMessageBox()
                err_msg_file.setIcon(QtGui.QMessageBox.Critical)
                err_msg_file.setWindowTitle("Error")
                err_msg_file.setText("You did not specify a file path.")
                err_msg_file.setInformativeText("click open to set the file path")
                err_msg_file.setStandardButtons(QtGui.QMessageBox.Open)
                err_msg_file.buttonClicked.connect(self.set_path)
                err_msg_file.exec_()
            except AssertionError:
                err_msg_analysis = QtGui.QMessageBox()
                err_msg_analysis.setIcon(QtGui.QMessageBox.Critical)
                err_msg_analysis.setWindowTitle("Error")
                err_msg_analysis.setText("You did not specify an analysis type")
                err_msg_analysis.setInformativeText("please go to the menu and select an analysis type before proceeding")
                err_msg_analysis.setStandardButtons(QtGui.QMessageBox.Close)
                #err_msg_analysis.buttonClicked.connect(self.set_path)
                err_msg_analysis.exec_()

    def get_image_arrays(self):
        return
