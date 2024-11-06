try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem


from renameThemAll.constants import OBJ_TYPE_DICT, OPTIONS_A, OPTIONS_B, INC_OPTIONS, INC_NUMBER_OF_DIGITS
from renameThemAll.name_structure_inspector import NameStructureInspector


class RenamerLogics:
    """
    A class containing static methods for renaming logic in a tree widget.

    This class provides functionality to rename items in a QTreeWidget based on
    different criteria such as type, zoning, orientation, alphabetical increment,
    and numerical increment.

    Methods
    -------
    set_name_with_type(tree_widget, type, rename_mode)
        Set names of items in the tree widget with the specified type.
    set_name_with_zoning(tree_widget, zoning, rename_mode)
        Set names of items in the tree widget with the specified zoning.
    set_name_with_orient(tree_widget, orient, rename_mode)
        Set names of items in the tree widget with the specified orientation.
    set_name_with_a_inc(tree_widget, a_inc, rename_mode)
        Set names of items in the tree widget with the specified alphabetical increment.
    set_name_with_n_inc(tree_widget, n_inc, rename_mode)
        Set names of items in the tree widget with the specified numerical increment.
    set_name_with_short_name(tree_widget, short_name)
        Set names of items in the tree widget with the specified short name.
    get_items_recursive(item, items)
        Recursively get all child items of a given item.
    rename_with_type(tree_widget, item, type)
        Rename a single item in the tree widget with a type.
    rename_with_zoning(tree_widget, item, zoning)
        Rename a single item in the tree widget with a zoning.
    rename_with_orient(tree_widget, item, orient)
        Rename a single item in the tree widget with an orientation.
    rename_with_a_inc(tree_widget, item, a_inc)
        Rename a single item in the tree widget with an alphabetical increment.
    rename_with_n_inc(tree_widget, item, n_inc)
        Rename a single item in the tree widget with a numerical increment.
    rename_with_short_name(tree_widget, item, short_name)
        Rename a single item in the tree widget with a short name.
    get_name_from_item_data(item)
        Extract the name from an item's data.
    """

    @staticmethod
    def set_name_with_type(tree_widget: QTreeWidget, type: str, rename_mode: str) -> None:
        """
        Set names of items in the tree widget with the specified type based on the rename mode.

        This method renames items in the tree widget according to the specified type and rename mode.
        It can operate on selected items, all groups, or all meshes depending on the rename mode.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to be renamed.
        type : str
            The type to be added to the item names.
        rename_mode : str
            The mode of renaming. Can be one of:
            - "selection": Rename only selected items.
            - "all_groups": Rename all group items (transforms).
            - "all_meshes": Rename all mesh items.

        Raises
        ------
        ValueError
            If no items are selected when using "selection" mode, or if no top-level item is found
            when using "all_groups" or "all_meshes" modes.

        Notes
        -----
        The actual renaming is performed by calling the `rename_with_type` method for each
        applicable item.

        The method uses the `OPTIONS_A` and `OBJ_TYPE_DICT` constants for mode and object type
        comparisons, respectively.
        """
        if rename_mode == OPTIONS_A.get("selection"):
            items = tree_widget.selectedItems()
            if not items:
                raise ValueError("No items selected")
            for item in items:
                RenamerLogics.rename_with_type(tree_widget, item, type)

        elif rename_mode == OPTIONS_A.get("all_groups"):
            top_level_item = tree_widget.topLevelItem(0)
            if not top_level_item:
                raise ValueError("No top level item found")
            items = []
            child_count = top_level_item.childCount()
            for i in range(child_count):
                child = top_level_item.child(i)
                RenamerLogics.get_items_recursive(child, items)
            for item in items:
                if item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT.get("transform"):
                    RenamerLogics.rename_with_type(tree_widget, item, type)

        elif rename_mode == OPTIONS_A.get("all_meshes"):
            top_level_item = tree_widget.topLevelItem(0)
            if not top_level_item:
                raise ValueError("No top level item found")
            items = []
            child_count = top_level_item.childCount()
            for i in range(child_count):
                child = top_level_item.child(i)
                RenamerLogics.get_items_recursive(child, items)
            for item in items:
                if item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT.get("transfo_mesh"):
                    RenamerLogics.rename_with_type(tree_widget, item, type)

    @staticmethod
    def set_name_with_zoning(tree_widget: QTreeWidget, zoning: str, rename_mode: str) -> None:
        """
        Set names of items in the tree widget with the specified zoning based on the rename mode.

        This method applies zoning to the names of selected items or selected items and their children,
        depending on the rename mode.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to be renamed.
        zoning : str
            The zoning string to be applied to the item names.
        rename_mode : str
            The mode of renaming. Can be either "selection" (rename only selected items) or
            "select_and_child" (rename selected items and their children).

        Raises
        ------
        ValueError
            If no items are selected in the tree widget.

        Notes
        -----
        - Only non-mesh items (i.e., items that are not of type "mesh" in OBJ_TYPE_DICT) are renamed.
        - The actual renaming is performed by calling the `rename_with_zoning` method for each applicable item.
        - When using "select_and_child" mode, the method recursively processes all children of selected items.
        """
        if rename_mode == OPTIONS_B.get("selection"):
            items = tree_widget.selectedItems()
            if not items:
                raise ValueError("No items selected")
            for item in items:
                if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                    RenamerLogics.rename_with_zoning(tree_widget, item, zoning)

        elif rename_mode == OPTIONS_B.get("select_and_child"):
            selected_items = tree_widget.selectedItems()
            if not selected_items:
                raise ValueError("No items selected")
            items = []
            for item in selected_items:
                items.append(item)
            for selected_item in selected_items:
                child_count = selected_item.childCount()
                for i in range(child_count):
                    child = selected_item.child(i)
                    RenamerLogics.get_items_recursive(child, items)
            for item in items:
                if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                    RenamerLogics.rename_with_zoning(tree_widget, item, zoning)

    @staticmethod
    def set_name_with_orient(tree_widget: QTreeWidget, orient: str, rename_mode: str) -> None:
        """
        Set names of items in the tree widget with the specified orientation based on the rename mode.

        This method applies orientation to the names of selected items or selected items and their children,
        depending on the rename mode.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to be renamed.
        orient : str
            The orientation string to be applied to the item names.
        rename_mode : str
            The mode of renaming. Can be either "selection" (rename only selected items) or
            "select_and_child" (rename selected items and their children).

        Raises
        ------
        ValueError
            If no items are selected in the tree widget.

        Notes
        -----
        - Only non-mesh items (i.e., items that are not of type "mesh" in OBJ_TYPE_DICT) are renamed.
        - The actual renaming is performed by calling the `rename_with_orient` method for each applicable item.
        - When using "select_and_child" mode, the method recursively processes all children of selected items.
        """
        if rename_mode == OPTIONS_B.get("selection"):
            items = tree_widget.selectedItems()
            if not items:
                raise ValueError("No items selected")
            for item in items:
                if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                    RenamerLogics.rename_with_orient(tree_widget, item, orient)

        elif rename_mode == OPTIONS_B.get("select_and_child"):
            selected_items = tree_widget.selectedItems()
            if not selected_items:
                raise ValueError("No items selected")
            items = []
            for item in selected_items:
                items.append(item)
            for selected_item in selected_items:
                child_count = selected_item.childCount()
                for i in range(child_count):
                    child = selected_item.child(i)
                    RenamerLogics.get_items_recursive(child, items)
            for item in items:
                if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                    RenamerLogics.rename_with_orient(tree_widget, item, orient)

    @staticmethod
    def set_name_with_symmetry(tree_widget: QTreeWidget, symmetry: str, rename_mode: str) -> None:
        """
        Set names of items in the tree widget with the specified symmetry based on the rename mode.
        """
        if rename_mode == OPTIONS_B.get("selection"):
            items = tree_widget.selectedItems()
            if not items:
                raise ValueError("No items selected")
            for item in items:
                if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                    RenamerLogics.rename_with_symmetry(tree_widget, item, symmetry)
        elif rename_mode == OPTIONS_B.get("select_and_child"):
            selected_items = tree_widget.selectedItems()
            if not selected_items:
                raise ValueError("No items selected")
            items = []
            for item in selected_items:
                items.append(item)
            for selected_item in selected_items:
                child_count = selected_item.childCount()
                for i in range(child_count):
                    child = selected_item.child(i)
                    RenamerLogics.get_items_recursive(child, items)
            for item in items:
                if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                    RenamerLogics.rename_with_symmetry(tree_widget, item, symmetry)

    @staticmethod
    def set_name_with_inc(tree_widget: QTreeWidget, a_inc: str, n_inc: str, rename_mode: str, inc_option: str) -> None:
        """
        Set names of items in the tree widget with the specified increment based on the rename mode.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to be renamed.
        a_inc : str
            The alphabetical increment to set.
        n_inc : str
            The numerical increment to set.
        rename_mode : str
            The mode of renaming. Can be either "selection" or "select_and_child".
        inc_option : str
            The increment option. Can be "A_TO_Z", "LETTERS", "ZERO_TO_999", or "NUMBERS".

        Notes
        -----
        This method delegates the renaming process to either `set_name_with_a_inc` or 
        `set_name_with_n_inc` based on the `inc_option`.
        """
        if inc_option in [INC_OPTIONS.get("A_TO_Z"), INC_OPTIONS.get("LETTERS")]:
            RenamerLogics.set_name_with_a_inc(tree_widget, a_inc, rename_mode, inc_option)
        elif inc_option in [INC_OPTIONS.get("ZERO_TO_999"), INC_OPTIONS.get("NUMBERS")]:
            RenamerLogics.set_name_with_n_inc(tree_widget, n_inc, rename_mode, inc_option)

    @staticmethod
    def set_name_with_a_inc(tree_widget: QTreeWidget, a_inc: str, rename_mode: str, inc_option: str) -> None:
        """
        Set names of items in the tree widget with the specified alphabetical increment based on the rename mode.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to be renamed.
        a_inc : str
            The alphabetical increment to set. If "A_TO_Z", it will increment from A to Z.
        rename_mode : str
            The mode of renaming. Can be either "selection" or "select_and_child".
        inc_option : str
            The increment option. Can be "A_TO_Z" or "LETTERS".

        Raises
        ------
        ValueError
            If no items are selected in the tree widget.

        Notes
        -----
        This method handles two rename modes:
        - "selection": Only renames selected items.
        - "select_and_child": Renames selected items and all their children recursively.

        For "A_TO_Z" increment, each top-level selection starts from 'A' and increments for its children.
        For "LETTERS" increment, the specified letter is used for all items.
        """
        if a_inc == "" and inc_option == INC_OPTIONS.get("A_TO_Z"):
            inc_option = INC_OPTIONS.get("LETTERS")
        if rename_mode == OPTIONS_B.get("selection"):
            items = tree_widget.selectedItems()
            if not items:
                raise ValueError("No items selected")
            if inc_option == INC_OPTIONS.get("A_TO_Z"):
                letter = "A"
                for item in items:
                    if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                        RenamerLogics.rename_with_a_inc(tree_widget, item, letter)
                        letter = chr(ord(letter) + 1)
            else:
                for item in items:
                    if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                        RenamerLogics.rename_with_a_inc(tree_widget, item, a_inc)

        elif rename_mode == OPTIONS_B.get("select_and_child"):
            selected_items = tree_widget.selectedItems()
            if not selected_items:
                raise ValueError("No items selected")
            items = []
            for item in selected_items:
                items.append(item)

            if inc_option == INC_OPTIONS.get("A_TO_Z"):
                letter = "A"
                for selected_item in selected_items:
                    items_to_rename = []
                    items_to_rename.append(selected_item)
                    child_count = selected_item.childCount()
                    for i in range(child_count):
                        child = selected_item.child(i)
                        RenamerLogics.get_items_recursive(child, items_to_rename)
                    for item in items_to_rename:
                        if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                            RenamerLogics.rename_with_a_inc(tree_widget, item, letter)
                    letter = chr(ord(letter) + 1)
            else:
                for selected_item in selected_items:
                    child_count = selected_item.childCount()
                    for i in range(child_count):
                        child = selected_item.child(i)
                        RenamerLogics.get_items_recursive(child, items)
                for item in items:
                    if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                        RenamerLogics.rename_with_a_inc(tree_widget, item, a_inc)

    @staticmethod
    def set_name_with_n_inc(tree_widget: QTreeWidget, n_inc: str, rename_mode: str, inc_option: str) -> None:
        """
        Set names of items in the tree widget with the specified numerical increment based on the rename mode.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to be renamed.
        n_inc : str
            The numerical increment to set.
        rename_mode : str
            The mode of renaming. Can be either "selection" or "select_and_child".
        inc_option : str
            The increment option. Can be "ZERO_TO_999" or "NUMBERS".

        Raises
        ------
        ValueError
            If no items are selected in the tree widget.

        Notes
        -----
        This method handles two rename modes:
        - "selection": Only renames selected items.
        - "select_and_child": Renames selected items and all their children recursively.

        For "ZERO_TO_999" increment, it uses a three-digit format starting from 001.
        For "NUMBERS" increment, it uses the specified numerical increment for all items.
        """
        if n_inc == "" and inc_option == INC_OPTIONS.get("ZERO_TO_999"):
            inc_option = INC_OPTIONS.get("NUMBERS")
        if rename_mode == OPTIONS_B.get("selection"):
            items = tree_widget.selectedItems()
            if not items:
                raise ValueError("No items selected")
            if inc_option == INC_OPTIONS.get("ZERO_TO_999"):
                number = 1
                for item in items:
                    if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                        n_inc = f"{number:0{INC_NUMBER_OF_DIGITS}d}"
                        RenamerLogics.rename_with_n_inc(tree_widget, item, n_inc)
                        number += 1
            else:
                for item in items:
                    if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                        RenamerLogics.rename_with_n_inc(tree_widget, item, n_inc)

        elif rename_mode == OPTIONS_B.get("select_and_child"):
            selected_items = tree_widget.selectedItems()
            if not selected_items:
                raise ValueError("No items selected")
            items = []
            for item in selected_items:
                items.append(item)

            if inc_option == INC_OPTIONS.get("ZERO_TO_999"):
                number = 1
                for selected_item in selected_items:
                    items_to_rename = []
                    items_to_rename.append(selected_item)
                    child_count = selected_item.childCount()
                    for i in range(child_count):
                        child = selected_item.child(i)
                        RenamerLogics.get_items_recursive(child, items_to_rename)
                    for item in items_to_rename:
                        if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                            n_inc = f"{number:0{INC_NUMBER_OF_DIGITS}d}"
                            RenamerLogics.rename_with_n_inc(tree_widget, item, n_inc)
                    number += 1
            else:
                for selected_item in selected_items:
                    child_count = selected_item.childCount()
                    for i in range(child_count):
                        child = selected_item.child(i)
                        RenamerLogics.get_items_recursive(child, items)
                for item in items:
                    if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                        RenamerLogics.rename_with_n_inc(tree_widget, item, n_inc)

    @staticmethod
    def set_name_with_short_name(tree_widget: QTreeWidget, short_name: str) -> None:
        """
        Set names of selected items in the tree widget with the specified short name.

        This method renames the selected items in the tree widget, excluding mesh objects,
        by applying the provided short name.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to be renamed.
        short_name : str
            The short name to be applied to the selected items.

        Raises
        ------
        ValueError
            If no items are selected in the tree widget.

        Notes
        -----
        This method only affects non-mesh objects among the selected items.
        The renaming is performed using the `rename_with_short_name` method.

        See Also
        --------
        RenamerLogics.rename_with_short_name : Method used for renaming individual items.
        """
        items = tree_widget.selectedItems()
        if not items:
            raise ValueError("No items selected")
        for item in items:
            if item.data(0, Qt.UserRole)[1] != OBJ_TYPE_DICT.get("mesh"):
                RenamerLogics.rename_with_short_name(tree_widget, item, short_name)

    @staticmethod
    def get_items_recursive(item: QTreeWidgetItem, items: list) -> None:
        """
        Recursively get all child items of a given item and add them to a list.

        This method traverses the tree structure starting from the given item,
        adding each item (including the initial item) to the provided list.
        It recursively processes all child items at each level of the tree.

        Parameters
        ----------
        item : QTreeWidgetItem
            The starting item from which to begin the recursive traversal.
        items : list
            The list to which all items (parent and children) will be appended.

        Returns
        -------
        None

        Notes
        -----
        This method modifies the input `items` list in-place by appending
        all encountered items during the traversal.

        The order of items in the resulting list will be depth-first,
        with parent items appearing before their children.
        """
        items.append(item)
        child_count = item.childCount()
        for i in range(child_count):
            child = item.child(i)
            RenamerLogics.get_items_recursive(child, items)

    @staticmethod
    def rename_with_type(tree_widget: QTreeWidget, item: QTreeWidgetItem, type: str) -> None:
        """
        Rename a single item in the tree widget with a type.

        This method adds or modifies the type of the given item's name in the tree widget.
        It reconstructs the name by combining the new type with existing name components.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the item to be renamed.
        item : QTreeWidgetItem
            The specific item in the tree widget to be renamed.
        type : str
            The type to be added or modified in the item's name.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the item's name is empty.

        Notes
        -----
        The method uses `NameStructureInspector.inspect_name_structure` to analyze the current name structure
        and rebuilds the name with the new type while preserving other name components.

        The final name structure follows the pattern:
        [type]_[name][zoning][orientation][alphabetical_inc]_[numerical_inc]

        See Also
        --------
        NameStructureInspector.inspect_name_structure : Method used to analyze the name structure.
        """
        name = RenamerLogics.get_name_from_item_data(item)
        if not name:
            raise ValueError("Item name is empty")
        name_part_dict = NameStructureInspector.inspect_name_structure(name)
        for index in name_part_dict:
            if "type" in name_part_dict[index]:
                name_part_dict[index]["type"] = type
        rebuilt_name = NameStructureInspector.rebuilt_name(name_part_dict)
        tree_widget.start_editing_by_renamer(item, rebuilt_name)

    @staticmethod
    def rename_with_zoning(tree_widget: QTreeWidget, item: QTreeWidgetItem, zoning: str) -> None:
        """
        Rename a single item in the tree widget with a zoning.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the item.
        item : QTreeWidgetItem
            The item to rename.
        zoning : str
            The zoning to add to the item's name.

        Raises
        ------
        ValueError
            If the item name is empty.
        """
        name = RenamerLogics.get_name_from_item_data(item)
        if not name:
            raise ValueError("Item name is empty")
        name_part_dict = NameStructureInspector.inspect_name_structure(name)
        for index in name_part_dict:
            if "zoning" in name_part_dict[index]:
                name_part_dict[index]["zoning"] = zoning
        rebuilt_name = NameStructureInspector.rebuilt_name(name_part_dict)
        tree_widget.start_editing_by_renamer(item, rebuilt_name)

    @staticmethod
    def rename_with_orient(tree_widget: QTreeWidget, item: QTreeWidgetItem, orient: str) -> None:
        """
        Rename a single item in the tree widget with an orientation.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the item.
        item : QTreeWidgetItem
            The item to rename.
        orient : str
            The orientation to add to the item's name.

        Raises
        ------
        ValueError
            If the item name is empty.
        """
        name = RenamerLogics.get_name_from_item_data(item)
        if not name:
            raise ValueError("Item name is empty")
        name_part_dict = NameStructureInspector.inspect_name_structure(name)
        for index in name_part_dict:
            if "orientation" in name_part_dict[index]:
                name_part_dict[index]["orientation"] = orient
        rebuilt_name = NameStructureInspector.rebuilt_name(name_part_dict)
        tree_widget.start_editing_by_renamer(item, rebuilt_name)

    @staticmethod
    def rename_with_a_inc(tree_widget: QTreeWidget, item: QTreeWidgetItem, a_inc: str) -> None:
        """
        Rename a single item in the tree widget with an alphabetical increment.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the item.
        item : QTreeWidgetItem
            The item to rename.
        a_inc : str
            The alphabetical increment to add to the item's name.

        Raises
        ------
        ValueError
            If the item name is empty.
        """
        name = RenamerLogics.get_name_from_item_data(item)
        if not name:
            raise ValueError("Item name is empty")
        name_part_dict = NameStructureInspector.inspect_name_structure(name)
        for index in name_part_dict:
            if "alphabetical_inc" in name_part_dict[index]:
                name_part_dict[index]["alphabetical_inc"] = a_inc
        rebuilt_name = NameStructureInspector.rebuilt_name(name_part_dict)
        tree_widget.start_editing_by_renamer(item, rebuilt_name)

    @staticmethod
    def rename_with_n_inc(tree_widget: QTreeWidget, item: QTreeWidgetItem, n_inc: str) -> None:
        """
        Rename a single item in the tree widget with a numerical increment.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the item.
        item : QTreeWidgetItem
            The item to rename.
        n_inc : str
            The numerical increment to add to the item's name.

        Raises
        ------
        ValueError
            If the item name is empty.
        """
        name = RenamerLogics.get_name_from_item_data(item)
        if not name:
            raise ValueError("Item name is empty")
        name_part_dict = NameStructureInspector.inspect_name_structure(name)
        for index in name_part_dict:
            if "numerical_inc" in name_part_dict[index]:
                name_part_dict[index]["numerical_inc"] = n_inc
        rebuilt_name = NameStructureInspector.rebuilt_name(name_part_dict)
        tree_widget.start_editing_by_renamer(item, rebuilt_name)

    @staticmethod
    def rename_with_symmetry(tree_widget: QTreeWidget, item: QTreeWidgetItem, symmetry: str) -> None:
        """
        Rename a single item in the tree widget with a symmetry.
        """
        name = RenamerLogics.get_name_from_item_data(item)
        if not name:
            raise ValueError("Item name is empty")
        name_part_dict = NameStructureInspector.inspect_name_structure(name)
        for index in name_part_dict:
            if "symmetry" in name_part_dict[index]:
                name_part_dict[index]["symmetry"] = symmetry
        rebuilt_name = NameStructureInspector.rebuilt_name(name_part_dict)
        tree_widget.start_editing_by_renamer(item, rebuilt_name)

    @staticmethod
    def rename_with_short_name(tree_widget: QTreeWidget, item: QTreeWidgetItem, short_name: str) -> None:
        """
        Rename a single item in the tree widget with a short name.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the item.
        item : QTreeWidgetItem
            The item to rename.
        short_name : str
            The short name to set for the item.

        Raises
        ------
        ValueError
            If the item name is empty.
        """
        name = RenamerLogics.get_name_from_item_data(item)
        if not name:
            raise ValueError("Item name is empty")
        name_part_dict = NameStructureInspector.inspect_name_structure(name)
        for index in name_part_dict:
            if "name" in name_part_dict[index]:
                name_part_dict[index]["name"] = short_name
        rebuilt_name = NameStructureInspector.rebuilt_name(name_part_dict)
        tree_widget.start_editing_by_renamer(item, rebuilt_name)

    @staticmethod
    def get_name_from_item_data(item: QTreeWidgetItem) -> str:
        """
        Extract the name from an item's data.

        Parameters
        ----------
        item : QTreeWidgetItem
            The item whose name is to be extracted.

        Returns
        -------
        str
            The extracted name.

        Raises
        ------
        ValueError
            If the item data is empty.
        """
        long_name = item.data(0, Qt.UserRole)[0]
        if not long_name:
            raise ValueError("Item data is empty")
        if "|" in long_name:
            name = long_name.split("|")[-1]
        else:
            name = long_name
        return name
