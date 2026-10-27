"""Local checks; all generated files stay in a temporary directory."""

import hashlib
import importlib.util
import math
import ctypes
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


def run(*args):
    return subprocess.run(args, text=True, capture_output=True, check=False, timeout=60)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class LocalChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="mersenne-test-")
        cls.work = Path(cls.temp.name)
        cls.c_binary = cls.work / "mersenne_rows_gmp"
        compiler = shutil.which("cc")
        cls.c_available = compiler is not None
        if cls.c_available:
            built = run(compiler, "-std=c99", "-O2", "-Wall", "-Wextra", "-Wpedantic", "-Werror", "-o", str(cls.c_binary),
                        str(ROOT / "mersenne_rows_gmp.c"), "-lgmp")
            if built.returncode:
                cls.c_available = False
                print("C/GMP unavailable; C checks skipped:\n" + built.stderr, file=sys.stderr)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def programs(self):
        programs = [(sys.executable, str(ROOT / "mersenne_rows.py"))]
        if self.c_available:
            programs.append((str(self.c_binary),))
        return programs

    def test_small_rows_against_independent_oracle(self):
        for p in range(2, 13):
            n, base = p + 2, (1 << p) - 1
            row = [math.comb(n, k) for k in range(n + 1)]
            value = 0
            for digit in row:
                value = value * base + digit
            self.assertEqual(value, 1 << (p * n))
            clean = all(digit < base for digit in row)
            for program in self.programs():
                for mode in ((), ("full",)):
                    with self.subTest(p=p, program=program, mode=mode):
                        result = run(*program, str(p), *mode)
                        self.assertEqual(result.returncode, 0 if clean else 1, result.stderr)
                        lines = result.stdout.splitlines()
                        emitted = list(map(int, lines[0].split()))
                        self.assertEqual(emitted, row)
                        self.assertEqual(emitted, emitted[::-1])
                        self.assertEqual(sum(emitted), 1 << n)
                        if p % 2:
                            x = (p + 1) // 2
                            catalan = math.comb(2 * x, x) // (x + 1)
                            self.assertEqual(emitted[n // 2], n * catalan)
                        self.assertIn("moduli=3/3", lines[-1])
                        if p <= 6:
                            self.assertFalse(clean)
                            self.assertEqual(result.returncode, 1)
                            self.assertIn("clean=NO", lines[-1])
                        self.assertIn(f"clean={'yes' if clean else 'NO'}", lines[-1])
                        self.assertIn("value(mod)=ok", lines[-1])
                        if mode:
                            self.assertIn("value(full)=ok", lines[-1])
                        else:
                            self.assertNotIn("value(full)", lines[-1])

    def test_coprime_modulus_selection(self):
        spec = importlib.util.spec_from_file_location("mersenne_select", ROOT / "mersenne_rows.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Composite candidates test gcd>1, not just base==0 modulo q.
        self.assertEqual(module.select_moduli(2, [15, 7]), [7])
        self.assertEqual(module.select_moduli(3, [15, 7]), [15])
        for p in (61, 89, 127, 122, 178, 254, 61 * 89):
            base = (1 << p) - 1
            expected = [q for q in module.MODULI if math.gcd(base, q) == 1]
            self.assertEqual(module.select_moduli(p, module.MODULI), expected)
        # Small CLI cases verify the reported count, with and without full.
        for p in (61, 89, 127, 122, 178, 254):
            for program in self.programs():
                for mode in ((), ("full",)):
                    with self.subTest(p=p, program=program, mode=mode):
                        result = run(*program, str(p), *mode)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertIn("moduli=2/3", result.stdout)
                        self.assertIn("value(mod)=ok", result.stdout)
                        if mode:
                            self.assertIn("value(full)=ok", result.stdout)
        # Every fixed modulus divides this base. Selection rejects it before
        # allocating the base or iterating the roughly 689000-element row.
        all_skip_p = 61 * 89 * 127
        self.assertEqual(module.select_moduli(all_skip_p, module.MODULI), [])
        for program in self.programs():
            for mode in ((), ("full",)):
                result = run(*program, str(all_skip_p), *mode)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("clean=unchecked value(mod)=unavailable moduli=0/3", result.stdout)
                self.assertIn("checks were not run", result.stderr)
                self.assertNotIn("value(full)=ok", result.stdout)

    def test_interior_digit_corruption_is_detected(self):
        py_source = (ROOT / "mersenne_rows.py").read_text()
        old = "(x * b + R) % q"
        self.assertIn(old, py_source)
        py_mutant = self.work / "digit_mutant.py"
        py_mutant.write_text(py_source.replace(old, "(x * b + R + (k == 1)) % q", 1))
        mutants = [(sys.executable, str(py_mutant))]
        if self.c_available:
            source = (ROOT / "mersenne_rows_gmp.c").read_text()
            old = "mpz_add(h[i], h[i], R);"
            self.assertIn(old, source)
            path = self.work / "digit_mutant.c"
            path.write_text(source.replace(old, old + "\n            if (k == 1) mpz_add_ui(h[i], h[i], 1);", 1))
            binary = self.work / "digit_mutant"
            built = run("cc", "-std=c99", "-O2", "-Wall", "-Wextra", "-Werror",
                        "-o", str(binary), str(path), "-lgmp")
            self.assertEqual(built.returncode, 0, built.stderr)
            mutants.append((str(binary),))
        for program in mutants:
            for p in (7, 61, 89, 127, 122):
                with self.subTest(program=program, p=p):
                    result = run(*program, str(p))
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("clean=yes value(mod)=WRONG", result.stdout)
                    self.assertIn("moduli=3/3" if p == 7 else "moduli=2/3", result.stdout)

    def test_default_and_invalid_input(self):
        ulong_max = (1 << (8 * ctypes.sizeof(ctypes.c_ulong))) - 1
        bad = [("",), ("0",), ("1",), ("-1",), ("garbage",),
               ("7junk",), ("7", "unknown"), ("7", "full", "extra")]
        for program in self.programs():
            with self.subTest(program=program, args=()):
                result = run(*program)
                self.assertEqual(result.returncode, 0)
                self.assertIn("p=7 row=9", result.stdout)
            self.assertEqual(run(*program, "--help").returncode, 0)
            invalid = bad + ([(str(ulong_max - 2),), (str(ulong_max + 1),),
                              (str(ulong_max - 3), "full")] if program[0] == str(self.c_binary) else [])
            for args in invalid:
                with self.subTest(program=program, args=args):
                    result = run(*program, *args)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_removed_project_caps_without_large_allocation(self):
        spec = importlib.util.spec_from_file_location("mersenne_rows", ROOT / "mersenne_rows.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.exponent("136279841"), 136279841)
        self.assertEqual(module.exponent("1000001"), 1000001)
        for program in self.programs():
            with self.subTest(program=program):
                result = run(*program, "1000", "full")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("value(full)=ok", result.stdout)

    def test_full_mismatch_sets_failure_even_if_modular_checks_pass(self):
        py_source = (ROOT / "mersenne_rows.py").read_text()
        self.assertIn("value_full = v == 1 << e", py_source)
        py_mutant = self.work / "mutant.py"
        py_mutant.write_text(py_source.replace("value_full = v == 1 << e",
                                               "value_full = v == 1 << (e + 1)", 1))
        mutants = [(sys.executable, str(py_mutant))]
        if self.c_available:
            c_source = (ROOT / "mersenne_rows_gmp.c").read_text()
            self.assertIn("mpz_setbit(t, (mp_bitcnt_t)(p * n));", c_source)
            c_mutant = self.work / "mutant.c"
            c_mutant.write_text(c_source.replace("mpz_setbit(t, (mp_bitcnt_t)(p * n));",
                                                 "mpz_setbit(t, (mp_bitcnt_t)(p * n + 1));", 1))
            binary = self.work / "mutant"
            built = run("cc", "-std=c99", "-O2", "-o", str(binary), str(c_mutant), "-lgmp")
            self.assertEqual(built.returncode, 0, built.stderr)
            mutants.append((str(binary),))
        for program in mutants:
            with self.subTest(program=program):
                result = run(*program, "7", "full")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("clean=yes value(mod)=ok value(full)=WRONG", result.stdout)

    def test_installer_and_runner(self):
        target = self.work / "chosen folder with spaces"
        source_files = [path for path in ROOT.rglob("*") if path.is_file() and "__pycache__" not in path.parts]
        before = [digest(path) for path in source_files]
        install = (sys.executable, str(ROOT / "setup" / "install.py"))
        self.assertEqual(run(*install, str(target)).returncode, 0)
        self.assertEqual(run(*install, str(target)).returncode, 0)
        spec = importlib.util.spec_from_file_location("installer", ROOT / "setup" / "install.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual({str(path.relative_to(target)) for path in target.rglob("*") if path.is_file()},
                         set(module.FILES))
        for referenced in ("PASCAL_VE_NP_ADIM_ADIM.md", "PASCAL_VE_NP_ADIM_ADIM.pdf", "README.md", "setup/install.py", "tests/test_local.py", "tr/README.md", "tr/note.md", "tr/note.pdf", "tr/tables/theorems.txt",
                           "NP_CARRY_FREE_ROW_BOUND.md", "NP_CARRY_FREE_ROW_BOUND.pdf", "tr/NP_ELDESIZ_SATIR_SINIRI.md", "tr/NP_ELDESIZ_SATIR_SINIRI.pdf",
                           "tests/verify_np.py", "tests/test_np.py", "tests/np_verification.json",
                           "tables/theorems.txt", 
                           "coordinates_en.pdf", "tr/coordinates_tr.pdf"):
            self.assertTrue((target / referenced).is_file(), referenced)
        second = self.work / "second chosen folder"
        self.assertEqual(run(sys.executable, str(target / "setup" / "install.py"), str(second)).returncode, 0)
        self.assertEqual(run("sh", str(second / "run.sh"), "7", "full").returncode, 0)
        self.assertEqual([digest(path) for path in source_files], before)
        self.assertEqual(run("sh", str(ROOT / "run.sh"), "7", "full").returncode, 0)
        for wrapper in ("run.sh", "run.command"):
            with self.subTest(wrapper=wrapper):
                result = run("sh", str(target / wrapper), "7", "full")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("value(full)=ok", result.stdout)
                self.assertEqual(run("sh", str(target / wrapper), "3").returncode, 1)
                self.assertEqual(run("sh", str(target / wrapper), "bad").returncode, 2)
        conflict = target / "run.sh"
        marker = target / "unrelated.txt"
        marker.write_text("keep me\n")
        conflict.write_text("unrelated content\n")
        before_conflict = conflict.read_bytes()
        self.assertEqual(run(*install, str(target)).returncode, 2)
        self.assertEqual(conflict.read_bytes(), before_conflict)
        self.assertEqual(run(*install, str(target), "--overwrite").returncode, 0)
        self.assertEqual(conflict.read_bytes(), (ROOT / "run.sh").read_bytes())
        self.assertEqual(marker.read_text(), "keep me\n")
        nested = self.work / "nested collision"
        nested.mkdir()
        (nested / "tr").write_text("unrelated directory name\n")
        self.assertEqual(run(*install, str(nested)).returncode, 2)
        self.assertFalse((nested / "mersenne_rows.py").exists())
        self.assertEqual((nested / "tr").read_text(), "unrelated directory name\n")
        for rejected in (ROOT, ROOT / "nested", ROOT.parent):
            self.assertEqual(run(*install, str(rejected)).returncode, 2)
        self.assertFalse((ROOT / "nested").exists())


if __name__ == "__main__":
    unittest.main()
