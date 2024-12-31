import os
import re


class BaseConverter:

  def _replace_link(self, content, ID2HPath):
    pattern = re.compile(r'\[(.*?)\]\(siyuan://blocks/([a-zA-Z0-9-]+)\)')

    def replace_match(match):
      text = match.group(1)
      block_id = match.group(2)
      path = ID2HPath.get(block_id, f'siyuan://blocks/{block_id}')
      return f'[{text}]({path}.md)'

    return pattern.sub(replace_match, content)

  def _convert_link(self, directory, HPaths, ID2HPath):
    for path in HPaths:
      file_name = f'{path}.md'
      file_name = directory + file_name
      with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
      content = self._replace_link(content, ID2HPath)
      with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Link conversion completed.")

  def convert(self, directory, HPaths, ID2HPath):
    self._convert_link(directory, HPaths, ID2HPath)

  def setup(self, directory, HPaths):
    return NotImplementedError
