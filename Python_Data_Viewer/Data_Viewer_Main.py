import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import *
import numpy as np
import scipy.io as scio
import sys
from Data_Viewer_Py import *
from pathlib import Path
from treelib import Tree, Node


class Data_Viewer(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Data_Viewer, self).__init__(parent=parent)
        self.setupUi(self)
        self.combox_init()
        self.btn_state_init()
        self.line_edit_init()
        self.file_tree = Tree()
        self.file_tree.create_node("Root", 'root')
        self.data_base = ""
        self.to_db_path = ""
        self.ab_id = ""
        self.to_ab_path = ""
        self.env = ""
        self.to_env_path = ""
        self.condition = ""
        self.item_list = [
            "Condition",
            "Emg",
            "Fp",
            "GcLeft",
            "GcRight",
            "Gon",
            "Id",
            "Ik",
            "Imu",
            "Jp",
            "Markers",
        ]

    def combox_init(self):
        self.abcomboBox.clear()
        self.envcomboBox.clear()
        self.conditioncomboBox.clear()
        self.abcomboBox.currentTextChanged.connect(self.abcomboxChangedCallback)
        self.envcomboBox.currentTextChanged.connect(self.envcomboxChangedCallback)
        self.conditioncomboBox.currentTextChanged.connect(self.conditioncomboxChangedCallback)

    def btn_state_init(self):
        self.fileUpdatepushButton.setEnabled(False)
        self.fileClearpushButton.setEnabled(False)
        self.exportpushButton.setEnabled(False)
        self.setpushButton.setEnabled(True)
        self.setpushButton.clicked.connect(self.setButtonCallback)
        self.fileUpdatepushButton.clicked.connect(self.updateButtonPushed)
        self.fileClearpushButton.clicked.connect(self.clearButtonPushed)

    def line_edit_init(self):
        self.dbpathlineEdit.setText("E:/Open_Source_Data/Data1")

    def setButtonCallback(self):
        print("DataBase Path “{}”".format(self.dbpathlineEdit.text()))
        db_path = self.dbpathlineEdit.text()
        if check_db_dir_correct(db_path):
            self.data_base = db_path.split('/')[-1]
            self.to_db_path = db_path
            if not self.file_tree.contains(self.data_base):
                self.file_tree.create_node(self.data_base, self.data_base, parent="root", data=db_path)
                self.abcomboBox.clear()
                dirs = os.listdir(db_path)
                for ab in dirs:
                    if ab[:2] == 'AB':
                        self.abcomboBox.addItem(ab)
                self.abcomboxChangedCallback()

    def abcomboxChangedCallback(self):
        if not self.abcomboBox.currentText() == "":
            self.ab_id = self.abcomboBox.currentText()
        self.to_ab_path = self.to_db_path + "/" + self.ab_id + "/" + self.ab_id
        dirs = os.listdir(self.to_ab_path)
        date = dirs[0]
        self.to_ab_path = self.to_ab_path + "/" + date
        if not self.file_tree.contains(self.ab_id):
            self.file_tree.create_node(self.ab_id, self.ab_id, parent=self.data_base, data=self.to_ab_path)
        self.envcomboBox.clear()
        envs = os.listdir(self.to_ab_path)
        for env in envs:
            self.envcomboBox.addItem(env)
        self.envcomboxChangedCallback()

    def envcomboxChangedCallback(self):
        if not self.envcomboBox.currentText() == "":
            self.env = self.envcomboBox.currentText()
        self.to_env_path = self.to_ab_path + "/" + self.env
        dirs = os.listdir(self.to_env_path)
        if not self.file_tree.contains(self.ab_id + self.env):
            self.file_tree.create_node(self.env, self.ab_id + self.env, parent=self.ab_id, data=self.to_env_path)
            for i in range(11):
                self.file_tree.create_node(self.item_list[i], self.item_list[i] + self.ab_id + self.env,
                                           parent=self.ab_id + self.env,
                                           data=self.to_env_path + "/" + dirs[i])
        conditions_path = self.to_env_path + "/" + dirs[0]
        dirs = os.listdir(conditions_path)
        self.conditioncomboBox.clear()
        for condition in dirs:
            self.conditioncomboBox.addItem(condition)
        self.conditioncomboxChangedCallback()

    def conditioncomboxChangedCallback(self):
        self.fileUpdatepushButton.setEnabled(True)
        self.fileClearpushButton.setEnabled(True)
        self.exportpushButton.setEnabled(True)

    def updateButtonPushed(self):
        if not self.conditioncomboBox.currentText() == "":
            self.condition = self.conditioncomboBox.currentText()
        dirs = os.listdir(self.to_env_path)
        if not self.file_tree.contains(self.condition + "_" + self.item_list[0]+self.ab_id):
            for i in range(11):
                self.file_tree.create_node(self.condition, self.condition + "_" + self.item_list[i]+self.ab_id,
                                           parent=self.item_list[i] + self.ab_id + self.env,
                                           data=self.to_env_path + dirs[i] + "/" + self.condition)
        self.fIleListtextBrowser.setText(self.file_tree.__str__())

    def clearButtonPushed(self):
        self.fIleListtextBrowser.setText("")
        self.abcomboBox.clear()
        self.envcomboBox.clear()
        self.conditioncomboBox.clear()
        self.fileUpdatepushButton.setEnabled(False)
        self.fileClearpushButton.setEnabled(False)
        self.exportpushButton.setEnabled(False)
        self.file_tree = Tree()
        self.file_tree.create_node("Root", 'root')


def check_db_dir_correct(db_path):
    if Path(db_path).is_dir():
        print("Is a Dir")
        dirs = os.listdir(db_path)
        if dirs[0][:2] == 'AB':
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    w = Data_Viewer()
    w.show()
    sys.exit(app.exec())
