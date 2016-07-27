"""
This file will contain the code that makes the XPD view GUI
"""

from PyQt4 import QtGui, QtCore
import os
import sys
import numpy as np
from Tif_File_Finder import TifFileFinder
from plot_analysis import reducedRepPlot
from xray_vision.messenger.mpl.cross_section_2d import CrossSection2DMessenger


def data_gen(length):
    # This will generate circular looking data
    x_length = 100
    y_length = 100
    data = []
    keys = []
    for idx in range(length):
        array_style = np.zeros((x_length, y_length))
        keys.append(str(idx))
        for x in range(x_length):
            for y in range(y_length):
                height = idx + 1
                if x == int(x_length/2) and y == int(y_length/2):
                    array_style[x][y] = 0
                else:
                    array_style[x][y] = height/np.sqrt((x-int(x_length/2))**2+(y-int(y_length/2))**2)
        data.append(array_style)
    return data, keys


class Display2(QtGui.QMainWindow):

    def __init__(self):
        # This is just setting up some of the beginning variables
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('XPD View')
        self.analysis_type = None
        self.file_path = None
        # self.key_list = ['Home']
        data_list, self.key_list = data_gen(1)
        self.analysis_list = ["min", "max", "mean", "Standard Deviation", "Total Intensity"]
        self.Tif = TifFileFinder()

        # These commands initialize the 2D cross section widget to draw itself
        self.messenger = CrossSection2DMessenger(data_list=data_list,
                                                 key_list=self.key_list)
        self.ctrls = self.messenger._ctrl_widget
        self.ctrls.set_image_intensity_behavior('full range')
        self.messenger.sl_update_image(0)
        self.data_dict = self.messenger._view._data_dict

        # This makes the layout for the main window
        self.frame = QtGui.QFrame()
        self.main_layout = QtGui.QVBoxLayout()
        self.frame.setLayout(self.main_layout)
        self.setCentralWidget(self.frame)
        self.display = self.messenger._display
        self.display_box = QtGui.QHBoxLayout()
        self.display_box.addWidget(self.display)
        self.tools_box = QtGui.QHBoxLayout()
        self.main_layout.addLayout(self.display_box)
        self.main_layout.addLayout(self.tools_box)

        # These methods will set up the menu bars and the tool bars
        self.name_label = QtGui.QLabel()
        self.set_up_tool_bar()
        self.set_up_menu_bar()

    def set_up_menu_bar(self):
        # set path option
        setpath = QtGui.QAction("&Set Directory", self)
        setpath.setShortcut("Ctrl+O")
        setpath.setStatusTip("Set image directory")
        setpath.triggered.connect(self.set_path)

        # sets up menu refresh option
        refresh_path = QtGui.QAction('&Refresh', self)
        refresh_path.setShortcut('Ctrl+R')
        refresh_path.triggered.connect(self.refresh)

        plt_action = QtGui.QAction("&Plot", self)
        plt_action.setShortcut("Ctrl+P")
        plt_action.triggered.connect(self.set_graph_settings)

        # This sets up all of the menu widgets that are used in the GUI
        mainmenu = self.menuBar()
        filemenu = mainmenu.addMenu("&File")
        graph_menu = mainmenu.addMenu('&Reduced Representation')
        filemenu.addAction(setpath)
        filemenu.addAction(refresh_path)
        graph_menu.addAction(plt_action)

    def set_analysis_type(self, i):
        self.analysis_type = self.analysis_list[i]

    def plot_analysis(self, x_min, x_max, y_min, y_max):
        try:
            rpp = reducedRepPlot(self.data_dict, self.key_list, x_min, x_max, y_min, y_max, self.analysis_type)
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
            err_msg_analysis.setText("The limits are incorrect")
            err_msg_analysis.setInformativeText("x_min must be less than x_max \n y_min must be greater than y_max")
            err_msg_analysis.setStandardButtons(QtGui.QMessageBox.Close)
            # err_msg_analysis.buttonClicked.connect(self.set_path)
            err_msg_analysis.exec_()

    def set_graph_settings(self):
        menu = QtGui.QDialog(self)
        menu.setWindowTitle("Reduced Representation Settings")
        menu.setWindowModality(QtCore.Qt.ApplicationModal)
        #menu.setGeometry(300, 300, 800, 300)
        vbox = QtGui.QVBoxLayout()
        hbox_lim_labels = QtGui.QHBoxLayout()
        hbox_lim_widgets = QtGui.QHBoxLayout()

        # creating qt widgets
        analysis_selector = QtGui.QComboBox(menu)
        analysis_selector.addItems(self.analysis_list)

        print(self.messenger._fig.axes[0].get_xlim())
        print(self.messenger._fig.axes[0].get_ylim())

        a_selector_label = QtGui.QLabel()
        x_min_label = QtGui.QLabel()
        x_max_label = QtGui.QLabel()
        y_min_label = QtGui.QLabel()
        y_max_label = QtGui.QLabel()

        a_selector_label.setText("Analysis Type")
        x_min_label.setText("x min")
        x_max_label.setText("x max")
        y_min_label.setText("y min")
        y_max_label.setText("y max")

        x_min, x_max = self.messenger._fig.axes[0].get_xlim()
        x_lim_min = QtGui.QSpinBox()
        x_lim_min.setMinimum(0)
        x_lim_min.setMaximum(2048)
        x_lim_min.setValue(int(x_min))

        x_lim_max = QtGui.QSpinBox()
        x_lim_max.setMinimum(0)
        x_lim_max.setMaximum(2048)
        x_lim_max.setValue(int(x_max))

        y_min, y_max = self.messenger._fig.axes[0].get_ylim()
        y_lim_min = QtGui.QSpinBox()
        y_lim_min.setMinimum(0)
        y_lim_min.setMaximum(10000)
        y_lim_min.setValue(int(y_min))

        y_lim_max = QtGui.QSpinBox()
        y_lim_max.setMinimum(0)
        y_lim_max.setMaximum(10000)
        y_lim_max.setValue(int(y_max))

        plt_btn = QtGui.QPushButton()
        plt_btn.setText("Plot")
        plt_btn.clicked.connect(menu.close)
        plt_btn.clicked.connect(lambda: self.set_analysis_type(analysis_selector.currentIndex()))
        plt_btn.clicked.connect(lambda: self.plot_analysis(x_lim_min.value(), x_lim_max.value(),
                                                           y_lim_min.value(), y_lim_max.value()))

        #defining layout
        vbox.addStretch()
        vbox.addWidget(a_selector_label)
        vbox.addStretch()
        vbox.addWidget(analysis_selector)
        vbox.addStretch()
        #defining label horizontal layout
        hbox_lim_labels.addStretch()
        hbox_lim_labels.addWidget(x_min_label)
        hbox_lim_labels.addStretch()
        hbox_lim_labels.addWidget(x_max_label)
        hbox_lim_labels.addStretch()
        hbox_lim_labels.addWidget(y_min_label)
        hbox_lim_labels.addStretch()
        hbox_lim_labels.addWidget(y_max_label)
        hbox_lim_labels.setAlignment(QtCore.Qt.AlignLeft)

        vbox.addLayout(hbox_lim_labels)
        vbox.addStretch()

        #defining widget horizontal layout
        hbox_lim_widgets.addStretch()
        hbox_lim_widgets.addWidget(x_lim_min)
        hbox_lim_widgets.addStretch()
        hbox_lim_widgets.addWidget(x_lim_max)
        hbox_lim_widgets.addStretch()
        hbox_lim_widgets.addWidget(y_lim_min)
        hbox_lim_widgets.addStretch()
        hbox_lim_widgets.addWidget(y_lim_max)
        hbox_lim_widgets.setAlignment(QtCore.Qt.AlignLeft)

        vbox.addLayout(hbox_lim_widgets)
        vbox.addStretch()
        vbox.addWidget(plt_btn)

        menu.setLayout(vbox)
        menu.show()
        menu.exec_()

    def set_up_tool_bar(self):
        # All these commands will extract the desired widgets from x-ray_vision for our purposes
        self.tools_box.addWidget(self.ctrls._slider_img)
        self.tools_box.addWidget(self.ctrls._spin_img)
        self.tools_box.addWidget(self.ctrls._cm_cb)
        self.tools_box.addWidget(self.ctrls._cmbbox_intensity_behavior)
        min_label = QtGui.QLabel()
        min_label.setText('Int Min')
        self.tools_box.addWidget(min_label)
        self.tools_box.addWidget(self.ctrls._spin_min)
        max_label = QtGui.QLabel()
        max_label.setText('Int Max')
        self.tools_box.addWidget(max_label)
        self.tools_box.addWidget(self.ctrls._spin_max)

        # This makes the Label that is used to display the current key name
        self.name_label.setText('Current File: '+self.key_list[0])
        self.tools_box.addWidget(self.name_label)
        # This makes sure that the display is updated when the image is changed
        self.ctrls._spin_img.valueChanged.connect(self.change_display_name)

        # This makes the refresh button
        refresh = QtGui.QPushButton('Refresh', self)
        refresh.clicked.connect(self.refresh)
        self.tools_box.addWidget(refresh)

    def set_path(self):
        popup = QtGui.QFileDialog()
        self.file_path = str(popup.getExistingDirectory())
        self.Tif._directory_name = self.file_path
        self.Tif.get_file_list()
        if len(self.Tif.pic_list) == 0:
            print('No .tif files in directory')
        else:
            x = self.key_list[0]
            if x == 'Home' or x == '0':
                del self.data_dict[self.key_list[0]]
                self.key_list.remove(x)
                self.update_data(self.Tif.pic_list, self.Tif.file_list)
            else:
                self.update_data(self.Tif.pic_list, self.Tif.file_list)

    def refresh(self):
        new_file_names, new_data = self.Tif.get_new_files()
        if len(new_file_names) == 0:
            print("No new .tif files found")
        else:
            self.update_data(new_data, new_file_names)

    def update_data(self, data_list, file_list):
        # This method updates the data in the image display taking in some new data list and some other
        # list that is normally the list of File names. The other list is represented as the new key names.
        old_length = len(self.key_list)
        for file in file_list:
            self.key_list.append(file)
        for i in range(old_length, len(self.key_list)):
            self.data_dict[self.key_list[i]] = data_list[i - old_length]
        self.ctrls._slider_img.setMaximum(len(self.key_list) - 1)
        self.ctrls._spin_img.setMaximum(len(self.key_list) - 1)

    def change_display_name(self, index_val):
        # This is how the display updates the current name displayed
        self.name_label.setText("Current: " + self.key_list[index_val])


def main():
    app = QtGui.QApplication(sys.argv)
    viewer = Display2()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
