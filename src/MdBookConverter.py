from BaseConverter import *
from urllib.parse import quote


class MdBookConverter(BaseConverter):

  def setup(self, directory, HPaths):
    file_name = "SUMMARY.md"
    file_name = os.path.join(directory, file_name)
    with open(file_name, 'w', encoding='utf-8') as f:
      f.write('# Summary\n\n')
      for HPath in HPaths:
        name = os.path.basename(HPath)
        levels = len(HPath.split('/')) - 2
        tabs = '\t' * levels
        encoded_path = quote(HPath)
        f.write(f'{tabs}- [{name}](.{encoded_path}.md)\n')
