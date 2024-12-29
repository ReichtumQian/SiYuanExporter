
import requests
import json
import os



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

  def export_notebook_markdown_zip(self, notebook_id, file_name = "notebook.zip", directory = None):
    url = self._api_base_url + "/export/exportNotebookMd"
    response = requests.post(url, headers=self._headers, json={"notebook": notebook_id, "path" : "/"})
    data = self._check_request(response)
    zip_path = data["data"]["zip"]
    url = self._base_url + zip_path
    self._download_file(url, file_name, directory)

