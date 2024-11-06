try:
    from PySide6.QtCore import Qt, QSize, QRect, QPoint, QModelIndex, QObject
    from PySide6.QtGui import QTextDocument, QIcon, QPainter
    from PySide6.QtWidgets import QStyledItemDelegate, QAbstractItemView, QStyleOptionViewItem, QStyle, QComboBox
except ImportError:
    from PySide2.QtCore import Qt, QSize, QRect, QPoint, QModelIndex, QObject
    from PySide2.QtGui import QTextDocument, QIcon, QPainter
    from PySide2.QtWidgets import QStyledItemDelegate, QAbstractItemView, QStyleOptionViewItem, QStyle, QComboBox

    from renameThemAll.constants import OBJ_TYPE_DICT
    from renameThemAll.outliner_text_colored import OutlinerTextColored
    from renameThemAll.name_structure_inspector import NameStructureInspector


class CustomItemDelegate(QStyledItemDelegate):
    """
    Custom item delegate for rendering and editing items in a QTreeView.

    This delegate handles custom painting, size hinting, and icon retrieval for items in the view.

    Parameters
    ----------
    view : QAbstractItemView
        The view that uses this delegate.
    parent : QObject, optional
        The parent object (default is None).

    Attributes
    ----------
    view : QAbstractItemView
        The view associated with this delegate.
    transform_icon : QIcon
        Icon for transform items.
    mesh_icon : QIcon
        Icon for mesh items.
    reference_icon : QIcon
        Icon for reference items.
    instance_icon : QIcon
        Icon for instance items.
    """

    def __init__(self, view: QAbstractItemView, parent: QObject = None, combo_lexicon: QComboBox = None) -> None:
        super().__init__(parent)
        self.view = view
        self.combo_lexicon = combo_lexicon
        self.transform_icon = QIcon(":transform.svg")
        self.mesh_icon = QIcon(":mesh.svg")
        self.reference_icon = QIcon(":out_reference.png")
        self.instance_icon = QIcon(":channelLayers.png")

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        """
        Paint the item in the view.

        This method handles the custom painting of items, including background, icons, and text.

        Parameters
        ----------
        painter : QPainter
            The painter used to draw the item.
        option : QStyleOptionViewItem
            The style options for the item.
        index : QModelIndex
            The index of the item in the model.
        
        Raises
        ------
        RuntimeError
            If painting the item fails.
        """
        try:
            if option.state & QStyle.State_Selected:
                color = option.palette.highlight().color()
                color.setAlpha(25)  
                painter.fillRect(option.rect, color)
            
            elif index.data(Qt.UserRole + 1): 
                color = option.palette.highlight().color()
                color.setAlpha(25) 
                painter.fillRect(option.rect, color)

            icon = self.get_icon(index)
            if icon:
                icon_size = QSize(16, 16)
                icon_y = option.rect.top() + (option.rect.height() - icon_size.height()) // 2
                icon_rect = QRect(QPoint(option.rect.left(), icon_y), icon_size)
                icon.paint(painter, icon_rect)

            obj_data = index.data(Qt.UserRole)
            if obj_data is None:
                obj_data = (None, None)

            name = obj_data[0].split("|")[-1]
            name_part_dict = NameStructureInspector.inspect_name_structure(name)

            html_text = OutlinerTextColored.set_colored_text(obj_data, name_part_dict, self.combo_lexicon.currentText())

            doc = QTextDocument()
            doc.setHtml(html_text)
            doc.setTextWidth(float('inf')) 

            text_rect = option.rect.adjusted(icon_size.width(), 0, 0, 0)
            
            painter.save()
            painter.translate(text_rect.topLeft())
            painter.setClipRect(text_rect.translated(-text_rect.topLeft()))
            doc.drawContents(painter)
            painter.restore()
        except Exception as e:
            raise RuntimeError(f"Failed to paint item: {str(e)}")

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        """
        Provide the size hint for the item.

        This method calculates the appropriate size for the item based on its content.

        Parameters
        ----------
        option : QStyleOptionViewItem
            The style options for the item.
        index : QModelIndex
            The index of the item in the model.

        Returns
        -------
        QSize
            The size hint for the item.
        
        Raises
        ------
        RuntimeError
            If getting the size hint fails.
        """
        try:
            obj_data = index.data(Qt.UserRole)
            name = obj_data[0].split("|")[-1]
            name_part_dict = NameStructureInspector.inspect_name_structure(name)
            html_text = OutlinerTextColored.set_colored_text(obj_data, name_part_dict, self.combo_lexicon.currentText())
            doc = QTextDocument()
            doc.setHtml(html_text)
            doc.setTextWidth(float('inf'))
            size = QSize(doc.idealWidth() + 20, max(doc.size().height(), 20))
            return size
        except Exception as e:
            raise RuntimeError(f"Failed to get size hint: {str(e)}")

    def get_icon(self, index: QModelIndex) -> QIcon:
        """
        Get the icon for the item.

        This method determines the appropriate icon based on the item's type and state.

        Parameters
        ----------
        index : QModelIndex
            The index of the item in the model.

        Returns
        -------
        QIcon
            The icon for the item.
        
        Raises
        ------
        RuntimeError
            If getting the icon fails.
        """
        try:
            if isinstance(index, QModelIndex):
                obj_type = index.data(Qt.UserRole)
            else:
                obj_type = index.data(0, Qt.UserRole)

            if isinstance(obj_type, (list, tuple)) and len(obj_type) > 1:
                obj_type = obj_type[1]
            icon_map = {
                OBJ_TYPE_DICT.get("reference"): self.reference_icon,
                OBJ_TYPE_DICT.get("instance"): self.instance_icon,
                OBJ_TYPE_DICT.get("transform"): self.transform_icon,
                OBJ_TYPE_DICT.get("mesh"): self.mesh_icon
            }

            is_expanded = index.model().hasChildren(index) and self.view.isExpanded(index)

            if obj_type == OBJ_TYPE_DICT.get("transfo_mesh"):
                return self.mesh_icon if not is_expanded else self.transform_icon
            else:
                return icon_map.get(obj_type, self.transform_icon)
        except Exception as e:
            print(f"Error in get_icon: {str(e)}")
            return QIcon()

    '''def createEditor(self, parent: QObject, option: QStyleOptionViewItem, index: QModelIndex) -> QLineEdit:
        """
        Create an editor for the item.

        This method is currently commented out and not in use.

        Parameters
        ----------
        parent : QObject
            The parent object.
        option : QStyleOptionViewItem
            The style options for the item.
        index : QModelIndex
            The index of the item in the model.

        Returns
        -------
        QLineEdit
            The editor for the item.
        
        Raises
        ------
        RuntimeError
            If creating the editor fails.
        """
        try:
            editor = QLineEdit(parent)
            editor.editingFinished.connect(lambda: self.finish_editing(index))
            editor.installEventFilter(self)
            return editor
        except Exception as e:
            raise RuntimeError(f"Failed to create editor: {str(e)}")

    def setEditorData(self, editor: QLineEdit, index: QModelIndex) -> None:
        """
        Set the data for the editor.

        This method is currently commented out and not in use.

        Parameters
        ----------
        editor : QLineEdit
            The editor for the item.
        index : QModelIndex
            The index of the item in the model.
        
        Raises
        ------
        RuntimeError
            If setting the editor data fails.
        """
        try:
            value = index.data(Qt.EditRole)
            editor.setText(value)
        except Exception as e:
            raise RuntimeError(f"Failed to set editor data: {str(e)}")

    def setModelData(self, editor: QLineEdit, model: QAbstractItemModel, index: QModelIndex) -> None:
        """
        Set the data from the editor to the model.

        This method is currently commented out and not in use.

        Parameters
        ----------
        editor : QLineEdit
            The editor for the item.
        model : QAbstractItemModel
            The model for the item.
        index : QModelIndex
            The index of the item in the model.
        
        Raises
        ------
        RuntimeError
            If setting the model data fails.
        """
        try:
            value = editor.text()
            model.setData(index, value, Qt.EditRole)
        except Exception as e:
            raise RuntimeError(f"Failed to set model data: {str(e)}")

    def edit(self, parent: QObject, option: QStyleOptionViewItem, index: QModelIndex) -> QLineEdit:
        """
        Edit the item.

        This method is currently commented out and not in use.

        Parameters
        ----------
        parent : QObject
            The parent object.
        option : QStyleOptionViewItem
            The style options for the item.
        index : QModelIndex
            The index of the item in the model.

        Returns
        -------
        QLineEdit
            The editor for the item.
        
        Raises
        ------
        RuntimeError
            If editing the item fails.
        """
        try:
            editor = super().edit(parent, option, index)
            if isinstance(editor, QLineEdit):
                editor.selectAll()
            return editor
        except Exception as e:
            raise RuntimeError(f"Failed to edit item: {str(e)}")

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Filter events for the editor.

        This method is currently commented out and not in use.

        Parameters
        ----------
        obj : QObject
            The object receiving the event.
        event : QEvent
            The event to be filtered.

        Returns
        -------
        bool
            True if the event is handled, False otherwise.
        
        Raises
        ------
        RuntimeError
            If filtering the event fails.
        """
        try:
            if isinstance(obj, QLineEdit) and event.type() == QEvent.FocusOut:
                self.finish_editing(self.sender().property("index"))
                return True
            return super().eventFilter(obj, event)
        except Exception as e:
            raise RuntimeError(f"Failed to filter event: {str(e)}")
'''