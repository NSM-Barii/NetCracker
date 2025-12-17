"""NetCracker - WiFi security assessment tool

Main entry point that handles dependency validation and application startup.
"""

import sys
import subprocess
from typing import List


class DependencyManager:
    """Manages application dependencies and installation."""

    REQUIRED_PACKAGES = [
        "rich",
        "scapy",
        "pyfiglet",
        "pyttsx3",
        "pywifi",
        "manuf",
        "mac-vendor-lookup",
        "requests"
    ]

    @staticmethod
    def check_dependencies() -> bool:
        """Check if all required dependencies are installed."""
        try:
            from rich.console import Console
            import pywifi
            from scapy.all import sniff
            import pyfiglet
            import pyttsx3

            return True

        except ImportError as e:
            print(f"Missing dependency: {e}")
            return False

    @classmethod
    def install_dependencies(cls) -> bool:
        """Install missing dependencies via pip."""
        print("\nInstalling dependencies...")

        for package in cls.REQUIRED_PACKAGES:
            try:
                print(f"Installing {package}...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"✓ {package} installed")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install {package}")
                return False

        return True

    @staticmethod
    def prompt_install() -> bool:
        """Ask user if they want to install dependencies."""
        response = input("\nInstall missing dependencies? (y/n): ").strip().lower()
        return response in ["y", "yes"]


def main():
    """Application entry point."""

    # Check dependencies
    if not DependencyManager.check_dependencies():
        if DependencyManager.prompt_install():
            if not DependencyManager.install_dependencies():
                print("\nFailed to install dependencies. Exiting.")
                sys.exit(1)
            print("\nDependencies installed successfully!")
        else:
            print("Dependencies required to run. Exiting.")
            sys.exit(1)

    # Import and run UI after dependency check
    try:
        from rich.console import Console
        from nsm_ui import MainUI

        console = Console()
        console.print("✓ Dependency check complete", style="bold green")

        MainUI.main()

    except ImportError as e:
        print(f"Error importing modules: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
