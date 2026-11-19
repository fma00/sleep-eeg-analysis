"""Course setup check.

Run from the repository folder:

    uv run python check_setup.py

It checks the Python version and packages, loads one Sleep-EDF night from
data/ and opens the interactive MNE browser. Close the browser window to finish.

Options:
    --no-gui       skip opening the browser (for automated tests)
    --auto-close   open the browser and close it automatically after 5 s
"""

import importlib
import importlib.util
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Windows consoles/pipes may use cp1252, which can't print emoji
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent
DATA = REPO / "data"
PACKAGES = ["mne", "mne_qt_browser", "PyQt6", "yasa", "pyriemann", "lightgbm",
            "numpy", "scipy", "pandas", "matplotlib", "sklearn", "ipykernel"]

ok = True


def fail(msg):
    global ok
    ok = False
    print(f"  ❌ {msg}")


def lightgbm_loads():
    """Import lightgbm in a fresh process (a failed native load can't be retried in-process)."""
    r = subprocess.run([sys.executable, "-c", "import lightgbm"], capture_output=True, text=True)
    return r.returncode == 0


def fix_lightgbm_macos():
    """lightgbm's macOS wheels need libomp (OpenMP) but don't ship it; they only look in
    Homebrew/MacPorts folders. scikit-learn ships its own libomp, so point lightgbm there."""
    lgbm_spec = importlib.util.find_spec("lightgbm")
    sk_spec = importlib.util.find_spec("sklearn")
    if lgbm_spec is None or sk_spec is None:
        return False
    lib = Path(lgbm_spec.origin).parent / "lib" / "lib_lightgbm.dylib"
    omp = Path(sk_spec.origin).parent / ".dylibs" / "libomp.dylib"
    tool = shutil.which("install_name_tool")
    if not (lib.exists() and omp.exists() and tool):
        print("  ⚠️  Can't repair automatically (Command Line Tools missing?). "
              "Run `xcode-select --install`, or `brew install libomp`, then re-run this check.")
        return False
    rpath = "@loader_path/" + str(Path("..", "..", "sklearn", ".dylibs"))
    subprocess.run([tool, "-add_rpath", rpath, str(lib)], capture_output=True)
    subprocess.run(["codesign", "--force", "--sign", "-", str(lib)], capture_output=True)
    return lightgbm_loads()


print("== System ==")
print(f"  Python {platform.python_version()} on {platform.system()} {platform.release()} ({platform.machine()})")
if not (3, 12) <= sys.version_info[:2] < (3, 14):
    fail("Python 3.12 or 3.13 expected. Did you run this with `uv run`?")
if ".venv" not in sys.prefix:
    print(f"  ⚠️  Not running from the project's .venv ({sys.prefix}). Use `uv run python check_setup.py`.")

print("== Packages ==")
if sys.platform == "darwin" and not lightgbm_loads():
    print("  🔧 lightgbm can't find the OpenMP library (libomp); repairing...")
    print("  ✅ lightgbm repaired" if fix_lightgbm_macos() else "  ❌ lightgbm repair failed")
for name in PACKAGES:
    try:
        mod = importlib.import_module(name)
        version = getattr(mod, "__version__", None)
        if version is None and name == "PyQt6":
            from PyQt6.QtCore import PYQT_VERSION_STR as version
        print(f"  ✅ {name:15s} {version or ''}")
    except Exception as e:  # noqa: BLE001
        fail(f"{name}: {e}")

print("== Data ==")
psg_files = sorted(DATA.glob("**/*-PSG.edf"))
hyp_files = sorted(DATA.glob("**/*-Hypnogram.edf"))
print(f"  Found {len(psg_files)} PSG and {len(hyp_files)} hypnogram files in {DATA}")
if not psg_files:
    fail("No *-PSG.edf files found. Unzip the course data into the data/ folder.")

raw = None
if ok:
    import mne

    mne.set_log_level("ERROR")
    psg = psg_files[0]
    # Sleep-EDF hypnogram names share the first 7 characters with the PSG (e.g. SC4001E0 / SC4001EC)
    hyp = next((h for h in hyp_files if h.name[:7] == psg.name[:7]), None)
    try:
        raw = mne.io.read_raw_edf(psg, preload=True, infer_types=True)
        print(f"  ✅ Loaded {psg.name}: {raw.times[-1] / 3600:.1f} h, {raw.info['sfreq']:.0f} Hz, channels {raw.ch_names}")
        if hyp is not None:
            raw.set_annotations(mne.read_annotations(hyp), emit_warning=False)
            print(f"  ✅ Loaded {hyp.name}: {len(raw.annotations)} annotations")
        else:
            print("  ⚠️  No matching hypnogram found (not needed for this check)")
    except Exception as e:  # noqa: BLE001
        fail(f"Could not load {psg.name}: {e}")

print("== Interactive browser ==")
if raw is not None and "--no-gui" not in sys.argv:
    try:
        import mne

        mne.viz.set_browser_backend("qt")
        kwargs = dict(duration=30, n_channels=len(raw.ch_names), scalings="auto",
                      title="Setup check: close this window when you see the signals")
        if "--auto-close" in sys.argv:  # automated tests: open, wait 5 s, close
            from PyQt6.QtCore import QTimer
            from PyQt6.QtWidgets import QApplication

            fig = raw.plot(block=False, **kwargs)
            QTimer.singleShot(5000, fig.close)
            QApplication.instance().exec()
        else:
            print("  Opening the MNE browser... close the window to finish.")
            raw.plot(block=True, **kwargs)
        print("  ✅ Qt browser worked")
    except Exception as e:  # noqa: BLE001
        fail(f"Qt browser failed: {e}\n"
             "     Fallback: mne.viz.set_browser_backend('matplotlib') in your notebook. Ask Flo.")
elif "--no-gui" in sys.argv:
    print("  (skipped, --no-gui)")

print()
print("✅ Setup OK. You're ready!" if ok else "❌ Setup incomplete. See the messages above, or ask Flo.")
sys.exit(0 if ok else 1)
