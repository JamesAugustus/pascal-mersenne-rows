"""Regression checks for strict boundaries, enclosure ambiguity and packaging."""
import importlib.util
import json
from math import comb
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('verify_np',ROOT/'tests/verify_np.py')
v=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class NPChecks(unittest.TestCase):
    def test_pi_enclosure_ambiguity_is_an_error(self):
        with self.assertRaises(ArithmeticError):
            v.pi_times_less(1,3,(2,4,1))
        interval=v.pi_interval()
        self.assertTrue(v.pi_times_less(1,4,interval))
        self.assertFalse(v.pi_times_less(1,3,interval))

    def test_threshold_equality_must_not_pass(self):
        # w(1)=2 equals the k=1 target, so the strict threshold is m=2.
        self.assertEqual(v.threshold_candidate(1,v.pi_interval()),2)
        for k in range(1,7):
            m=v.threshold_candidate(k,v.pi_interval())
            self.assertLess(comb(2*m,m)<<k,1<<(2*m))
            self.assertGreaterEqual(comb(2*m-2,m-1)<<k,1<<(2*m-2))

    def test_quick_cli_scope_and_exit(self):
        with tempfile.TemporaryDirectory(prefix='np-check-') as tmp:
            result=Path(tmp)/'result.json'
            proc=subprocess.run([sys.executable,'-B',str(ROOT/'tests/verify_np.py'),'--quick','--json',str(result)],
                                text=True,capture_output=True,timeout=120)
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
            data=json.loads(result.read_text())
            self.assertEqual(data['status'],'PASS')
            self.assertEqual(data['scope']['p_max'],1000)
            self.assertEqual(data['scope']['threshold_k_max'],8)
            self.assertEqual(data['transitions'],[38,159,646])
            self.assertGreater(data['checks'],10000)

    def test_installed_package_includes_new_note_and_verifier(self):
        with tempfile.TemporaryDirectory(prefix='np-install-') as tmp:
            target=Path(tmp)/'package'
            proc=subprocess.run([sys.executable,'-B',str(ROOT/'setup/install.py'),str(target)],text=True,capture_output=True)
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
            for file in ('PASCAL_VE_NP_ADIM_ADIM.md','PASCAL_VE_NP_ADIM_ADIM.pdf','NP_CARRY_FREE_ROW_BOUND.md','NP_CARRY_FREE_ROW_BOUND.pdf','tr/NP_ELDESIZ_SATIR_SINIRI.md','tr/NP_ELDESIZ_SATIR_SINIRI.pdf','tests/verify_np.py',
                         'tests/test_np.py','tests/np_verification.json'):
                self.assertEqual((target/file).read_bytes(),(ROOT/file).read_bytes())
            proc=subprocess.run([sys.executable,'-B',str(target/'tests/verify_np.py'),'--quick'],text=True,capture_output=True,timeout=120)
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)

if __name__=='__main__':
    unittest.main()
