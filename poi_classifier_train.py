from PyQt5 import uic
from PyQt5 import QtWidgets
from multiprocessing import Process
from PyQt5 import QtCore, QtWidgets,uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QMenu,QAction
from PyQt5.QtWidgets import QPushButton,QFileDialog,QProgressDialog,QProgressBar,QApplication,QMainWindow
from PyQt5.QtWidgets import QMessageBox,QDialog
from PyQt5.QtCore import QSize,QTimer
from PyQt5.QtGui import *  
from PyQt5.QtCore import *  
from qgis.utils import iface
from PyQt5 import QtCore,QtGui,QtWidgets
from qgis.core import *
from qgis.gui import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
import re,time,sys
import os,subprocess,datetime,csv


FORM_CLASS, _ = uic.loadUiType(os.path.join(
	os.path.dirname(__file__), 'poi_classifier_train_section.ui'))
	
class PoiClassifierTrainDialog(QtWidgets.QDialog, FORM_CLASS):
	def __init__(self,parent=None):
		super(PoiClassifierTrainDialog, self).__init__(parent)
		self.setupUi(self)	
		self.exppahchoosenfilebtn.clicked.connect(self.exp_path_file)
		self.choose_train_data_btn.clicked.connect(self.train_data_file)
		self.featureextractionbtn.clicked.connect(self.featureextractionbtnbtncliked)
		self.algorithmselectionbtn.clicked.connect(self.algorithmselectionbtncliked)
		self.modelselectionbtn.clicked.connect(self.modelselectionbtncliked)
		self.trainmodelbtn.clicked.connect(self.trainmodelbtncliked)
		self.clasifiercomboBoxfillcomboBox(self.clasifiercomboBox)
		
	def exp_path_file(self):
		QMessageBox.information(self,"INFO","Please select the experiment folder ")
		try:
			train_file_dir = QFileDialog()
			full_dir=str(train_file_dir.getExistingDirectory(self,"Select Experiment Folder",os.getcwd(),QFileDialog.ShowDirsOnly))
			self.exppahchoosenfile.setText(full_dir.replace("/","\\\\")+"\\\\")
		except FileNotFoundError:
			QMessageBox.warning(self,"CAUTION","No file specified")
			self.exppahchoosenfile.clear()		
		
	
	def train_data_file(self):
		QMessageBox.information(self,"INFO","Please select train data (csv)")
		try:
			train_data_dir = QFileDialog()
			file_path = "Libraries\Documents"
			filter = "csv(*.csv)"
			full_train_dir = str(train_data_dir.getOpenFileName(self,"Select Train Data CSV",os.getcwd(),filter))
			full_train_dir = str(str(full_train_dir).split(",",1)[:1]).replace("[","").replace("]","").replace("(","").replace(")","").replace("'","").replace("/","\\\\")          
			self.chosen_train_data.setText(str(full_train_dir))
			
		except FileNotFoundError:
			QMessageBox.warning(self,"CAUTION","No file specified")
			self.chosen_train_data.clear()		
		
		
	def featureextractionbtnbtncliked(self):
		progress = QProgressBar()
		progress.setGeometry(200, 80, 250, 20)
		progress.move(600,600)
		progress.setWindowTitle('Processing..')
		progress.setAlignment(QtCore.Qt.AlignCenter)
		progress.show()
		command = f'python .\\LGM-Classification-master\\src\\features_extraction.py -poi_fpath {self.chosen_train_data.text()}'
		try:
			print(command)
			output = subprocess.check_output(command,shell=True,universal_newlines=True)#stderr=subprocess.STDOUT,universal_newlines=True)
		except subprocess.CalledProcessError:
			QMessageBox.warning(self,"WARNING","Execution of command failed")
			QMessageBox.warning(self,"WARNING",str(subprocess.STDOUT))
		QMessageBox.information(self,'INFO',str(output))		



	def algorithmselectionbtncliked(self):
		progress = QProgressBar()
		progress.setGeometry(200, 80, 250, 20)
		progress.move(600,600)
		progress.setWindowTitle('Processing..')
		progress.setAlignment(QtCore.Qt.AlignCenter)
		progress.show()
		exp_path = self.exppahchoosenfile.text()
		command = f'python .\\LGM-Classification-master\\src\\algorithm_selection.py -experiment_path {exp_path}'
		try:
			output = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
		except subprocess.CalledProcessError:
			QMessageBox.warning(self,"WARNING","Execution of command failed")
			QMessageBox.warning(self,"WARNING",str(subprocess.STDOUT))
		out_put = str(output)
		QMessageBox.information(self,'INFO','Command executed successfully')
		
	def modelselectionbtncliked(self):
		theclassifierstr=self.clasifiercomboBox.itemText(self.clasifiercomboBox.currentIndex())
		progress = QProgressBar()
		progress.setGeometry(200, 80, 250, 20)
		progress.move(600,600)
		progress.setWindowTitle('Processing..')
		progress.setAlignment(QtCore.Qt.AlignCenter)
		progress.show()
		exp_path = self.exppahchoosenfile.text()+"\\"
		command = f'python .\\LGM-Classification-master\\src\\model_selection.py -classifier {theclassifierstr} -experiment_path {exp_path}'
		try:
			output = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
		except subprocess.CalledProcessError:
			QMessageBox.warning(self,"WARNING","Execution of command failed")
		out_put = str(output)
		QMessageBox.information(self,'INFO','Command executed successfully')

	
	def clasifiercomboBoxfillcomboBox(self,componame):
		componame.addItem ("\"Naive Bayes\"")  
		componame.addItem ("\"Gaussian Process\"")
		componame.addItem ("\"AdaBoost\"")	
		componame.addItem ("\"Nearest Neighbors\"")	
		componame.addItem ("\"Logistic Regression\"")	
		componame.addItem ("\"SVM\"")	
		componame.addItem ("\"MLP\"")	
		componame.addItem ("\"Decision Tree\"")	
		componame.addItem ("\"Random Forest\"")	
		componame.addItem ("\"Extra Trees\"")			
		
	def trainmodelbtncliked(self):
		progress = QProgressBar()
		progress.setGeometry(200, 80, 250, 20)
		progress.move(600,600)
		progress.setWindowTitle('Processing..')
		progress.setAlignment(QtCore.Qt.AlignCenter)
		progress.show()
		
		exp_path = self.exppahchoosenfile.text()
		command = f'python .\\LGM-Classification-master\\src\\model_training.py -experiment_path {exp_path}'
		print(command)
		try:
			output = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
		except subprocess.CalledProcessError:
			QMessageBox.warning(self,"WARNING","Execution of command failed")
		out_put = str(output)
		QMessageBox.information(self,'INFO','Command executed successfully')
		
		
		