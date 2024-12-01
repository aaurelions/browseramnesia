import os
import subprocess
import click

# Define paths to remove for each browser
BROWSER_PATHS = {
    "Google Chrome": [
        "/Applications/Google Chrome.app/",
        "/Library/LaunchAgents/com.google.keystone*",
        "/Library/Application Support/Google/Chrome",
        "~/Library/Preferences/com.google.Chrome*",
        "~/Applications/Chrome Apps.localized/",
        "~/Library/Application Support/CrashReporter/Google Chrome",
        "~/Library/Caches/com.google.Chrome*",
        "~/Library/Saved Application State/com.google.Chrome.savedState/",
        "~/Library/Google/GoogleSoftwareUpdate/Actives/com.google.Chrome",
        "~/Library/Google/Google Chrome*",
    ],
    "Brave": [
        "/Applications/Brave Browser.app/",
        "~/Library/Application Support/BraveSoftware/",
        "~/Library/Caches/BraveSoftware/",
        "~/Library/Saved Application State/com.brave.Browser.savedState/",
    ],
    "Opera": [
        "/Applications/Opera.app/",
        "~/Library/Application Support/com.operasoftware.Opera/",
        "~/Library/Caches/com.operasoftware.Opera/",
        "~/Library/Saved Application State/com.operasoftware.Opera.savedState/",
    ],
    "Firefox": [
        "/Applications/Firefox.app/",
        "~/Library/Application Support/Firefox/",
        "~/Library/Caches/Firefox/",
        "~/Library/Saved Application State/org.mozilla.firefox.savedState/",
    ],
    "Puffin": [
        "/Applications/Puffin Secure Browser.app/",
        "~/Library/Application Support/Puffin Secure Browser/",
        "~/Library/Caches/Puffin Secure Browser/",
        "~/Library/Saved Application State/com.cloudmosa.puffin.savedState/",
    ],
    "Tor": [
        "/Applications/Tor Browser.app/",
        "~/Library/Application Support/TorBrowser-Data/",
        "~/Library/Caches/org.torproject.TorBrowser/",
        "~/Library/Saved Application State/org.torproject.TorBrowser.savedState/",
    ],
    "DuckDuckGo": [
        "/Applications/DuckDuckGo.app/",
        "~/Library/Application Support/DuckDuckGo/",
        "~/Library/Caches/DuckDuckGo/",
    ],
    "Mullvad": [
        "/Applications/Mullvad Browser.app/",
        "~/Library/Application Support/Mullvad/",
        "~/Library/Caches/Mullvad/",
    ],
    "Vivaldi": [
        "/Applications/Vivaldi.app/",
        "~/Library/Application Support/Vivaldi/",
        "~/Library/Caches/com.vivaldi.Vivaldi/",
        "~/Library/Saved Application State/com.vivaldi.Vivaldi.savedState/",
    ]
}

def remove_browser_files(browser_name):
    """Remove all files and directories related to the specified browser."""
    paths = BROWSER_PATHS.get(browser_name, [])
    for path in paths:
        try:
            resolved_path = os.path.expanduser(path)
            if os.path.exists(resolved_path):
                print(f"Removing {resolved_path}")
                subprocess.run(["rm", "-rf", resolved_path], check=True)
        except Exception as e:
            print(f"Error removing {resolved_path}: {e}")

@click.group()
def cli():
    """Browser Amnesia: Permanently uninstall browsers and delete all related data."""
    pass

@cli.command()
def list_browsers():
    """List all supported browsers."""
    click.echo("Supported Browsers:")
    for browser in BROWSER_PATHS.keys():
        click.echo(f"- {browser}")

@cli.command()
@click.argument("browser_name", type=str)
def uninstall(browser_name):
    """Uninstall a specific browser."""
    if browser_name in BROWSER_PATHS:
        click.confirm(
            f"Are you sure you want to permanently uninstall {browser_name} and delete all related data?",
            abort=True
        )
        remove_browser_files(browser_name)
        click.echo(f"{browser_name} has been permanently uninstalled.")
    else:
        click.echo("Browser not recognized. Use `browser_amnesia list-browsers` to see supported browsers.")

@cli.command()
def uninstall_all():
    """Permanently uninstall all supported browsers."""
    click.confirm(
        "Are you sure you want to permanently uninstall ALL browsers and delete all related data?",
        abort=True
    )
    for browser_name in BROWSER_PATHS.keys():
        click.echo(f"Uninstalling {browser_name}...")
        remove_browser_files(browser_name)
    click.echo("All supported browsers have been permanently uninstalled.")

if __name__ == "__main__":
    cli()