"""Uncompress the distink zipped dbf files into managable databases."""
import zipfile
import sys
import os

def main():
    parent_dir = sys.argv[1]

    for dirpath, _, filenames in os.walk(parent_dir):
        for fn in filenames:

            if fn == "AREA_IMOVEL.zip":
                
                dstdir = os.path.join(dirpath, "AREA_IMOVEL")
                os.makedirs(dstdir, exist_ok=True)

                fp = os.path.join(dirpath, fn)
                zip_ref = zipfile.ZipFile(fp)
                zip_ref.extractall(dstdir)
                zip_ref.close()

                # os.remove(fp)

if __name__ == "__main__":
    main()