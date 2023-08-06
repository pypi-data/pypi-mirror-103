import argparse
import sys

from PySide6 import QtWidgets

import twobodyproblem_gui
from twobodyproblem_gui.entry import EntryWindow

if __name__ == "__main__":
    # add CLI arguments
    parser = argparse.ArgumentParser(
        prog="twobodyproblem_gui",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="python/python3 -m twobodyproblem_gui [-h | -v ] [-d]",
        description="This is a graphical user interface for the package "
                    "twobodyproblem.\nTo run the GUI normally, just run the "
                    "command without any of the optional arguments.",
        epilog="For further information, "
               "visit:\nhttps://github.com/Two-Body-Problem/twobodyproblem"
               "-simulation-python-gui"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version="%(prog)s version " + twobodyproblem_gui.__version__,
        help="show the version of the program and exit"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="run the program with debug info prints"
    )
    args = parser.parse_args()

    if args.debug:
        print("debugging activated...")
        print("passed arguments:", end=" ")
        print(sys.argv)

    # run the GUI app
    app = QtWidgets.QApplication(sys.argv)
    window = EntryWindow(debug=args.debug)
    window.ui.show()
    sys.exit(app.exec_())
