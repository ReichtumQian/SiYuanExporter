
import requests
import json
import os
import zipfile
import shutil



class SiYuanExporter:
  
  def __init__(self, json_file = "config.json"):
    with open(json_file, "r") as f:
      data = json.load(f)
    self._base_url = data["base_url"]
    self._api_base_url = self._base_url + "/api"
    self._token = data["token"]
    self._headers = {
      "Authorization": "token " + self._token
    }

  def _check_request(self, response):
    if response.status_code == 200:
      data = response.json()
    else:
      assert False, "Request failed with status code " + str(response.status_code)
    return data

  def _download_file(self, url, file_name, directory = None):
    if directory is None:
      directory = os.getcwd()
    
    os.makedirs(directory, exist_ok=True)

    file_name = os.path.join(directory, file_name)
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
      with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
          file.write(chunk)
      print(f"File {file_name} downloaded successfully")
    else:
      print(f":Download failed with status code {response.status_code}")
    
  def _init_IDs(self):
    url = self._api_base_url + "/filetree/listDocsByPath"
    def _init_IDs_helper(path):
      # if depth != 0:
      #   sy_path = path + ".sy"
      response = requests.post(url, headers=self._headers, json={"notebook": self._notebook_id, "path" : path})
      data = self._check_request(response)
      files = data["data"]["files"]
      for file in files:
        self._IDs.append(file["id"])
        if file["subFileCount"] > 0:
          # if depth != 0:
            # path = path + "/"
          _init_IDs_helper(path + file["id"] + "/")
    _init_IDs_helper("/")
        

  def _init_ID2HPath(self):
    url = self._api_base_url + "/filetree/getHPathByID"
    for i in range(len(self._IDs)):
      response = requests.post(url, headers=self._headers, json={"id": self._IDs[i]})
      data = self._check_request(response)
      if data["data"] is None:
        assert False, "HPath not found for ID " + self._IDs[i]
      self._HPaths.append(data["data"])
      self._ID2HPath[self._IDs[i]] = data["data"]
  
  def set_notebook(self, notebook_id, notebook_name):
    self._notebook_id = notebook_id
    self._notebook_name = notebook_name
    self._IDs = []
    self._init_IDs()
    self._ID2HPath = {}
    self._HPaths = []
    self._init_ID2HPath()
    
  @property
  def notebook_id(self):
    return self._notebook_id
  
  @property
  def notebook_name(self):
    return self._notebook_name
  
  @property
  def HPaths(self):
    return self._HPaths

  def list_notebook(self):
    url = self._api_base_url + "/notebook/lsNotebooks"
    response = requests.post(url, headers=self._headers)
    data = self._check_request(response)
    notebook_ids = []
    notebook_names = []
    for notebook in data["data"]["notebooks"]:
      notebook_ids.append(notebook["id"])
      notebook_names.append(notebook["name"])
    return notebook_ids, notebook_names

  def export_notebook_markdown_zip(self, directory = None):
    file_name = self._notebook_name + ".zip"
    url = self._api_base_url + "/export/exportNotebookMd"
    response = requests.post(url, headers=self._headers, json={"notebook": self._notebook_id, "path" : "/"})
    data = self._check_request(response)
    zip_path = data["data"]["zip"]
    url = self._base_url + zip_path
    self._download_file(url, file_name, directory)

  def export_notebook_markdowns(self, directory = None):
    file_name = self._notebook_name + ".zip"
    self.export_notebook_markdown_zip(directory)
    if directory is None:
      directory = os.getcwd()
    os.makedirs(directory, exist_ok=True)
    file_name = os.path.join(directory, file_name)
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
      zip_ref.extractall(directory)
      print(f"File {file_name} extracted successfully to {directory}")
    os.remove(file_name)



