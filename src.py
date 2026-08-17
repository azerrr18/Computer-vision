#first donwload the data

import os
from huggingface_hub import snapshot_download
from pathlib import Path


class SimpleDatasetDownloader():
    def __init__(self,local_dir:str ="./gastronomic_dataset" ):
        self.repo_id = "issai/Global_Gastronomic_Culinary_Dataset"
        self.local_dir = Path(local_dir)

    def get_dataset_path(self) -> str | None:
        try:
            print("Dataset is downloaded/ checked 🌐...")
            dataset_path = snapshot_download(repo_id=self.repo_id,
            repo_type="dataset",
            local_dir=str(self.local_dir))
            print(f"Dataset is now working {dataset_path}")
            return dataset_path

        except Exception as e :
            print(f"Error when downloading the dataset:{e}")
            return None

    def list_files(self,limit: int=10) ->list[str]:
        path = self.get_dataset_path()
        if path and os.path.exists(path):
            files = os.listdir(path)
            print(f"\n There are {len(files)}")
            for f in files[:limit]:
                print(f"  - {f}")
            if len(files)>limit:
                print(f" Remained {len(files)-limit} files")
            return files
        return []

if __name__=="__main__":
    downloader = SimpleDatasetDownloader()
    downloader.list_files()


