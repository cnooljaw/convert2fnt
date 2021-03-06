# -*- coding: utf-8 -*-
import sys
import os

from fnt_helper import generate

from PyQt5.QtCore import QDate, QSize, Qt
from PyQt5.QtWidgets import (QDesktopWidget, QPushButton, QWidget, QLineEdit, QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem, QFileDialog)
from PyQt5.QtGui import (QColor, QImage, QPixmap)

class ConvertFnt(QWidget):

	def __init__(self):
		super(ConvertFnt, self).__init__()
		
		self.setAcceptDrops(True)

		self.image_config = []
		self.initUI()
	
	def append_items(self, item_data_list):
		for data in item_data_list:
			pathname = data["pathname"]
			path,name = os.path.split(pathname)
			character = ""
			if "character" in data:
				character = data["character"]

			count = self.table.rowCount()
			self.table.insertRow(count)
			# thumbnail
			img = QImage()
			img.load(pathname)
			thumbnail_item = QTableWidgetItem()
			thumbnail_item.setTextAlignment(Qt.AlignCenter);
			thumbnail_item.setData(Qt.DecorationRole, QPixmap.fromImage(img));
			self.table.setItem(count, 0, thumbnail_item)
			# name
			name_item = QTableWidgetItem(name)
			name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
			self.table.setItem(count, 1, name_item)
			# character
			self.table.setItem(count, 2, QTableWidgetItem(character))

			self.image_config.append({
				"image":pathname,
				"character":character,    
			})

		self.table.resizeColumnToContents(0)		

	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls():
			e.accept()
		else:
			e.ignore() 

	def dropEvent(self, e):
		if e.mimeData().hasUrls():
			url_text_list = []
			for url in e.mimeData().urls():
				url_text_list.append((url.path(),url.fileName()))

			self.append_with_pathlist(url_text_list)

	def append_with_pathlist(self, path_list):
		item_data_list = []
		for i,(pathname,name) in enumerate(path_list):
			character = ""
			if os.path.isfile(pathname):
				underline_pos = name.rfind('_')
				if underline_pos != -1:
					try:
						character = chr(int(name[underline_pos+1:name.rfind(".")]))
					except ValueError:
						pass

				item_data_list.append({
					"pathname":pathname,
					"character":character,
				})
		self.append_items(item_data_list)

	def on_click_generate(self):
		for row in range(0, self.table.rowCount()):
			self.image_config[row]["character"] = self.table.item(row, self.table.columnCount()-1).text()

		# fname = QFileDialog.getSaveFileName(self)
		fname = ["/Users/bilt/Documents/convert2fnt/bin/test"]
		if fname[0]:
			path,name = os.path.split(fname[0])
			save_name,ext = os.path.splitext(name)
			generate(path, save_name, self.image_config)


	def initUI(self):
		button = QPushButton("Generate", self)
		button.clicked.connect(self.on_click_generate)

		self.table = QTableWidget(0, 3)
		self.table.setHorizontalHeaderLabels(["Preview","Item", "Character"])
		self.table.verticalHeader().setVisible(False)
		self.table.horizontalHeader().setStretchLastSection(True)		

		layout = QVBoxLayout()
		layout.addWidget(self.table)
		layout.addWidget(button)

		self.setLayout(layout)

		self.setWindowTitle('ConvertFnt')
		self.resize(300, 300)
		self.center()


	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = ConvertFnt()
	ex.show()
	app.exec_()