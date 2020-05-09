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

if __name__ == '__main__':
    unittest.main()