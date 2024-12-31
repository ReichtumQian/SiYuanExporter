import os
import re


class MdBookExporter:

  def _replace_link(self, content, ID2HPath):
    pattern = re.compile(r'\[(.*?)\]\(siyuan://blocks/([a-zA-Z0-9-]+)\)')

    def replace_match(match):
      text = match.group(1)
      block_id = match.group(2)
      path = ID2HPath.get(block_id, f'siyuan://blocks/{block_id}')
      return f'[{text}]({path}.md)'

    return pattern.sub(replace_match, content)

  def convert_link(self, directory, HPaths, ID2HPath):
    for path in HPaths:
      file_name = f'{path}.md'
      file_name = directory + file_name
      with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
      content = self._replace_link(content, ID2HPath)
      with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Link conversion completed.")

  def write_summary(self, directory, HPaths):
    file_name = "SUMMARY.md"
    file_name = os.path.join(directory, file_name)
    with open(file_name, 'w', encoding='utf-8') as f:
      f.write('# Summary\n\n')
      for HPath in HPaths:
        name = os.path.basename(HPath)
        levels = len(HPath.split('/')) - 2
        tabs = '\t' * levels
        f.write(f'{tabs}- [{name}](.{HPath}.md)\n')
