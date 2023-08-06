import os
import sys
from pathlib import Path

from PySide6 import QtGui, QtWidgets, QtCore, QtUiTools
from twobodyproblem import preset
from twobodyproblem.values import Values
from twobodyproblem.visualization.simulation import Simulation

from twobodyproblem_gui.examples import ExamplesWindow
from twobodyproblem_gui.settings import SettingsWindow


class EntryWindow(QtWidgets.QMainWindow):
    """main window for inputs

    inherits from: QtWidgets.QMainWindow
    """

    def __init__(self, *args, parent=None, debug=False, **kwargs):
        """constructor extends QtWidgets.QMainWindow constructor

        args:
            parent: parent window (default None)
            debug: true if should be run in debug mode (default False)
            *args and **kwargs: additional args to be passed
        """
        # set up UI
        super(EntryWindow, self).__init__(*args, parent, **kwargs)
        self.parent = parent
        self.debug = debug
        self.directory = os.path.dirname(os.path.realpath(__file__))
        if self.debug:
            print("directory: " + self.directory)
        self.ui = QtUiTools.QUiLoader().load(
            QtCore.QFile(self.directory + "/ui/entry.ui"))
        self.ui.setWindowIcon(QtGui.QIcon(self.directory + "/ui/icon.gif"))
        # create other windows
        self.w_examples = ExamplesWindow(parent=self)
        self.w_settings = SettingsWindow(parent=self)

        # add button and action functionality
        self.ui.b_ok.clicked.connect(lambda: Simulation(
            values=self.get(),
            options=self.w_settings.get()).start())
        self.ui.b_reset.clicked.connect(self.clear)
        self.ui.actionVerlassen.triggered.connect(self.ui.close)
        self.ui.actionNeu_starten.triggered.connect(self.restart)
        self.ui.actionWerte_speichern.triggered.connect(
            lambda: self.save())
        self.ui.actionWertedatei_speichern_unter.triggered.connect(
            lambda: self.save(False))
        self.ui.actiongespeicherte_Werte_laden.triggered.connect(
            lambda: self.load())
        self.ui.actionWertedatei_oeffnen.triggered.connect(
            lambda: self.load(False))
        self.ui.actionVoreinstellungen.triggered.connect(
            self.w_examples.ui.show)
        self.ui.actionEinstellungen.triggered.connect(self.w_settings.ui.show)
        # set the tab for central as "default"
        self.ui.tabWidget.setCurrentIndex(0)

    def restart(self):
        """restart the program"""
        if self.debug:
            print("restarting in debug mode...")
        os.execl(sys.executable, sys.executable, *sys.argv)

    def clear(self):
        """delete all values in all fields"""
        self.ui.central_radius.setText("")
        self.ui.central_mass.setText("")
        self.ui.sat_mass.setText("")
        self.ui.sat_radius.setText("")
        self.ui.distance.setText("")
        self.ui.sat_v0_x.setText("")
        self.ui.sat_v0_y.setText("")
        self.ui.sat_v0_z.setText("")
        self.ui.central_v0_x.setText("")
        self.ui.central_v0_y.setText("")
        self.ui.central_v0_z.setText("")

    def fill_standards(self):
        """fill in the standard values if field is empty or wrongly filled"""
        try:  # check if valid number entered
            float(self.ui.central_mass.text())
        except ValueError:  # enter standard value if an error occurs
            self.ui.central_mass.setText(str(preset.Earth.mass))
        try:
            float(self.ui.central_radius.text())
        except ValueError:
            self.ui.central_radius.setText(str(preset.Earth.radius))
        try:
            float(self.ui.central_v0_x.text())
        except ValueError:
            self.ui.central_v0_x.setText("0")
        try:
            float(self.ui.central_v0_y.text())
        except ValueError:
            self.ui.central_v0_y.setText("0")
        try:
            float(self.ui.central_v0_z.text())
        except ValueError:
            self.ui.central_v0_z.setText("0")

        try:
            float(self.ui.sat_mass.text())
        except ValueError:
            self.ui.sat_mass.setText(str(preset.Sputnik2.mass))
        try:
            float(self.ui.sat_radius.text())
        except ValueError:
            self.ui.sat_radius.setText(str(preset.Sputnik2.radius))
        try:
            float(self.ui.sat_v0_x.text())
        except ValueError:
            self.ui.sat_v0_x.setText("0")
        try:
            float(self.ui.sat_v0_y.text())
        except ValueError:
            self.ui.sat_v0_y.setText("0")
        try:
            float(self.ui.sat_v0_z.text())
        except ValueError:
            self.ui.sat_v0_z.setText("-8000")

        try:
            float(self.ui.distance.text())
        except ValueError:
            self.ui.distance.setText(
                str(preset.distance("EarthSat")))

        if self.debug:
            print("standard values have been applied")

    def fill(self, values: Values):
        """fill in the given values

        args:
            values: Values object to be filled in
        """
        self.ui.central_mass.setText(str(values.central.mass))
        self.ui.central_radius.setText(str(values.central.radius))
        self.ui.central_v0_x.setText(str(values.central.velocity.x))
        self.ui.central_v0_y.setText(str(values.central.velocity.y))
        self.ui.central_v0_z.setText(str(values.central.velocity.z))
        self.ui.sat_mass.setText(str(values.sat.mass))
        self.ui.sat_radius.setText(str(values.sat.radius))
        self.ui.sat_v0_x.setText(str(values.sat.velocity.x))
        self.ui.sat_v0_y.setText(str(values.sat.velocity.y))
        self.ui.sat_v0_z.setText(str(values.sat.velocity.z))
        self.ui.distance.setText(str(values.distance))

    def get(self) -> Values:
        """get the entered values for further use

        returns: Values
        """
        self.fill_standards()
        values = Values(central_mass=float(self.ui.central_mass.text()),
                        central_radius=float(self.ui.central_radius.text()),
                        central_v0_x=float(self.ui.central_v0_x.text()),
                        central_v0_y=float(self.ui.central_v0_y.text()),
                        central_v0_z=float(self.ui.central_v0_z.text()),
                        sat_mass=float(self.ui.sat_mass.text()),
                        sat_radius=float(self.ui.sat_radius.text()),
                        sat_v0_x=float(self.ui.sat_v0_x.text()),
                        sat_v0_y=float(self.ui.sat_v0_y.text()),
                        sat_v0_z=float(self.ui.sat_v0_z.text()),
                        distance=float(self.ui.distance.text()))
        if self.debug:
            print("these values are being used:", end=" ")
            print(values.to_dict())
        return values

    def save(self, default=True):
        """save values to file

        args:
            default: True if saving to default file (default True)
        """
        dir_path = str(Path.home()) + "/Documents/TwoBodyProblem"
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if default:
            self.get().save()
            if self.debug:
                print("values saved to: " + dir_path + "/default/values.yml")
        else:
            name = QtWidgets.QFileDialog.getSaveFileName(
                parent=self, caption="Eingaben speichern",
                dir=dir_path, filter="YAML (*.yml)")
            if name[0] != "":
                self.get().save(name[0])
                if self.debug:
                    print("values saved to: " + name[0])

    def load(self, default=True):
        """load values file

        args:
            default: True if loading from default file (default True)
        """
        dir_path = str(Path.home()) + "/Documents/TwoBodyProblem"
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if default:
            try:
                self.fill(Values.from_file())
                if self.debug:
                    print("values loaded from: " + dir_path +
                          "/default/values.yml")
            except FileNotFoundError:
                err = QtWidgets.QMessageBox()
                err.setIcon(QtWidgets.QMessageBox.Critical)
                err.setText("keine gespeicherten Werte vorhanden")
                err.setWindowTitle("Fehler")
                err.exec()
        else:
            name = QtWidgets.QFileDialog.getOpenFileName(
                parent=self, caption="Wertedatei öffnen",
                dir=dir_path, filter="YAML (*.yml))")
            if name[0] != "":
                self.fill(Values.from_file(name[0]))
                if self.debug:
                    print("values loaded from: " + name[0])
