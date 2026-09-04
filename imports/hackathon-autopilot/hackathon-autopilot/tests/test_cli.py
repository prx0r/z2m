import json, tempfile, unittest
from pathlib import Path
from hack_autopilot.cli import words, script_duration, root_hygiene, score

class TestCLI(unittest.TestCase):
    def test_words(self):
        self.assertGreater(words("# Hello world\nThis is a test."), 4)

    def test_duration(self):
        self.assertAlmostEqual(script_duration("word " * 145, 145), 60, delta=1)

    def test_root_hygiene(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/"HANDOVER-old.md").write_text("x")
            self.assertTrue(root_hygiene(p))

    def test_minimal_score(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/"README.md").write_text("demo problem architecture sponsor limitations")
            (p/"RECORDING-SCRIPT.md").write_text("word " * 400)
            (p/"claims.json").write_text(json.dumps({"claims":[]}))
            (p/"hackathon.json").write_text(json.dumps({
                "video":{"min_seconds":120,"max_seconds":240},
                "sponsor":{"causal":True,"capabilities_used":["search"]},
                "rubric":[{"name":"x","weight":1.0}]
            }))
            result=score(p)
            self.assertIn("score",result)

if __name__ == "__main__":
    unittest.main()
