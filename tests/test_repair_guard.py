"""The proposed code repairer cannot edit its own authority or tests."""
import tempfile
import unittest
from pathlib import Path
from scripts import repair_guard

class GuardTests(unittest.TestCase):
    def test_sanitizes_secret_and_bearer(self):
        value=repair_guard.sanitize_logs('Authorization: Bearer abc.def.ghi\napi_key=ultrasecret\n')
        self.assertNotIn('abc.def.ghi',value)
        self.assertNotIn('ultrasecret',value)

    def test_forbid_self_repair_and_policy(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'scripts').mkdir()
            (root/'scripts/collect.py').write_text('def function():\n    return 1\n')
            for path in ('scripts/repair_guard.py','scripts/witness_loom.py','tests/test_engine.py','.github/workflows/eternal-manuscript.yml'):
                with self.assertRaises(ValueError):
                    repair_guard.validate({'path':path,'original_snippet':'def function():\n',
                                          'replacement_snippet':'def function():\n    pass\n','reason':'Bad'},root)

    def test_small_syntax_valid_edit_only(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'scripts').mkdir()
            p=root/'scripts/collect.py';p.write_text('def thing():\n    return 1\n')
            proposal={'path':'scripts/collect.py','original_snippet':'    return 1\n','replacement_snippet':'    return 2\n','reason':'Fix bug'}
            repair_guard.validate(proposal,root)
            repair_guard.apply(proposal,root)
            self.assertIn('return 2',p.read_text())
            with self.assertRaises(ValueError):repair_guard.apply(proposal,root)
            bad={**proposal,'original_snippet':'    return 2\n','replacement_snippet':'    return ?\n'}
            with self.assertRaises(SyntaxError):repair_guard.validate(bad,root)

if __name__=='__main__': unittest.main()
