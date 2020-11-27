"""Uncompress the distink zipped dbf files into managable databases."""
import zipfile
import sys
import os
from pathlib import Path

def uncompress_zips(root, regex="*.zip"):
    rootdir = Path(root)

    for path in rootdir.rglob(regex):

        dstdir = path.parent.joinpath(path.stem)
        os.makedirs(dstdir, exist_ok=True)

        zipref = zipfile.ZipFile(path)
        zipref.extractall(dstdir)
        zipref.close()

        os.remove(path)

def main():

    parent_dir = sys.argv[1]

    uncompress_zips(parent_dir, regex="*/SHAPE_*.zip")
    uncompress_zips(parent_dir, regex="*/AREA_IMOVEL.zip")

if __name__ == "__main__":
    main()