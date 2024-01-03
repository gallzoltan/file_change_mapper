import os
import yaml
import argparse
from datetime import datetime

def map_folder_contents(folder_path):
  """
    Visszaadja a mappában található fájlok listáját
    folder_path: mappa elérési útja
  """
  file_info = []
  for root, dirs, files in os.walk(folder_path):
    for file in files:
      file_path = os.path.join(root, file)
      file_size = os.path.getsize(file_path)
      file_info.append({
        'name': file,
        'path': file_path,
        'size': file_size
      })
  return file_info

def get_changed_files(previous_file_info, current_file_info):
  """
    Visszaadja a változott fájlokat
    previous_file_info: korábbi fájlok listája
    current_file_info: jelenlegi fájlok listája
  """
  previous_file_map = {file['path']: file for file in previous_file_info}
  changed_files = []
  
  for current_file in current_file_info:
    previous_file = previous_file_map.get(current_file['path'])
    if previous_file is None or previous_file['size'] != current_file['size']:
      changed_files.append(current_file)
  return changed_files

def open_previous_file_info(previous_file):
  """
    Megnyitja a korábbi fájlt
    previous_file: korábbi fájl elérési útja
  """
  with open(f"{previous_file}", 'r', encoding='utf8') as file:
    return yaml.load(file, Loader=yaml.FullLoader)

def save_file_info(file_info, file_name):
  """
    Mentés YAML fájlba
    file_info: menteni kívánt adatok
    file_name: menteni kívánt fájl neve
  """
  current_date = datetime.now().strftime('%Y-%m-%d_%H%M%S')
  file_name_with_date = f".\\logs\\{file_name}_{current_date}.yml"
  with open(file_name_with_date, 'w', encoding='utf8') as file:
    yaml.dump(file_info, file, allow_unicode=True)

def main():
  parser = argparse.ArgumentParser(description='File changes detector.')
  parser.add_argument('-p', '--previous', type=str, help='The name of the previous file.')
  parser.add_argument('-f', '--folder', type=str, help='The name of the folder to inspect.')

  args = parser.parse_args()

  previous_file = args.previous
  folder_path = args.folder

  if(folder_path is None):
    print("Missing folder path!")
    return
  if(previous_file is None):
    current_file_info = map_folder_contents(folder_path)
    save_file_info(current_file_info, "file_info")
    print("Mapping completed!")
  else:
    previous_file_info = open_previous_file_info(previous_file)
    current_file_info = map_folder_contents(folder_path)
    changed_files = get_changed_files(previous_file_info, current_file_info)
    save_file_info(current_file_info, "file_info")
    save_file_info(changed_files, "changed_files")
    print(f"Changed files: {changed_files}")

if __name__ == '__main__':
  main()