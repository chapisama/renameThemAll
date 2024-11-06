import maya.cmds as mc

try:
    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItemIterator, QTreeWidgetItem, QWidget
    from PySide6.QtCore import Qt   
except ImportError:
    from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItemIterator, QTreeWidgetItem, QWidget
    from PySide2.QtCore import Qt   
    
from renameThemAll.constants import OBJ_TYPE_DICT, MAIN_GROUP_DICT

class MenuLogics:
    """
    A class containing static methods for handling menu-related logic in a tree widget.

    This class provides methods for toggling visibility of shapes and meshes,
    as well as managing the visibility of a legend widget.
    """
    @staticmethod
    def toggle_visibility_shapes(tree_widget: QTreeWidget, is_hidden: bool) -> None:
        """
        Toggle the visibility of shape items in the tree widget.

        This method checks if the item type corresponds to 'mesh' in OBJ_TYPE_DICT,
        and hides or shows it in the tree widget accordingly.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to toggle.
        is_hidden : bool
            Whether the shapes should be hidden or shown.

        Raises
        ------
        RuntimeError
            If toggling the visibility of an item fails.
        """
        items = MenuLogics.get_items(tree_widget)
                
        for item in items:
            try:
                if not is_hidden and item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT["mesh"]:
                    parent = item.parent()
                    if parent:
                        item.setHidden(False)   
                elif is_hidden and item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT["mesh"]:
                    parent = item.parent()
                    if parent:
                        if parent.isExpanded():
                            parent.setExpanded(False)
                        item.setHidden(True)
                        
            except RuntimeError as e:
                raise RuntimeError(f"Failed to toggle item visibility: {str(e)}")
    
    @staticmethod
    def toggle_visibility_meshes(tree_widget: QTreeWidget, is_visible: bool) -> None:
        """
        Toggle the visibility of mesh items in the tree widget.

        This method checks if the item type corresponds to 'transfo_mesh' in OBJ_TYPE_DICT,
        and shows or hides it in the tree widget accordingly.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to toggle.
        is_visible : bool
            Whether the meshes should be visible or hidden.

        Raises
        ------
        RuntimeError
            If toggling the visibility of an item fails.
        """
        items = MenuLogics.get_items(tree_widget)
        
        for item in items:
            try:
                if is_visible and item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT["transfo_mesh"]:
                    item.setHidden(False)
                elif not is_visible and item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT["transfo_mesh"]:
                    item.setHidden(True)
            except RuntimeError as e:
                raise RuntimeError(f"Failed to toggle item visibility: {str(e)}")
            
    @staticmethod
    def toggle_visibility_legend(legend_widget: QWidget, is_visible: bool) -> None:
        """
        Toggle the visibility of the legend widget.

        Parameters
        ----------
        legend_widget : QWidget
            The legend widget to show or hide.
        is_hidden : bool
            Whether the legend should be hidden or shown.
        """
        if is_visible:
            legend_widget.show()
        else:
            legend_widget.hide()

    @staticmethod
    def toggle_visibility_non_unique(tree_widget: QTreeWidget, non_unique_mod: bool, shape_hidden: bool, mesh_visible: bool) -> None:
        """
        Toggle visibility of objects with non-unique short names in the tree widget.

        This method traverses all child elements of the main group and checks if their short names
        are unique. It then shows or hides the items accordingly based on the non_unique_mod flag.
        When non_unique_mod is False, it applies visibility based on shape_hidden and mesh_visible flags.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to check and modify.
        non_unique_mod : bool
            Flag indicating whether to show only non-unique items (True) or apply normal visibility rules (False).
        shape_hidden : bool
            Flag indicating whether shapes should be hidden when non_unique_mod is False.
        mesh_visible : bool
            Flag indicating whether meshes should be visible when non_unique_mod is False.

        Returns
        -------
        None

        Notes
        -----
        This method uses the OutlinerLogics and MenuLogics classes, as well as Maya commands (mc)
        to retrieve and process object information.
        """

        if non_unique_mod:
            master_grp = MAIN_GROUP_DICT
            all_objects = mc.listRelatives(master_grp, allDescendents=True, fullPath=True) or []
            short_names = [obj.split('|')[-1] for obj in all_objects]
            unique_short_names = set([name for name in short_names if short_names.count(name) == 1])

            items = MenuLogics.get_items(tree_widget)
            for item in items:
                full_name = item.data(0, Qt.UserRole)[0]
                short_name = full_name.split('|')[-1]
                if short_name not in unique_short_names:
                    if item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT["mesh"]:
                        if not shape_hidden:
                            item.setHidden(False)
                            parent = item.parent()
                            while parent:    
                                parent.setHidden(False)
                                parent.setExpanded(True)
                                parent = parent.parent()
                    else:
                        item.setHidden(False)
                        if item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT["transfo_mesh"]:
                            if not shape_hidden:
                                item.setExpanded(False)
                            else:
                                item.setExpanded(True)
                        else:
                            item.setExpanded(True)
                        parent = item.parent()
                        while parent:
                            parent.setHidden(False)
                            parent.setExpanded(True)
                            parent = parent.parent()
                else:
                    item.setHidden(True)
        else:
            items = MenuLogics.get_items(tree_widget)
            for item in items:
                if item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT["mesh"]:
                    if not shape_hidden:
                        item.setHidden(False)
                elif item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT["transfo_mesh"]:
                    if mesh_visible:
                        item.setHidden(False)
                        item.setExpanded(True)
                else:
                    item.setHidden(False)
    @staticmethod
    def get_items(tree_widget: QTreeWidget) -> list[QTreeWidgetItem]:
        """
        Retrieve all items from the tree widget.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget to retrieve items from.

        Returns
        -------
        list[QTreeWidgetItem]
            A list containing all items in the tree widget.
        """
        items = []
        iterator = QTreeWidgetItemIterator(tree_widget)
        while iterator.value():
            item = iterator.value()
            items.append(item)
            iterator += 1   
        
        return items

