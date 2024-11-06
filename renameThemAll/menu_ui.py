try:
    from PySide6.QtWidgets import QWidget, QHBoxLayout, QTreeWidget, QMenuBar
    from PySide6.QtGui import QAction
    from PySide6.QtCore import Signal
except ImportError:
    from PySide2.QtWidgets import QWidget, QHBoxLayout, QTreeWidget, QMenuBar, QAction
    
from renameThemAll.menu_logics import MenuLogics
from renameThemAll.about_dialog import AboutDialog
from renameThemAll.user_settings_ui import UserSettingsUI

class MenuUI(QWidget):
    """
    A class representing the menu user interface.

    This class creates a menu bar with display options for shapes, meshes, and legend.

    Parameters
    ----------
    tree_widget : QTreeWidget, optional
        The tree widget to be controlled by the menu actions.
    legend_widget : QWidget, optional
        The legend widget to be controlled by the menu actions.

    Attributes
    ----------
    tree_widget : QTreeWidget
        The tree widget controlled by the menu actions.
    legend_widget : QWidget
        The legend widget controlled by the menu actions.
    is_shapes_hidden : bool
        Flag indicating whether shapes are hidden.
    is_meshes_shown : bool
        Flag indicating whether meshes are shown.
    is_legend_hidden : bool
        Flag indicating whether the legend is hidden.
    """

    restart_application = Signal()

    def __init__(self, tree_widget: QTreeWidget = None, legend_widget: QWidget = None):
        super().__init__()
        self.tree_widget = tree_widget
        self.legend_widget = legend_widget
        self.is_shapes_hidden = True
        self.is_meshes_shown = True
        self.is_legend_shown = False
        self.non_unique_mod = False
        self.create_actions()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
    
    def create_actions(self) -> None:
        """
        Create QActions for the menu items.

        This method initializes the QActions for hiding shapes, showing meshes, and hiding the legend.
        """
        '''self.action_display_shapes = QAction("Hide Shapes", self)
        self.action_display_shapes.setCheckable(True)
        self.action_display_shapes.setChecked(self.is_shapes_hidden)'''

        self.action_display_meshes = QAction("Show Meshes", self)
        self.action_display_meshes.setCheckable(True)
        self.action_display_meshes.setChecked(self.is_meshes_shown)

        '''self.action_display_non_unique = QAction("Non Unique Mod", self)
        self.action_display_non_unique.setCheckable(True)
        self.action_display_non_unique.setChecked(self.non_unique_mod)'''

        self.action_config = QAction("Configuration", self)
        #self.action_colors = QAction("Colors", self)

        self.action_display_legend = QAction("Show Legend", self)
        self.action_display_legend.setCheckable(True)
        self.action_display_legend.setChecked(self.is_legend_shown)

        self.action_about = QAction("About", self)
        #self.action_documentation = QAction("Documentation", self)
    
    def create_widgets(self) -> None:
        """
        Create the menu bar and add menu items.

        This method creates the menu bar and adds the display menu with its actions.
        """
        self.menu_bar = QMenuBar()
        display_menu = self.menu_bar.addMenu("Display")
        #display_menu.addAction(self.action_display_shapes)
        display_menu.addAction(self.action_display_meshes)
        #display_menu.addAction(self.action_display_non_unique)

        config_menu = self.menu_bar.addMenu("Config")
        config_menu.addAction(self.action_config)
        #config_menu.addAction(self.action_colors)

        help_menu = self.menu_bar.addMenu("Help")
        help_menu.addAction(self.action_display_legend)
        help_menu.addAction(self.action_about)
        #help_menu.addAction(self.action_documentation)

    def create_layout(self) -> None:
        """
        Create the layout for the widget.

        This method sets up the horizontal box layout and adds the menu bar to it.
        """
        self.hbox_layout = QHBoxLayout(self)
        self.hbox_layout.setMenuBar(self.menu_bar)
        self.hbox_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox_layout)

    def create_connections(self) -> None:
        """
        Create signal-slot connections for the menu actions.

        This method connects the menu actions to their respective functions for toggling visibility.
        """
        #self.action_display_shapes.triggered.connect(lambda: MenuLogics.toggle_visibility_shapes(self.tree_widget, self.action_display_shapes.isChecked()))
        #self.action_display_shapes.triggered.connect(lambda: self.toggle_shapes_hidden())
        self.action_display_meshes.triggered.connect(lambda: MenuLogics.toggle_visibility_meshes(self.tree_widget, self.action_display_meshes.isChecked()))
        self.action_display_meshes.triggered.connect(lambda: self.toggle_meshes_shown())
        self.action_display_legend.triggered.connect(lambda: MenuLogics.toggle_visibility_legend(self.legend_widget, self.action_display_legend.isChecked()))
        self.action_config.triggered.connect(self.show_config_menu)
        self.action_about.triggered.connect(self.show_about_dialog)
        #self.action_display_non_unique.triggered.connect(lambda: MenuLogics.toggle_visibility_non_unique(self.tree_widget, self.action_display_non_unique.isChecked(), self.is_shapes_hidden, self.is_meshes_shown))
        #self.action_display_non_unique.triggered.connect(lambda: self.toggle_non_unique_shown())

    def toggle_shapes_hidden(self) -> None:
        """
        Toggle the visibility state of shapes.

        This method inverts the current state of shape visibility.
        """
        if self.is_shapes_hidden:
            self.is_shapes_hidden = False
        else:
            self.is_shapes_hidden = True

    def toggle_meshes_shown(self) -> None:
        """
        Toggle the visibility state of meshes.

        This method inverts the current state of mesh visibility.
        """
        if self.is_meshes_shown:
            self.is_meshes_shown = False
        else:
            self.is_meshes_shown = True

    def toggle_non_unique_shown(self) -> None:
        """
        Toggle the visibility state of non unique items.
        """
        if self.non_unique_mod:
            self.non_unique_mod = False
        else:
            self.non_unique_mod = True

    def show_config_menu(self) -> None:
        """
        Show the configuration menu.
        """
        config_dialog = UserSettingsUI()
        config_dialog.restart_application.connect(self.restart_application.emit)
        config_dialog.exec_()

    def show_about_dialog(self) -> None:
        """
        Show the about dialog.
        """
        about_dialog = AboutDialog()
        about_dialog.exec_()
