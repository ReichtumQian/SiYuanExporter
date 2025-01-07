from BaseConverter import *
from urllib.parse import quote


class MkdocsConverter(BaseConverter):

  def setup(self, directory, HPaths):
    file_name = "nav.yml"
    file_name = os.path.join(directory, file_name)
    with open(file_name, 'w', encoding='utf-8') as f:
      f.write('nav:\n')
      for i in range(len(HPaths)):
        HPath = HPaths[i]
        HPath_next = HPaths[i + 1] if i < len(HPaths) - 1 else None
        name = os.path.basename(HPath)
        levels = len(HPath.split('/')) - 1
        levels_next = len(HPath_next.split('/')) - 1 if HPath_next else 0
        tabs = '  ' * levels
        # deal with some special characters
        encoded_path = HPath
        # write to file
        if levels < levels_next:
          f.write(f'{tabs}- {name}: \n')
          # f.write(f'{tabs}  - ".{encoded_path}.md"\n')
        else:
          f.write(f'{tabs}- {name}: ".{encoded_path}.md"\n')
