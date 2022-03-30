#!/usr/bin/python

import sys
import urllib3
import json

update_files_url = 'https://raw.githubusercontent.com/codesyntax/volto-txantiloiak/main/update-files.json'

if len(sys.argv) > 1 and sys.argv[1] == "-frontend":
  print("Updating project templates...")
  http = urllib3.PoolManager()
  print("Getting which files to update...")
  update_files = http.request('GET', update_files_url)
  update_files_data = json.loads(update_files.data.decode('utf-8'))
  replaces = update_files_data.get('frontend').get('replaces')
  if replaces:
    print("Replacing files...")
    for replace in replaces:
      filename = replace.get('filename')
      print(f"Replacing {filename}...")
      file = http.request('GET', replace['file_url'])
      path = replace.get('path')
      with open(f"{path}{filename}", 'w') as f:
        f.write(file.data.decode('utf-8'))
      print(f"Completed {filename}")

if len(sys.argv) > 1 and sys.argv[1] == "-theme":
  print("Updating project templates...")
  http = urllib3.PoolManager()
  print("Getting which files to update...")
  update_files = http.request('GET', update_files_url)
  update_files_data = json.loads(update_files.data.decode('utf-8'))
  replaces = update_files_data.get('theme').get('replaces')
  if replaces:
    print("Replacing files...")
    for replace in replaces:
      filename = replace.get('filename')
      print(f"Replacing {filename}...")
      file = http.request('GET', replace['file_url'])
      path = replace.get('path')
      with open(f"{path}{filename}", 'w') as f:
        f.write(file.data.decode('utf-8'))
      print(f"Completed {filename}")

elif len(sys.argv) > 1 and sys.argv[1] == "-myself":
  print("Updating myself...")
  http = urllib3.PoolManager()
  print("Getting where to update from...")
  update_files = http.request('GET', update_files_url)
  update_files_data = json.loads(update_files.data.decode('utf-8'))
  updater = update_files_data.get('update_updater')
  if updater:
    print("Updating updater...")
    file = http.request('GET', updater)
    path = updater.get('path')
    filename = updater.get('filename')
    with open(f"{path}{filename}", 'w') as f:
      f.write(file.data.decode('utf-8'))
    print("Completed updater update")

else:
  print("Usage:")
  print("==================================================")
  print("")
  print("- Update project templates")
  print("---------------------------")
  print("  $ python3 update-templates.py -frontend")
  print("               OR")
  print("  $ python3 update-templates.py -theme")
  print("")
  print("- Update this updater file")
  print("---------------------------")
  print("  $ python3 update-templates.py -me")
  sys.exit(1)
