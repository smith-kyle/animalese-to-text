from os import listdir
from os.path import isfile, join
from pathlib import Path
import unittest
from PIL import Image

from data import transcribe

TEST_DIR = Path(__file__).parent

class ImageTestMethods(unittest.TestCase):
    def test_triangles(self):
        triangles_path = TEST_DIR / "triangles"
        triangles = [triangles_path / f for f in listdir(triangles_path) if isfile(join(triangles_path, f))]

        for t in triangles:
            assert transcribe.OCR.has_yellow_arrow(Image.open(t))

    def test_no_triangles(self):
        triangles_path = TEST_DIR / "no_triangles"
        no_triangles = [triangles_path / f for f in listdir(triangles_path) if isfile(join(triangles_path, f))]

        for nt in no_triangles:
            assert not transcribe.OCR.has_yellow_arrow(Image.open(nt))
    

    def test_name_cherry(self):
        NAMES_DIR  = TEST_DIR / "names"
        assert transcribe.OCR.get_character(Image.open(NAMES_DIR / "cherry1.png")) == "Cherry"
        assert transcribe.OCR.get_character(Image.open(NAMES_DIR / "cherry2.png")) == "Cherry"
        assert transcribe.OCR.get_character(Image.open(NAMES_DIR / "cherry3.png")) == "Cherry"
        assert transcribe.OCR.get_character(Image.open(NAMES_DIR / "cherry4.png")) == "Cherry"


    def test_name_blathers(self):
        NAMES_DIR  = TEST_DIR / "names"
        assert transcribe.OCR.get_character(Image.open(NAMES_DIR / "blathers1.png")) == "Blathers"
        assert transcribe.OCR.get_character(Image.open(NAMES_DIR / "blathers2.png")) == "Blathers"
        assert transcribe.OCR.get_character(Image.open(NAMES_DIR / "blathers3.png")) == "Blathers"
        assert transcribe.OCR.get_character(Image.open(NAMES_DIR / "blathers4.png")) == "Blathers"
    
if __name__ == '__main__':
    unittest.main()