from pathlib import Path
import unittest

from data import transcribe

TEST_DIR = Path(__file__).parent

def test_video(path, texts, char):
    i = 0
    for s in transcribe.process_video(path):
        assert texts[i] in s.text
        print(s.char)
        assert s.char == char
        i += 1


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
        test_video(cherry1_path, snippet_text, "Cherry")

    def test_blathers1(self):
        blathers1_path = TEST_DIR / "samples" / "blathers1.mp4"
        snippet_text = [
            "here to help",
            "Marvelous! What would"
        ]
        test_video(blathers1_path, snippet_text, "Blathers")

    def test_gulliver1(self):
        gulliver1_path = TEST_DIR / "samples" / "gulliver1.mp4"
        snippet_text = [
            "pool noodles"
        ]
        test_video(gulliver1_path, snippet_text, "Gulliver")

    def test_gulliver2(self):
        gulliver2_path = TEST_DIR / "samples" / "gulliver2.mp4"
        snippet_text = [
            "Mrmph",
            "already tipped",
            "Who are you"
        ]
        test_video(gulliver2_path, snippet_text, "Gulliver")

    def test_gulliver3(self):
        gulliver3_path = TEST_DIR / "samples" / "gulliver3.mp4"
        snippet_text = [
            "communicator parts",
            "if that's the case",
            "had a shovel"
        ]
        test_video(gulliver3_path, snippet_text, "Gulliver")

    def test_timmy1(self):
        timmy1_path = TEST_DIR / "samples" / "timmy1.mp4"
        snippet_text = [
            "help you today",
            "Of course"
        ]
        test_video(timmy1_path, snippet_text, "Timmy")

    def test_curly1(self):
        curly1_path = TEST_DIR / "samples" / "curly1.mp4"
        snippet_text = [
            "Working up a",
            "place gets me",
            "wanna jog"
        ]
        test_video(curly1_path, snippet_text, "Curly")

    def test_tom_nook1(self):
        tom_nook1_path = TEST_DIR / "samples" / "tom_nook1.mp4"
        snippet_text = [
            "Hello, hello",
            "would you like"
        ]
        test_video(tom_nook1_path, snippet_text, "Tom Nook")

    def test_roald1(self):
        video_path = TEST_DIR / "samples" / "roald1.mp4"
        snippet_text = [
            "What's up",
            "REALLY gets the"
        ]
        test_video(video_path, snippet_text, "Roald")

    def test_barold1(self):
        video_path = TEST_DIR / "samples" / "barold1.mp4"
        snippet_text = [
            "Nice to meet",
            "play yet because"
        ]
        test_video(video_path, snippet_text, "Barold")

    def test_canberra1(self):
        video_path = TEST_DIR / "samples" / "canberra1.mp4"
        snippet_text = [
            "nuh uh",
            "for a shop"
        ]
        test_video(video_path, snippet_text, "Canberra")

    def test_tommy1(self):
        video_path = TEST_DIR / "samples" / "tommy1.mp4"
        snippet_text = [
            "to see you",
            "campfire",
            "Resident Services"
        ]
        test_video(video_path, snippet_text, "Tommy")

    def test_gulliver4(self):
        video_path = TEST_DIR / "samples" / "gulliver4.mp4"
        snippet_text = [
            "communicator parts"
        ]
        test_video(video_path, snippet_text, "Gulliver")
    

if __name__ == '__main__':
    unittest.main()