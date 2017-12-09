import requests
import json

url = "https://api.github.com/users/undistinguishedfellows/repos"
print(url)
r = requests.get(url)
repoList = []
if (r.ok):
	repoItem = json.loads(r.text or r.content)
	for item in repoItem:
		repoList.append(item["name"])


#for item in self.repoItem['assets']:
#			lb_name = QtWidgets.QLabel(item["name"])
#			lb_downloadCount = QtWidgets.QLabel(str(item["download_count"]))
#			count += item["download_count"]
#			self.v_boxRequest.addWidget(lb_name)
#			self.v_boxRequest.addWidget(lb_downloadCount)