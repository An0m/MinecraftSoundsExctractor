import json
import os
import shutil

assetsFolder = os.getenv("APPDATA").replace("\\", "/") + "/.minecraft/assets"
version = input("Enter the Minecraft version (ex: 1.19) or write \"latest\" to use the latest installed: ")

# Get the latest Minecraft version
if (version.lower() in ["latest", "auto", ""]):
    versions = list(filter(lambda v: str(v).startswith("1"), os.listdir(assetsFolder+"/indexes/")))
    versions = sorted([int(v[2:][:2].replace(".", "").replace("-", "")) for v in versions])
    version = f"1.{str(versions[-1])}"
    del versions

try:
    with open(f"{assetsFolder}/indexes/{version}.json", "r") as f:
        sounds = {
            key[17:] : value["hash"] for (key, value) in json.load(f)["objects"].items() 
            if str(key).startswith("minecraft/sounds/")}.items()

        # Exctract the files
        print("Extracting...")
        for filePath, fileName in sounds:
            src_fpath = f"{assetsFolder}/objects/{fileName[:2]}/{fileName}"
            dest_fpath = f"{version}/{filePath}"

            os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
            shutil.copyfile(src_fpath, dest_fpath)
        print("Done!")
except:
    print("Invalid Minecraft version")
