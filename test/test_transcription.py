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

    def test_gulliver3(self):
        gulliver3_path = TEST_DIR / "samples" / "gulliver3.mp4"
        snippet_text = [
            "communicator parts",
            "if that's the case",
            "had a shovel"
        ]
        i = 0
        for s in transcribe.process_video(gulliver3_path):
            assert snippet_text[i] in s.text
            assert s.char == "Gulliver"
            i += 1

    def test_timmy1(self):
        timmy1_path = TEST_DIR / "samples" / "timmy1.mp4"
        snippet_text = [
            "help you today",
            "Of course"
        ]
        i = 0
        for s in transcribe.process_video(timmy1_path):
            assert snippet_text[i] in s.text
            assert s.char == "Timmy"
            i += 1

    def test_curly1(self):
        curly1_path = TEST_DIR / "samples" / "curly1.mp4"
        snippet_text = [
            "Working up a",
            "place gets me",
            "wanna jog"
        ]
        i = 0
        for s in transcribe.process_video(curly1_path):
            assert snippet_text[i] in s.text
            assert s.char == "Curly"
            i += 1

    def test_tom_nook1(self):
        tom_nook1_path = TEST_DIR / "samples" / "tom_nook1.mp4"
        snippet_text = [
            "Hello, hello",
            "would you like"
        ]
        i = 0
        for s in transcribe.process_video(tom_nook1_path):
            assert snippet_text[i] in s.text
            assert s.char == "Tom Nook"
            i += 1

    def test_roald1(self):
        roald1_path = TEST_DIR / "samples" / "roald1.mp4"
        snippet_text = [
            "What's up",
            "REALLY gets the"
        ]
        i = 0
        for s in transcribe.process_video(roald1_path):
            assert snippet_text[i] in s.text
            assert s.char == "Roald"
            i += 1

if __name__ == '__main__':
    unittest.main()