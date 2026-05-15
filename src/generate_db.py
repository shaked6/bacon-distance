import tarfile
import pandas as pd


def generate_db(file_path: str):

    # Open the tar.gz file
    with tarfile.open("your_file.tar.gz", "r:gz") as tar:
        # Option A: If you know the filename inside the archive
        member = tar.getmember("data_inside.csv")
        f = tar.extractfile(member)
        df = pd.read_csv(f)