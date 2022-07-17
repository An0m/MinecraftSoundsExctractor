import json
import os
import shutil

assetsFolder = os.getenv("APPDATA").replace("\\", "/") + "/.minecraft/assets"

# Get the Minecraft version
versions = list(filter(lambda v: str(v).startswith("1"), os.listdir(assetsFolder+"/indexes/")))
versions = sorted([int(v[2:][:2].replace(".", "").replace("-", "")) for v in versions])
version = f"1.{str(versions[-1])}.json"
del versions

with open(f"{assetsFolder}/indexes/{version}", "r") as f:
    sounds = {
        key[17:] : value["hash"] for (key, value) in json.load(f)["objects"].items() 
        if str(key).startswith("minecraft/sounds/")}.items()

    # Exctract the files
    for filePath, fileName in sounds:
        src_fpath = f"{assetsFolder}/objects/{fileName[:2]}/{fileName}"
        dest_fpath = f"sounds/{filePath}"

        os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
        shutil.copyfile(src_fpath, dest_fpath)
