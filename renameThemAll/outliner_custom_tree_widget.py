import maya.cmds as mc

try:
    from PySide6.QtCore import Qt, QItemSelection
    from PySide6.QtWidgets import QTreeWidget, QWidget, QAbstractItemView, QTreeWidgetItem, QLineEdit,QTreeWidgetItemIterator, QComboBox
    from PySide6.QtGui import QMouseEvent
except ImportError:
    from PySide2.QtCore import Qt, QItemSelection
    from PySide2.QtWidgets import QTreeWidget, QWidget, QAbstractItemView, QTreeWidgetItem, QLineEdit,QTreeWidgetItemIterator, QComboBox
    from PySide2.QtGui import QMouseEvent


from renameThemAll.outliner_logics import OutlinerLogics
from renameThemAll.outliner_text_colored import OutlinerTextColored
from renameThemAll.name_structure_inspector import NameStructureInspector

class OutlinerCustomTreeWidget(QTreeWidget):
    """
    A custom tree widget for the outliner.

    This class extends QTreeWidget to provide custom functionality for the outliner,
    including custom mouse events and item editing.

    Attributes
    ----------
    lexicon_ui : object
        The lexicon UI object associated with this widget.

    Methods
    -------
    mouseDoubleClickEvent(event)
        Handle double-click events on tree items.
    on_item_double_clicked(item)
        Start editing when an item is double-clicked.
    mousePressEvent(event)
        Handle mouse press events, including custom expand/collapse functionality.
    selectionChanged(selected, deselected)
        Handle changes in item selection.
    update_ancestor_highlight()
        Update the highlight of ancestor items for selected items.
    reset_all_items_highlight()
        Reset the highlight of all items in the tree.
    highlight_ancestors(item)
        Highlight the ancestors of a given item.
    get_item_at_click(event)
        Get the item at the position of a mouse click.
    expand_or_collapse(event)
        Expand or collapse an item and its children.
    expand_item(item)
        Recursively expand an item and its children.
    collapse_item(item)
        Recursively collapse an item and its children.
    start_editing_by_lexicon(tree_widget, item)
        Start editing an item programmatically.
    start_editing_by_clicking(item, column)
        Start editing an item when it's clicked.
    start_editing_by_renamer(item, name)
        Start editing an item programmatically.
    finish_editing(item, editor)
        Finish editing an item and update its data.
    edit_shape_name_item(item, shape_name)
        Edit the shape name of an item and update its display.
    """

    def __init__(self, parent: QWidget = None, lexicon_ui = None) -> None:
        """
        Initialize the custom tree widget for the outliner.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget (default is None).
        lexicon_ui : object, optional
            The lexicon UI object associated with this widget (default is None).
        combo_lexicon : QComboBox, optional
            The combo box associated with this outliner UI (default is None).
        """
        super().__init__(parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setMouseTracking(False)  # Désactive le suivi de la souris
        self.lexicon_ui = lexicon_ui

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """
        Handle the mouse double-click event.

        Parameters
        ----------
        event : QMouseEvent
            The mouse event triggered by double-clicking.
        """
        item = self.itemAt(event.pos())
        if item:
            self.on_item_double_clicked(item)

    def on_item_double_clicked(self, item: QTreeWidgetItem) -> None:
        """
        Handle the item double-clicked event.

        Parameters
        ----------
        item : QTreeWidgetItem
            The item that was double-clicked.
        """
        if isinstance(item, QTreeWidgetItem):
            self.start_editing_by_clicking(item, 0)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Override the mouse press event to handle custom expansion/collapse on Ctrl+Shift+Left click.

        Parameters
        ----------
        event : QMouseEvent
            The mouse event triggered by pressing a mouse button.
        """
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            if event.modifiers() == (Qt.ControlModifier | Qt.ShiftModifier):
                self.expand_or_collapse(event)

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        """
        Handle changes in item selection.

        Parameters
        ----------
        selected : QItemSelection
            The newly selected items.
        deselected : QItemSelection
            The newly deselected items.
        """
        super().selectionChanged(selected, deselected)
        self.update_ancestor_highlight()

    def update_ancestor_highlight(self):
        """
        Update the highlight of ancestor items for selected items.
        """
        self.reset_all_items_highlight()
        for item in self.selectedItems():
            self.highlight_ancestors(item)
        self.viewport().update()

    def reset_all_items_highlight(self):
        """
        Reset the highlight of all items in the tree.
        """
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            item = iterator.value()
            item.setData(0, Qt.UserRole + 1, False)
            iterator += 1

    def highlight_ancestors(self, item: QTreeWidgetItem):
        """
        Highlight the ancestors of a given item.

        Parameters
        ----------
        item : QTreeWidgetItem
            The item whose ancestors should be highlighted.
        """
        parent = item.parent()
        while parent:
            parent.setData(0, Qt.UserRole + 1, True)
            parent = parent.parent()
        self.viewport().update()

    def get_item_at_click(self, event: QMouseEvent) -> QTreeWidgetItem:
        """
        Get the item at the position of the mouse click event.

        Parameters
        ----------
        event : QMouseEvent
            The mouse event containing the click position.

        Returns
        -------
        QTreeWidgetItem
            The item at the click position, or None if no item is found.

        Raises
        ------
        RuntimeError
            If failed to get item at click.
        """
        try:
            pos = event.position().toPoint()
            item = self.itemAt(pos)
            return item
        except Exception as e:
            raise RuntimeError(f"Failed to get item at click: {str(e)}")

    def expand_or_collapse(self, event: QMouseEvent) -> None:
        """
        Expand or collapse the item at the click position, including all its children.

        Parameters
        ----------
        event : QMouseEvent
            The mouse event containing the click position.

        Raises
        ------
        RuntimeError
            If failed to expand or collapse item.
        """
        try:
            item = self.get_item_at_click(event)
            if item:
                if not item.isExpanded():
                    self.collapse_item(item)
                    item.setExpanded(False)
                else:
                    self.expand_item(item)
                    item.setExpanded(True)
        except Exception as e:
            raise RuntimeError(f"Failed to expand or collapse item: {str(e)}")

    def expand_item(self, item: QTreeWidgetItem) -> None:
        """
        Recursively expand the given item and all its children.

        Parameters
        ----------
        item : QTreeWidgetItem
            The item to be expanded.

        Raises
        ------
        RuntimeError
            If failed to expand item.
        """
        try:
            if item.childCount() == 1 and item.child(0).isHidden():
                item.setExpanded(False)
            else:
                item.setExpanded(True)
                for i in range(item.childCount()):
                    self.expand_item(item.child(i))
        except Exception as e:
            raise RuntimeError(f"Failed to expand item: {str(e)}")

    def collapse_item(self, item: QTreeWidgetItem) -> None:
        """
        Recursively collapse the given item and all its children.

        Parameters
        ----------
        item : QTreeWidgetItem
            The item to be collapsed.

        Raises
        ------
        RuntimeError
            If failed to collapse item.
        """
        try:
            item.setExpanded(False)
            for i in range(item.childCount()):
                self.collapse_item(item.child(i))
        except Exception as e:
            raise RuntimeError(f"Failed to collapse item: {str(e)}")

    def start_editing_by_clicking(self, item: QTreeWidgetItem, column: int) -> None:
        """
        Start editing the item by clicking.

        Parameters
        ----------
        item : QTreeWidgetItem
            The item to be edited.
        column : int
            The column of the item to be edited.

        Raises
        ------
        RuntimeError
            If failed to start editing by clicking.
        """
        if column == 0:
            obj_type = item.data(0, Qt.UserRole)[1]
            if obj_type == "reference":
                pass
            else:
                try:
                    rect = self.visualItemRect(item)
                    editor = QLineEdit(self.viewport())
                    long_name = item.data(0, Qt.UserRole)[0]
                    raw_text = long_name.split("|")[-1]
                    editor.setText(raw_text)
                    editor.setGeometry(rect)
                    editor.setFocus()
                    editor.selectAll()
                    editor.editingFinished.connect(lambda: self.finish_editing(item, editor, True))
                    editor.show()
                except Exception as e:
                    raise RuntimeError(f"Failed to start editing by clicking: {str(e)}")

    def start_editing_by_renamer(self, item: QTreeWidgetItem, name: str) -> None:
        """
        Start editing the text of the widget programmatically.

        Parameters
        ----------
        item : QTreeWidgetItem
            The tree widget item associated with this widget.
        name : str
            The name to set in the text field.

        Raises
        ------
        RuntimeError
            If failed to start editing by renamer.
        """
        try:
            obj_type = item.data(0, Qt.UserRole)[1]
            if obj_type == "reference":
                pass
            else:
                rect = self.visualItemRect(item)
                editor = QLineEdit(self.viewport())
                editor.setText(name)
                editor.setGeometry(rect)
                editor.setFocus()
                editor.selectAll()
                editor.textChanged.connect(lambda: self.finish_editing(item, editor, True))
                editor.textChanged.emit(editor.text())
                editor.show()
        except Exception as e:
            raise RuntimeError(f"Failed to start editing by renamer: {str(e)}")

    @staticmethod
    def start_editing_by_lexicon(tree_widget: QTreeWidget, item: QTreeWidgetItem) -> None:
        """
        Start editing the text of the widget programmatically.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget associated with this widget.
        item : QTreeWidgetItem
            The tree widget item associated with this widget.

        Raises
        ------
        RuntimeError
            If failed to start editing by lexicon.
        """
        obj_type = item.data(0, Qt.UserRole)[1]
        if obj_type == "reference":
            pass
        else:
            rect = tree_widget.visualItemRect(item)
            editor = QLineEdit(tree_widget.viewport())
            name = item.data(0, Qt.UserRole)[0].split("|")[-1]
            editor.setText(name)
            editor.setGeometry(rect)
            editor.setFocus()
            editor.selectAll()
            editor.textChanged.connect(lambda: tree_widget.finish_editing(item, editor, False))
            editor.textChanged.emit(editor.text())
            editor.show()

    def finish_editing(self, item: QTreeWidgetItem, editor: QLineEdit, check_unique: bool) -> None:
        """
        Finish editing the item and update its data.

        This method completes the editing process for a tree widget item, updating its name
        and associated data. It handles name uniqueness checks, applies color formatting,
        and updates the item's display in the tree widget.

        Parameters
        ----------
        item : QTreeWidgetItem
            The item being edited.
        editor : QLineEdit
            The editor widget used for editing the item's name.
        check_unique : bool
            Flag to determine if the new name should be checked for uniqueness.

        Raises
        ------
        RuntimeError
            If the editing process fails for any reason.

        Notes
        -----
        This method performs the following steps:
        1. Retrieves the new name from the editor.
        2. Checks for name uniqueness if required.
        3. Applies color formatting to the new name.
        4. Updates the item's data and display text.
        5. Refreshes the viewport to reflect changes.
        6. Cleans up the editor widget.
        """
        try:
            new_name = editor.text()
            name_part_dict = None
            if check_unique:
                old_long_name = item.data(0, Qt.UserRole)[0]
                before, sep, after = old_long_name.rpartition('|')
                new_long_name = f"{before}{sep}{new_name}"
                if mc.objExists(new_long_name) and old_long_name != new_long_name:
                    name_part_dict = NameStructureInspector.inspect_name_structure(new_name)   
                    new_name, name_part_dict = OutlinerLogics.rename_non_unique_name(new_long_name, name_part_dict)
            if not name_part_dict:
                name_part_dict = NameStructureInspector.inspect_name_structure(new_name)
            obj_data = item.data(0, Qt.UserRole)
            lexicon_name = self.lexicon_ui.get_current_lexicon()
            colored_text = OutlinerTextColored.set_colored_text(obj_data, name_part_dict, lexicon_name)
            new_long_name = OutlinerLogics.set_new_long_name(item, new_name)

            item.setData(0, Qt.UserRole, [new_long_name, item.data(0, Qt.UserRole)[1]])
            item.setText(0, colored_text)
            self.viewport().update(self.visualItemRect(item))
            editor.deleteLater()
        except Exception as e:
            raise RuntimeError(f"Failed to finish editing: {str(e)}")

    def edit_shape_name_item(self, item: QTreeWidgetItem, shape_name: str) -> None:
        """
        Edit the shape name item and update its display.

        Parameters
        ----------
        item : QTreeWidgetItem
            The tree widget item associated with this widget.
        shape_name : str
            The new shape name to set.

        Raises
        ------
        RuntimeError
            If failed to edit shape name item.
        """
        try:
            name_part_dict = NameStructureInspector.inspect_name_structure(shape_name)
            obj_data = item.data(0, Qt.UserRole)
            if obj_data is None:
                obj_data = (None, None)
            txt_colored = OutlinerTextColored.set_colored_text(obj_data, name_part_dict)
            item.setText(0, txt_colored)
            self.viewport().update(self.visualItemRect(item))
        except Exception as e:
            raise RuntimeError(f"Failed to edit shape name item: {str(e)}")

