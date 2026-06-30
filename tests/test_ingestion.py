import shutil
import os
from pathlib import Path

from ingestion import load_faq_to_chroma

def test_load_faq_to_chroma(tmp_path):
    # Copy sample data to temp
    shutil.copytree("data", tmp_path / "data")
    chroma_path = tmp_path / "chroma"
    load_faq_to_chroma(data_dir=str(tmp_path / "data"), chroma_path=str(chroma_path))
    assert os.path.isdir(chroma_path)
