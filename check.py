import inspect
import os
from pathlib import Path

from src import SimpleDatasetDownloader

def inspect_dataset(base_path="./gastronomic_dataset",max_depth=2):
    simple_path = Path(base_path)

    if not simple_path.exists():
        print(f"Folder {simple_path.resolve()} does not exists")
        print("If you have just launched the script, the download is still running in the background.")

        return
    print(f"Folder downloaded:{simple_path.resolve()}")

    extesnsion_counts = {}
    total_files = 0

    for p in simple_path.rglob("*"):
        if p.is_file():
            ext = p.suffix.lower() if p.suffix else "Without extension"
            extesnsion_counts[ext] = extesnsion_counts.get(ext,0) +1 
            total_files +=1

    print("Number of files with extensions:")

    for ext,count in sorted(extesnsion_counts.items(),key=lambda x: x[1],reverse=True):
        print(f"  • {ext}: {count} pcs.")

    print(f"Total files : {total_files}\n" + "-"*40)

    print("\n Structure of Direoctories:")
    for root,dirs,files in os.walk(simple_path):
        rel_path = Path(root).relative_to(simple_path)
        depth = len(rel_path.parts)

        if depth > max_depth:
            continue

        indent = "" * depth 
        folder_name = rel_path.name if rel_path.parts else "root"
        print(f"{indent}📂 {folder_name}/ ({len(files)} files)")

        for f in files[:3]:
            print(f"{indent}  ├── 📄 {f}")
            if len(files) > 3:
                print(f"{indent}  └── ... и еще {len(files) - 3} файлов")

if __name__ == "__main__":
    downloader = SimpleDatasetDownloader()

    downloader.list_files()
    inspect_dataset()
