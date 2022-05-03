#!/usr/bin/python

import pdb
import sys
import urllib3
import json

update_files_url = "https://raw.githubusercontent.com/codesyntax/volto-txantiloiak/main/update-files.json"


def update_data(original_data, new_data, format="json"):

    if format == "json":
        original_json = json.loads(original_data)
        new_json = json.loads(new_data)
        for key in new_json:
            original_json[key] = original_json[key] | new_json[key]

        return json.dumps(original_json, indent=2)

    return original_data


if len(sys.argv) > 1 and sys.argv[1] == "-frontend":
    print("Updating project templates...")
    http = urllib3.PoolManager()
    print("Getting which files to update...")
    update_files = http.request("GET", update_files_url)
    update_files_data = json.loads(update_files.data.decode("utf-8"))
    replaces = update_files_data.get("frontend").get("replaces")
    if replaces:
        print("Replacing files...")
        for replace in replaces:
            filename = replace.get("filename")
            print(f"Replacing {filename}...")
            file_url = replace.get("file_url")
            file = http.request("GET", file_url)
            path = replace.get("path")
            with open(f"{path}{filename}", "w") as f:
                f.write(file.data.decode("utf-8"))
            print(f"Completed {filename}")

    updates = update_files_data.get("frontend").get("updates", [])
    if updates:
        print("Updating files...")
        for update in updates:
            filename = update.get("filename")
            print(f"Updating {filename}...")
            update_format = update.get("format")
            file_url = update.get("file_url")
            file = http.request("GET", file_url)
            path = update.get("path")
            old_data = ""
            with open(f"{path}{filename}", "r") as f:
                old_data = f.read()
            with open(f"{path}{filename}", "w") as f:
                new_data = update_data(
                    old_data,
                    file.data.decode("utf-8"),
                    update.get("format"),
                )
                f.write(new_data)
            print(f"Completed {filename}")

elif len(sys.argv) > 1 and sys.argv[1] == "-theme":
    print("Updating project templates...")
    http = urllib3.PoolManager()
    print("Getting which files to update...")
    update_files = http.request("GET", update_files_url)
    update_files_data = json.loads(update_files.data.decode("utf-8"))
    replaces = update_files_data.get("theme").get("replaces")
    if replaces:
        print("Replacing files...")
        for replace in replaces:
            filename = replace.get("filename")
            print(f"Replacing {filename}...")
            file_url = replace.get("file_url")
            file = http.request("GET", file_url)
            path = replace.get("path")
            with open(f"{path}{filename}", "w") as f:
                f.write(file.data.decode("utf-8"))
            print(f"Completed {filename}")

elif len(sys.argv) > 1 and sys.argv[1] == "-myself":
    print("Updating myself...")
    http = urllib3.PoolManager()
    print("Getting where to update from...")
    update_files = http.request("GET", update_files_url)
    update_files_data = json.loads(update_files.data.decode("utf-8"))
    updater = update_files_data.get("update_updater")
    if updater:
        print("Updating updater...")
        file_url = updater.get("file_url")
        file = http.request("GET", file_url)
        path = updater.get("path")
        filename = updater.get("filename")
        with open(f"{path}{filename}", "w") as f:
            f.write(file.data.decode("utf-8"))
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
    print("  $ python3 update-templates.py -myself")
    sys.exit(1)
