from pathlib import Path
import unittest

from data import transcribe

TEST_DIR = Path(__file__).parent

class TranscriptionTestMethods(unittest.TestCase):
    def test_cherry1(self):
        cherry1_path = TEST_DIR / "samples" / "cherry1.mp4"
        snippet_text = [
            "Does it hurt?",
            "Gotta be careful",
            "what what",
            "I'd give it to you",
            "to MAKE medicine.",
            "whip up some",
        ]
        i = 0
        for s in transcribe.process_video(cherry1_path):
            assert snippet_text[i] in s.text
            assert s.char == "Cherry"
            i += 1

    def test_blathers1(self):
        blathers1_path = TEST_DIR / "samples" / "blathers1.mp4"
        snippet_text = [
            "here to help",
            "Marvelous! What would"
        ]
        i = 0
        for s in transcribe.process_video(blathers1_path):
            assert snippet_text[i] in s.text
            assert s.char == "Blathers"
            i += 1

    def test_gulliver1(self):
        gulliver1_path = TEST_DIR / "samples" / "gulliver1.mp4"
        snippet_text = [
            "pool noodles"
        ]
        i = 0
        for s in transcribe.process_video(gulliver1_path):
            assert snippet_text[i] in s.text
            assert s.char == "Gulliver"
            i += 1

    def test_gulliver2(self):
        gulliver2_path = TEST_DIR / "samples" / "gulliver2.mp4"
        snippet_text = [
            "Mrmph",
            "already tipped",
            "Who are you"
        ]
        i = 0
        for s in transcribe.process_video(gulliver2_path):
            assert snippet_text[i] in s.text
            assert s.char == "Gulliver"
            i += 1

if __name__ == '__main__':
    unittest.main()