# Browser Amnesia

<div style="text-align:center" align="center">
    <img src="https://raw.githubusercontent.com/aaurelions/browseramnesia/master/images/banner.png" width="400">
</div>

Browser Amnesia is a Python tool for macOS to permanently uninstall browsers and delete all related data. It comes in two versions:

- **CLI version** for terminal enthusiasts.
- **GUI version** with a clean and user-friendly interface.

## Features

- Supports popular browsers: Google Chrome, Brave, Opera, Vivaldi, DuckDuckGo, Mullvad, Tor, Puffin and Firefox.
- Deletes all associated data, including preferences, caches, and system files.

## Download

- [Download BrowserAmnesia for macOS](https://github.com/aaurelions/browseramnesia/releases)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/aaurelions/browser_amnesia.git
cd browser_amnesia
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install the CLI tool:

```bash
pip install .
```

## GUI Version

1. Run the GUI script directly:

```bash
python browser_amnesia_gui.py
```

2. Alternatively, build a macOS .app using pyinstaller:

```bash
pyinstaller --onefile --noconsole --windowed --icon=images/logo.icns --add-data "images:images" browser_amnesia_gui.py
```

## Usage

#### CLI Version

- List all supported browsers:

```bash
browser_amnesia list-browsers
```

- Uninstall a specific browser:

```bash
browser_amnesia uninstall "Google Chrome"
```

- Uninstall all browsers:

```bash
browser_amnesia uninstall-all
```

#### GUI Version

Run the GUI script and follow the interactive interface to uninstall individual browsers or all browsers at once.

- Supported Browsers
  - Google Chrome
  - Brave
  - Opera
  - Vivaldi
  - DuckDuckGo
  - Mullvad
  - Firefox
  - Tor
  - Puffin

## License

MIT License

!!! Not tested with all browsers, use at your own risk !!!
