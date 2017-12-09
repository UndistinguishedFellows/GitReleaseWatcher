import sys
import requests
import json
from PyQt5 import QtWidgets

class Window():
	def __init__(self):
		self.app = QtWidgets.QApplication(sys.argv)
		self.w = QtWidgets.QWidget()
		
		self.lb_user = QtWidgets.QLabel("User/Org")
		self.tb_user = QtWidgets.QLineEdit("undistinguishedfellows")

		self.dropDownRepos = QtWidgets.QComboBox()
		self.dropDownReleases = QtWidgets.QComboBox()


		#repo tb
		#self.lb_repo = QtWidgets.QLabel("Repo")	
		#self.tb_repo = QtWidgets.QLineEdit("")

		self.bt_refresh = QtWidgets.QPushButton("Refresh")
		self.bt_load_repos = QtWidgets.QPushButton("Load Repos")
		self.v_box = QtWidgets.QVBoxLayout()
		self.v_boxRequest = QtWidgets.QVBoxLayout()

		self.v_box.addWidget(self.lb_user)
		self.v_box.addWidget(self.tb_user)
		self.v_box.addWidget(self.bt_load_repos)

		self.v_box.addWidget(self.dropDownRepos)
		self.v_box.addWidget(self.dropDownReleases)
		#self.v_box.addWidget(self.lb_repo)
		#self.v_box.addWidget(self.tb_repo)

		self.v_box.addWidget(self.bt_refresh)
		
		self.v_box.addLayout(self.v_boxRequest)

		self.w.setLayout(self.v_box)
		
		self.bt_refresh.clicked.connect(lambda: self.refresh_click(self.tb_user.text(), self.dropDownRepos.currentText()))
		self.bt_load_repos.clicked.connect(lambda: self.loadRepos(self.tb_user.text()))
		self.dropDownRepos.currentIndexChanged.connect(self.selection_change)
		self.w.setWindowTitle("GitWatcher")

	def selection_change(self, i):
		url = "https://api.github.com/repos/" + str(self.tb_user.text()) + "/" + str(self.dropDownRepos.currentText()) + "/releases" #https://api.github.com/users/CapitanLiteral/repos
		print(url)
		r = requests.get(url)
		self.releaseList = []
		if (r.ok):
			self.jReleases = json.loads(r.text or r.content)
			i = 0
			for item in self.jReleases:
				pair = []
				pair.append(item["tag_name"])
				pair.append(item["id"])
				self.releaseList.append(pair)
			for x in self.releaseList:
			    self.dropDownReleases.addItem(x[0])
			

	def refresh_click(self, user, repo):
		id = 0
		for x in self.releaseList:
		    if x[0] == self.dropDownReleases.currentText():
		        id = x[1]
		url = "https://api.github.com/repos/" + str(user) + "/" + str(repo) + "/releases/" + str(id)
		print(url)
		r = requests.get(url)
		for i in reversed(range(self.v_boxRequest.count())): 
			self.v_boxRequest.itemAt(i).widget().setParent(None)
		if (r.ok):
			self.repoItem = json.loads(r.text or r.content)
			self.update()
		else:
			lb_name = QtWidgets.QLabel("No releases found or some error ocurred with request.")
			self.v_boxRequest.addWidget(lb_name)
			#print(repoItem)
	def loadRepos(self, user):
		url = "https://api.github.com/users/" + str(user) + "/repos" #https://api.github.com/users/CapitanLiteral/repos
		print(url)
		r = requests.get(url)
		self.repoList = []
		if (r.ok):
			self.jRepos = json.loads(r.text or r.content)
			i = 0
			for item in self.jRepos:
				self.repoList.append(item["name"])
			self.dropDownRepos.addItems(self.repoList)


			#print(repoItem)
	def update(self):
		count = 0
		if len(self.repoItem['assets']) > 0:
			for item in self.repoItem['assets']:
				lb_name = QtWidgets.QLabel(item["name"])
				lb_downloadCount = QtWidgets.QLabel(str(item["download_count"]))
				count += item["download_count"]
				self.v_boxRequest.addWidget(lb_name)
				self.v_boxRequest.addWidget(lb_downloadCount)

			lb_count = QtWidgets.QLabel(str("Download total count: " + str(count)))
			self.v_boxRequest.addWidget(lb_count)
		else:
			lb_name = QtWidgets.QLabel("No releases found or some error ocurred with request.")
			self.v_boxRequest.addWidget(lb_name)


	def window(self):		
		self.w.show()
		sys.exit(self.app.exec_())


window = Window()
window.window()
sys.exit(app.exec_())