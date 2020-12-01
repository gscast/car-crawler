for file in "$1/*"

do
    echo $file
    python3.8 src/utils/uncompress_dbf.py $file
done