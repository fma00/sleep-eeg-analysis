# Sleep EEG Analysis: From Signal Processing to Machine Learning and Deep Learning

Course material for the Cajal course "Neurobiology of Sleep" (Bordeaux, Nov–Dec 2026).

## Setup

### macOS
1. **git:** open Terminal and run `git --version`. If a dialog asks to install the Command Line Tools, click *Install* and wait.
2. **uv:** `curl -LsSf https://astral.sh/uv/install.sh | sh`, then **close and reopen Terminal**.
3. **VS Code:** install from https://code.visualstudio.com, then add the **Python** and **Jupyter** extensions.
4. **Get the course code:**
   ```bash
   mkdir -p ~/courses && cd ~/courses
   git clone https://github.com/fma00/sleep-eeg-analysis.git
   cd sleep-eeg-analysis
   ```

### Windows
1. **git:** install Git for Windows from https://git-scm.com (default options), or run `winget install Git.Git`.
2. **uv:** in PowerShell, run
   `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`,
   then **close and reopen PowerShell**.
3. **VS Code:** install the *User Installer* from https://code.visualstudio.com (tick "Add to PATH"), then add the **Python** and **Jupyter** extensions.
4. **Get the course code:**
   ```powershell
   mkdir $HOME\courses -Force; cd $HOME\courses
   git clone https://github.com/fma00/sleep-eeg-analysis.git
   cd sleep-eeg-analysis
   ```

> **Why not Documents or Desktop?** These folders are often synced to iCloud (Mac) or OneDrive (Windows). Syncing the thousands of files in `.venv` slows everything down and can break the environment. A plain folder in your home directory avoids this.

### Linux
Works on x86_64 with Ubuntu 22.04+, Debian 12+, Fedora 35+ or similar (glibc 2.34 or newer). Older systems such as Ubuntu 20.04 are not supported.
1. **git, curl and the libraries the interactive plot window (Qt) needs.** On Ubuntu/Debian:
   ```bash
   sudo apt install git curl libegl1 libgl1 libfontconfig1 libdbus-1-3 libxkbcommon-x11-0 \
     libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
     libxcb-render-util0 libxcb-shape0 libxcb-xinerama0 libxcb-xfixes0 libxcb-xkb1
   ```
   On Fedora: `sudo dnf install git curl mesa-libEGL libxkbcommon-x11 xcb-util-cursor xcb-util-wm xcb-util-image xcb-util-keysyms xcb-util-renderutil`
2. **uv:** `curl -LsSf https://astral.sh/uv/install.sh | sh`, then open a new terminal.
3. **VS Code:** install the .deb/.rpm from https://code.visualstudio.com, then add the **Python** and **Jupyter** extensions.
4. **Get the course code:** same as macOS (`mkdir -p ~/courses && cd ~/courses && git clone …`).

If the check says `Could not load the Qt platform plugin "xcb"`, a library from step 1 is missing.

### All systems
5. **Create the environment:** `uv sync` (downloads Python and all packages into `.venv`, takes 1–3 min)
6. **Data:** unzip the course data into the `data/` folder
7. **Check:** `uv run python check_setup.py`. An MNE window with EEG signals opens. Close it, and you should see `✅ Setup OK`.
8. **VS Code:** *File → Open Folder* → `sleep-eeg-analysis`. Open a notebook and select the `.venv` kernel (top right).
   If you installed uv while VS Code was open, **quit and restart VS Code** so it sees the new PATH.

**Always start Python through uv** (`uv run python …`) or through the `.venv` kernel. You don't need a system Python, and on Windows typing plain `python` may open the Microsoft Store instead.

### Using another editor instead of VS Code
That's fine, as long as it uses the course environment (`.venv`):
- **JupyterLab** (easiest alternative, since the course material is notebooks): `uv run --with jupyterlab jupyter lab`
- **Spyder:** *Preferences → Python interpreter → Use the following interpreter* → `.venv/bin/python` (Windows: `.venv\Scripts\python.exe`). Spyder then asks for `spyder-kernels`: install the version it names with `uv pip install "spyder-kernels==<version>"`. Spyder doesn't open notebooks, so use JupyterLab for those.
- **PyCharm:** *Settings → Project → Python Interpreter → Add → Existing* → the same `.venv` path.

The instructor can only support VS Code during the course.

### Windows on ARM (e.g. Snapdragon laptops)
Some packages have no native ARM build. Use the x64 Python instead, which runs under Windows' built-in emulation:
`uv sync --python cpython-3.12-windows-x86_64-none`

## Updating
`git pull` gets new material, and `uv sync` installs any new packages.
