# cli.py

import argparse
from mediagui.gui import main as gui_main

def main():
    """CLI entry point for mediaGUI."""
    parser = argparse.ArgumentParser(
        prog="mediagui",
        description="mediaGUI - A graphical media application. For help, use --help."
    )
    parser.add_argument(
        "--view",
        type=int,
        choices=[0, 1],
        help="Launch mediaGUI with a specific view: 0 for default view with fixed frame extraction, 1 for every __ frame extraction.",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="MediaGUI 1.0.0",
        help="Show the version of MediaGUI."
    )
    
    args = parser.parse_args()

    if args.view is not None:
        print(f"Launching mediaGUI with view {args.view}...")
        gui_main(view=args.view)
    else:
        print("Launching mediaGUI...")
        gui_main()

if __name__ == "__main__":
    main()
