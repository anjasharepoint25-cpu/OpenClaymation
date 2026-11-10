import unittest
from openclaymation.blender.clay_shader import CLAY_PALETTES
from openclaymation.assembler.audio_sync import align_scenes_to_narration

class TestOpenClaymation(unittest.TestCase):
    def test_clay_palettes(self):
        self.assertIn("terracotta", CLAY_PALETTES)
        self.assertIn("midnight_blue", CLAY_PALETTES)
        self.assertEqual(len(CLAY_PALETTES["terracotta"]), 4)

    def test_scene_alignment(self):
        scenes = align_scenes_to_narration(total_audio_duration=20.0, scene_count=4)
        self.assertEqual(len(scenes), 4)
        self.assertEqual(scenes[0]["start"], 0.0)
        self.assertEqual(scenes[-1]["end"], 20.0)
        self.assertEqual(scenes[0]["target_frames_12fps"], 60)
        self.assertEqual(scenes[0]["output_frames_24fps"], 120)

if __name__ == "__main__":
    unittest.main()
