import maya.OpenMayaUI as omui
import maya.cmds as mc
import importlib
import sys

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QDialog, QWidget, QHBoxLayout, QComboBox
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QDialog, QWidget, QHBoxLayout, QComboBox

try:
    from shiboken6 import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance

from renameThemAll.outliner_ui import OutlinerUI
from renameThemAll.renamer_ui import RenamerUI
from renameThemAll.lexicon_ui import LexiconUI
from renameThemAll.constants import NO_LEXICON


def maya_main_window():
    """
    Return the Maya main window widget as a Python object.

    Returns
    -------
    QWidget
        The Maya main window widget.
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


class RenameThemAllUI(QDialog):
    """
    A dialog for managing nomenclature in Maya.

    This class provides a user interface for outlining and renaming objects in Maya.

    Attributes
    ----------
    WINDOW_TITLE : str
        The title of the dialog window.
    """

    WINDOW_TITLE = "Rename Them All"

    def __init__(self, parent=maya_main_window()):
        """
        Initialize the RenameThemAllUI dialog.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget. Defaults to Maya's main window.
        """
        super().__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if mc.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        elif mc.about(macOS=True):
            self.setWindowFlags(Qt.Tool)

        self.setMinimumWidth(670)
        self.setMinimumHeight(800)

        self.combo_lexicon = QComboBox()
        self.combo_lexicon.addItem(NO_LEXICON)
        self.combo_lexicon.setCurrentText(NO_LEXICON)
        self.outliner_ui = OutlinerUI(combo_lexicon=self.combo_lexicon)
        tree_widget = self.outliner_ui.tree_widget
        self.lexicon_ui = LexiconUI(tree_widget, self.combo_lexicon)
        self.outliner_ui.tree_widget.lexicon_ui = self.lexicon_ui   
        self.renamer_ui = RenamerUI(tree_widget, self.lexicon_ui)

        self.create_layout()

        self.outliner_ui.restart_application.connect(self.restart_application)

    def create_layout(self):
        """
        Create the main layout of the dialog.

        This method sets up the horizontal layout and adds the outliner and renamer widgets.
        """
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.outliner_ui)
        main_layout.addWidget(self.renamer_ui)

    def closeEvent(self, event):
        """
        Handle the close event for the dialog.

        This method is called when the dialog is closed. It cleans up the resources 
        used by the dialog and calls the superclass closeEvent method.

        Parameters
        ----------
        event : QCloseEvent
            The close event object.

        Returns
        -------
        None

        Notes
        -----
        This method calls the cleanup method of the outliner_ui before closing.
        """
        self.outliner_ui.cleanup()
        super().closeEvent(event)

    def keyPressEvent(self, event):
        """
        Intercept keyboard events when the window has focus.

        This method specifically blocks Ctrl+Z by explicitly accepting it.

        Parameters
        ----------
        event : QKeyEvent
            The keyboard event to handle.

        Returns
        -------
        None
        """
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z:
            event.accept()  
            return 
        else:
            super().keyPressEvent(event)  

    def restart_application(self):
        """
        Restart the application by reloading all modules.

        This method reloads all the application modules and creates a new instance
        of the main UI window.

        Returns
        -------
        None

        Notes
        -----
        The method will attempt to reload each module individually and print any
        errors that occur during the reload process.
        """
        modules_to_reload = [
            'renameThemAll.about_dialog',
            'renameThemAll.default_settings',
            'renameThemAll.constants',
            'renameThemAll.outliner_logics',
            'renameThemAll.name_structure_inspector',      
            'renameThemAll.outliner_text_colored',
            'renameThemAll.outliner_custom_delegate',
            'renameThemAll.outliner_custom_tree_widget',
            'renameThemAll.user_settings_logics',
            'renameThemAll.menu_logics',
            'renameThemAll.user_settings_ui',    
            'renameThemAll.menu_ui',
            'renameThemAll.outliner_ui',
            'renameThemAll.renamer_logics',
            'renameThemAll.renamer_ui',
            'renameThemAll.lexicon_logics',
            'renameThemAll.lexicon_ui',
            'renameThemAll.main_ui',
        ]
        
        for module_name in modules_to_reload:
            try:
                if module_name in sys.modules:
                    importlib.reload(sys.modules[module_name])
            except Exception as e:
                print(f"Error while reloading {module_name}: {e}")
        
        new_instance = RenameThemAllUI()
        new_instance.show()
        self.close()
        
