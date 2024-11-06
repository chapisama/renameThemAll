import os
import maya.cmds as mc
from functools import partial
from typing import Optional, Dict

try:
    from PySide6.QtWidgets import QDialog, QAbstractItemView, QPushButton, QHBoxLayout, QVBoxLayout, QTreeWidgetItem, \
        QMessageBox, QWidget, QLabel, QMenu, QTreeWidgetItemIterator, QComboBox, QLineEdit
    from PySide6.QtGui import Qt
    from PySide6.QtCore import QPoint, Signal
except ImportError:
    from PySide2.QtWidgets import QDialog, QAbstractItemView, QPushButton, QHBoxLayout, QVBoxLayout, QTreeWidgetItem, \
        QMessageBox, QWidget, QLabel, QMenu, QTreeWidgetItemIterator, QComboBox, QLineEdit
    from PySide2.QtGui import Qt
    from PySide2.QtCore import QPoint, Signal

from renameThemAll.constants import OBJ_TYPE_DICT, DEFAULT_COLORS, MAIN_GROUP_DICT
from renameThemAll.outliner_custom_delegate import CustomItemDelegate
from renameThemAll.outliner_custom_tree_widget import OutlinerCustomTreeWidget
from renameThemAll.outliner_logics import OutlinerLogics
from renameThemAll.menu_ui import MenuUI

class OutlinerUI(QDialog):
    """
    The OutlinerUI class provides a dialog for displaying and interacting with a hierarchical tree structure.

    This class initializes the outliner dialog, sets up the initial state, creates widgets, and establishes connections.
    It also handles the loading of stylesheets and refreshing of the tree widget.

    Attributes
    ----------
    MIN_WIDTH : int
        Minimum width of the dialog.
    MIN_HEIGHT : int
        Minimum height of the dialog.
    MARGIN : int
        Margin size for layouts.
    tree_widget : OutlinerCustomTreeWidget
        Custom tree widget for displaying the hierarchy.
    colored_delegate : CustomItemDelegate
        Custom delegate for rendering items in the tree widget.
    btn_refresh : QPushButton
        Button to refresh the tree widget.
    """

    MIN_WIDTH = 300
    MIN_HEIGHT = 500
    MARGIN = 2
    restart_application = Signal()

    def __init__(self, lexicon_ui = None, combo_lexicon: QComboBox = None) -> None:
        """
        Initialize the OutlinerUI dialog.

        Parameters
        ----------
        lexicon_ui : LexiconUI, optional
            The LexiconUI instance to be used for lexicon-related operations.       
        combo_lexicon : QComboBox, optional
            The combo box associated with this outliner UI.

        This method sets up the initial state of the outliner, including minimum dimensions, widget creation,
        and icon initialization. It also triggers the creation of UI elements and loads initial data.

        Raises
        ------
        FileNotFoundError
            If the stylesheet file is not found.
        RuntimeError
            If refreshing the tree widget fails.
        """
        super().__init__()
        self.legend_widget = QWidget()
        self.combo_lexicon = combo_lexicon
        self.tree_widget = OutlinerCustomTreeWidget(self, lexicon_ui)
        self.menu_ui = MenuUI(tree_widget=self.tree_widget, legend_widget=self.legend_widget)
        self.menu_ui.restart_application.connect(self.restart_application.emit)
        self.colored_delegate = CustomItemDelegate(view=self.tree_widget, combo_lexicon=self.combo_lexicon)
        self.tree_widget.setItemDelegate(self.colored_delegate)
        self.setMinimumWidth(self.MIN_WIDTH)
        self.setMinimumHeight(self.MIN_HEIGHT)

        self.script_job_number = -1

        self.create_widgets()
        self.create_widget_legend()
        self.create_layout()
        self.create_connections()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.load_stylesheet()
        self.refresh_tree_widget()

    def create_widgets(self) -> None:
        """
        Create and initialize the widgets for the outliner.

        This method configures the tree widget with extended selection mode and a hidden header,
        and creates a refresh button.
        """
        self.entry_custom_name = QLineEdit()
        self.entry_custom_name.setPlaceholderText(MAIN_GROUP_DICT)
        self.tree_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree_widget.setHeaderHidden(True)
        self.btn_refresh = QPushButton("Refresh")

    def create_widget_legend(self) -> None:
        """
        Create a legend widget with colored squares and labels.

        This method initializes a QLabel widget to display colored squares
        representing the colors from the DEFAULT_COLORS dictionary,
        along with corresponding labels.
        """
        layout = QVBoxLayout(self.legend_widget)
        first_line_layout = QHBoxLayout()
        second_line_layout = QHBoxLayout()
        layout.addLayout(first_line_layout)
        layout.addLayout(second_line_layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        for i, (color_name, color_value) in enumerate(DEFAULT_COLORS.items()):
            if i % 2 == 0:
                row_layout = QHBoxLayout()
                first_line_layout.addLayout(row_layout)
            else:
                row_layout = QHBoxLayout()
                second_line_layout.addLayout(row_layout)

            color_square = QLabel()
            color_square.setFixedSize(15, 15)
            color_square.setStyleSheet(f"background-color: {color_value}; border: 1px solid black;")

            label = QLabel(color_name.capitalize().replace("_", " "))

            row_layout.addWidget(color_square)
            row_layout.addWidget(label)
            row_layout.addStretch()

        self.legend_widget.hide()

    def create_layout(self) -> None:
        """
        Create the layout for the outliner dialog.

        This method sets up the main layout, including the tree widget and the refresh button at the bottom.
        """
        custom_name_layout = QHBoxLayout()
        custom_name_layout.addWidget(QLabel("Outline this object:"))
        custom_name_layout.addWidget(self.entry_custom_name)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.btn_refresh)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(self.MARGIN, 0, self.MARGIN, self.MARGIN)
        main_layout.setSpacing(self.MARGIN)
        main_layout.addWidget(self.menu_ui)
        main_layout.addLayout(custom_name_layout)
        main_layout.addWidget(self.tree_widget)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.legend_widget)
        

    def create_connections(self) -> None:
        """
        Create signal-slot connections for the UI elements.

        This method connects various signals from the tree widget and refresh button
        to their corresponding slots.
        """
        self.entry_custom_name.textChanged.connect(self.on_custom_name_changed)
        self.tree_widget.itemCollapsed.connect(self.on_item_collapsed_or_expanded)
        self.tree_widget.itemExpanded.connect(self.on_item_collapsed_or_expanded)
        self.tree_widget.itemClicked.connect(lambda item: OutlinerLogics.select_elements(item))
        self.btn_refresh.clicked.connect(self.refresh_tree_widget)

    def on_item_collapsed_or_expanded(self, item: QTreeWidgetItem) -> None:
        """
        Handle the collapse or expand event of a tree item.

        This method updates the icon of the item when it's collapsed or expanded.

        Parameters
        ----------
        item : QTreeWidgetItem
            The item that was collapsed or expanded.
        """
        index = self.tree_widget.indexFromItem(item)
        self.colored_delegate.get_icon(index)

    def on_custom_name_changed(self, text: str) -> None:
        """
        Handle the change event of the custom name entry.
        """
        if text in mc.ls(assemblies=True):
            self.refresh_tree_widget(text)
        else:
            self.refresh_tree_widget()

    def load_stylesheet(self) -> None:
        """
        Load and apply the CSS stylesheet for the tree widget.

        This method attempts to read the CSS file from the same directory as the script
        and applies it to the tree widget.

        Raises
        ------
        FileNotFoundError
            If the stylesheet file is not found.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        stylesheet_path = os.path.join(current_dir, "outliner_style.css")
        try:
            with open(stylesheet_path, "r") as f:
                self.tree_widget.setStyleSheet(f.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: CSS file not found at location: {stylesheet_path}")

    def refresh_tree_widget(self, custom_name: Optional[str] = None) -> None:
        """
        Refresh the tree widget with the latest scene elements.

        This method clears the current tree, retrieves the latest scene hierarchy,
        and populates the tree with updated data.

        Raises
        ------
        RuntimeError
            If refreshing the tree widget fails.
        """
        self.tree_widget.clear()
        try:
            main_group = MAIN_GROUP_DICT if custom_name is None else custom_name
            if mc.objExists(main_group):
                outliner_elements = OutlinerLogics.dict_outliner_elements(main_group)
                type_dict = {
                "transfo_mesh": OutlinerLogics.get_transfo_mesh(main_group),
                "reference": OutlinerLogics.get_reference_elements(main_group),
                "instance": OutlinerLogics.get_instance_elements(main_group)
            }

                self.add_items(None, outliner_elements, type_dict)

                self.update_selection()
        except RuntimeError as e:
            QMessageBox.critical(self, "Error", f"Refresh failed: {str(e)}")
            return    

    def add_items(self, parent_item: Optional[QTreeWidgetItem], outliner_elements: Dict[str, Dict], type_dict: Dict[str, Dict]) -> None:
        """
        Recursively add items to the tree widget.

        This method creates tree items for each element in the scene hierarchy,
        configures their data and appearance, and recursively adds child items.

        Parameters
        ----------
        parent_item : QTreeWidgetItem or None
            The parent item to add to, or None for top-level items.
        outliner_elements : dict
            A dictionary representing the scene hierarchy, with long names as keys
            and their children as values.
        """
 
        for name, children in outliner_elements.items():
            item = QTreeWidgetItem(parent_item)

            if parent_item is None:
                self.tree_widget.addTopLevelItem(item)
            else:
                parent_item.addChild(item)

            short_name = name.split("|")[-1]
            OutlinerLogics.set_obj_data_type(item, name, type_dict)
            item.setText(0, short_name)
            if item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT["mesh"] and self.menu_ui.is_shapes_hidden:
                item.setHidden(True)
            if item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT["transfo_mesh"] and not self.menu_ui.is_meshes_shown:
                item.setHidden(True)
            if children:
                self.add_items(item, children, type_dict)

    def show_context_menu(self, point: QPoint):
        """
        Display the context menu at the specified point.

        This method creates a context menu with actions for displaying shapes,
        meshes, and the legend, and shows it at the given point.

        Parameters
        ----------
        point : QPoint
            The point where the context menu should be displayed.
        """
        context_menu = QMenu(self)
        #context_menu.addAction(self.menu_ui.action_display_shapes)
        context_menu.addAction(self.menu_ui.action_display_meshes)
        context_menu.addSeparator()
        context_menu.addAction(self.menu_ui.action_display_legend)
        context_menu.exec_(self.tree_widget.mapToGlobal(point))

    def update_selection(self):
        """
        Update the selection in the tree widget based on the current Maya selection.

        This method retrieves the current selection in Maya, clears the current
        tree widget selection, and then selects the corresponding items in the tree widget.
        """
        selection = mc.ls(selection=True, long=True)
        iterator = QTreeWidgetItemIterator(self.tree_widget)
        self.tree_widget.clearSelection() 
        while iterator.value():
            item = iterator.value()
            full_name = item.data(0, Qt.UserRole)[0]
            if full_name in selection:
                item.setSelected(True)
            else:
                item.setSelected(False)  
            iterator += 1

    def set_script_job_enabled(self, enabled: bool):
        """
        Enable or disable the script job for selection changes.

        This method creates or kills a Maya script job that updates the tree widget
        selection when the Maya selection changes.

        Parameters
        ----------
        enabled : bool
            Whether to enable (True) or disable (False) the script job.
        """
        if enabled and self.script_job_number < 0:
            self.script_job_number = mc.scriptJob(event=["SelectionChanged", partial(self.update_selection)], protected=True)
        elif not enabled and self.script_job_number >= 0:
            mc.scriptJob(kill=self.script_job_number, force=True)
            self.script_job_number = -1

    def showEvent(self, event):
        """
        Handle the show event for the dialog.

        This method is called when the dialog is shown. It enables the script job
        for selection changes.

        Parameters
        ----------
        event : QShowEvent
            The show event object.

        Returns
        -------
        None

        Notes
        -----
        This method calls the superclass showEvent method before enabling the script job.
        """
        super().showEvent(event)
        self.set_script_job_enabled(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.tree_widget.setColumnWidth(0, self.tree_widget.viewport().width())

    def cleanup(self):
        """
        Clean up resources used by OutlinerUI.

        This method should be called when closing the main interface. It disables
        the script job for selection changes.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        This method ensures that the script job is properly disabled to prevent
        any potential issues or resource leaks.
        """
        self.set_script_job_enabled(False)
