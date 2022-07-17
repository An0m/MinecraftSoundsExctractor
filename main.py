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
            os.makedirs(os.path.dirname(f"{version}/{filePath}"), exist_ok=True)
            shutil.copyfile(f"{assetsFolder}/objects/{fileName[:2]}/{fileName}", f"{version}/{filePath}")
        print("Done!")
except:
    print("Invalid Minecraft version")
