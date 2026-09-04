import unittest
from contracts.module_protocol_v1 import Envelope, ModuleStatusPayload, ProgramStatus

class ProtocolTests(unittest.TestCase):
    def test_strict_protocol(self):
        env = Envelope(request_id="req-1", module_id="bitt", payload={"x": 1})
        self.assertEqual(env.protocol_version, "1.0.0")

    def test_program_status(self):
        status = ProgramStatus(
            program_id="bittensor/sn60",
            state="LIVE_COMPETE",
            capability_demand={"security": 0.99},
            possible_actions=["train", "submit"],
            economics={},
        )
        payload = ModuleStatusPayload(
            module_id="bitt", module_name="Bittensor", programs=[status]
        )
        self.assertEqual(payload.programs[0].program_id, "bittensor/sn60")

    def test_extra_fields_fail(self):
        with self.assertRaises(Exception):
            ProgramStatus(
                program_id="x", state="LIVE",
                capability_demand={}, possible_actions=[], economics={},
                surprise="not allowed",
            )

if __name__ == "__main__":
    unittest.main()
