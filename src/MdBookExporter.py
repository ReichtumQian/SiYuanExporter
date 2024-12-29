
import os

class MdBookExporter:

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





