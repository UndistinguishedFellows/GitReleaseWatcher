import sys
import requests
import json
from PyQt5 import QtWidgets

class Window():
	def __init__(self):
		self.app = QtWidgets.QApplication(sys.argv)
		self.w = QtWidgets.QWidget()

		self.lb_user = QtWidgets.QLabel("User/Org")
		self.lb_repo = QtWidgets.QLabel("Repo")	
		self.tb_user = QtWidgets.QLineEdit("")
		self.tb_repo = QtWidgets.QLineEdit("")

		self.bt_refresh = QtWidgets.QPushButton("Refresh")
		self.v_box = QtWidgets.QVBoxLayout()
		self.v_boxRequest = QtWidgets.QVBoxLayout()

		self.v_box.addWidget(self.lb_user)
		self.v_box.addWidget(self.tb_user)

		self.v_box.addWidget(self.lb_repo)
		self.v_box.addWidget(self.tb_repo)

		self.v_box.addWidget(self.bt_refresh)
		self.v_box.addLayout(self.v_boxRequest)

		self.w.setLayout(self.v_box)

		self.bt_refresh.clicked.connect(lambda: self.refresh_click(self.tb_user.text(), self.tb_repo.text()))
		self.w.setWindowTitle("GitWatcher")


	def refresh_click(self, user, repo):
		url = "https://api.github.com/repos/" + str(user) + "/" + str(repo) + "/releases/latest"
		print(url)
		r = requests.get(url)
		if (r.ok):
			self.repoItem = json.loads(r.text or r.content)
			self.update()
			#print(repoItem)
	def update(self):
		for i in reversed(range(self.v_boxRequest.count())): 
			self.v_boxRequest.itemAt(i).widget().setParent(None)
		count = 0
		for item in self.repoItem['assets']:
			lb_name = QtWidgets.QLabel(item["name"])
			lb_downloadCount = QtWidgets.QLabel(str(item["download_count"]))
			count += item["download_count"]
			self.v_boxRequest.addWidget(lb_name)
			self.v_boxRequest.addWidget(lb_downloadCount)

		lb_count = QtWidgets.QLabel(str("Download total count: " + str(count)))
		self.v_boxRequest.addWidget(lb_count)
		


	def window(self):		
		self.w.show()
		sys.exit(self.app.exec_())


window = Window()
window.window()
sys.exit(app.exec_())