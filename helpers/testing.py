from pathlib import Path, PurePath

path = PurePath()
print(path)
path = path.parent.joinpath("seasonCsvs")
print(path)

for child in Path(path).iterdir():
    print(f"{child.name}")