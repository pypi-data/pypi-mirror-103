import os
from pathlib import Path

from PySide6 import QtWidgets, QtUiTools, QtCore
from twobodyproblem.options import Options


class SettingsWindow(QtWidgets.QMainWindow):
    """window for settings

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
        super(SettingsWindow, self).__init__(*args, parent, **kwargs)
        self.parent = parent
        self.debug = debug
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.ui = QtUiTools.QUiLoader().load(
            QtCore.QFile(self.directory + "/ui/settings.ui"))
        self.ui.actionSpeichern.triggered.connect(lambda: self.save())
        self.ui.actionSpeichern_unter.triggered.connect(
            lambda: self.save(default=False))
        self.ui.actionLaden.triggered.connect(lambda: self.load())
        self.ui.actionLaden_von.triggered.connect(
            lambda: self.load(default=False))
        self.ui.actionVerlassen.triggered.connect(self.ui.close)
        self.ui.b_ok.clicked.connect(lambda: (self.save(), self.ui.close()))
        self.ui.b_close.clicked.connect(self.ui.close)
        self.ui.show_pointers.stateChanged.connect(
            self.show_pointers_changed_action)
        self.ui.tabWidget.setCurrentIndex(0)

        self.load()
        self.show_pointers_changed_action()

    def fill(self, options: Options):
        """fill in the given options

        args:
            options: Options object to be filled in
        """
        self.ui.canvas_width.setValue(options.canvas.width)
        self.ui.canvas_height.setValue(options.canvas.height)
        self.ui.color_objects_r.setValue(options.colors.bodies.x)
        self.ui.color_objects_g.setValue(options.colors.bodies.y)
        self.ui.color_objects_b.setValue(options.colors.bodies.z)
        self.ui.color_pointer_r.setValue(options.colors.pointers.x)
        self.ui.color_pointer_g.setValue(options.colors.pointers.y)
        self.ui.color_pointer_b.setValue(options.colors.pointers.z)
        self.ui.show_pointers.setChecked(options.pointers)
        self.ui.update_rate.setValue(options.rate)
        self.ui.max_seconds.setValue(options.sim_time)
        self.ui.t_factor.setValue(options.delta_t)
        self.ui.do_central_centered.setChecked(options.central_centered)
        self.ui.do_testing.setChecked(options.testing)
        self.ui.do_restart.setChecked(options.restart)

    def get(self) -> Options:
        """get the entered options for further use

        returns: Options
        """
        options = Options(canvas_width=self.ui.canvas_width.value(),
                          canvas_height=self.ui.canvas_height.value(),
                          color_objects_r=self.ui.color_objects_r.value(),
                          color_objects_g=self.ui.color_objects_g.value(),
                          color_objects_b=self.ui.color_objects_r.value(),
                          color_pointers_r=self.ui.color_pointer_r.value(),
                          color_pointers_g=self.ui.color_pointer_g.value(),
                          color_pointers_b=self.ui.color_pointer_b.value(),
                          show_pointers=int(self.ui.show_pointers.isChecked()),
                          update_rate=self.ui.update_rate.value(),
                          max_seconds=self.ui.max_seconds.value(),
                          delta_t=self.ui.t_factor.value(),
                          central_centered=int(
                              self.ui.do_central_centered.isChecked()),
                          testing=int(self.ui.do_testing.isChecked()),
                          restart=int(self.ui.do_restart.isChecked()))
        if self.debug:
            print("these settings are being used:", end=" ")
            print(options.to_dict())
        return options

    def save(self, default=True):
        """save settings to file

        args:
            default: True if saving to default file (default True)
        """
        dir_path = str(Path.home()) + "/Documents/TwoBodyProblem"
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if default:
            self.get().save()
            if self.debug:
                print("settings saved to: " + dir_path +
                      "/default/settings.yml")
        else:
            name = QtWidgets.QFileDialog.getSaveFileName(
                parent=self, caption="Einstellungen speichern",
                dir=dir_path, filter="YAML (*.yml)")
            if name[0] != "":
                self.get().save(name[0])
                if self.debug:
                    print("settings saved to: " + name[0])

    def load(self, default=True):
        """load settings file

        args:
            default: True if loading from default file (default True)
        """
        dir_path = str(Path.home()) + "/Documents/TwoBodyProblem"
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if default:
            try:
                self.fill(Options.from_file())
                if self.debug:
                    print("settings loaded from: " + dir_path +
                          "/default/settings.yml")
            except FileNotFoundError:
                err = QtWidgets.QMessageBox()
                err.setIcon(QtWidgets.QMessageBox.Critical)
                err.setText("keine gespeicherten Einstellungen vorhanden")
                err.setWindowTitle("Fehler")
                err.exec()
        else:
            name = QtWidgets.QFileDialog.getOpenFileName(
                parent=self, caption="Einstellungsdatei öffnen",
                dir=dir_path, filter="YAML (*.yml))")
            if name[0] != "":
                self.fill(Options.from_file(name[0]))
                if self.debug:
                    print("settings loaded from: " + name[0])

    def show_pointers_changed_action(self):
        """changes enabled state of the pointer color choosing fields"""
        if self.ui.show_pointers.isChecked():
            self.ui.color_pointer_r.setEnabled(True)
            self.ui.color_pointer_g.setEnabled(True)
            self.ui.color_pointer_b.setEnabled(True)
        else:
            self.ui.color_pointer_r.setEnabled(False)
            self.ui.color_pointer_g.setEnabled(False)
            self.ui.color_pointer_b.setEnabled(False)
