import maya.cmds as mc

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QTreeWidgetItem
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QTreeWidgetItem

from renameThemAll.constants import OBJ_TYPE_DICT, INC_NUMBER_OF_DIGITS
from renameThemAll.name_structure_inspector import NameStructureInspector


class OutlinerLogics:
    """
    Class managing Outliner logics for Maya.

    This class provides static methods to manipulate and query
    the hierarchical structure of objects in Maya, particularly for
    use in a custom Outliner.

    Main features:
    - Renaming objects and updating hierarchy
    - Identifying object types (mesh, reference, instance)
    - Retrieving information about the scene structure
    - Selecting elements in Maya

    Note: This class is designed to be used with the Maya API and
    requires Maya to be properly initialized.
    """


    @staticmethod
    def dict_outliner_elements(group: str) -> dict:
        """
        Get a dictionary representation of outliner elements starting from the given group.

        This method creates a hierarchical dictionary of all elements in the outliner.

        Parameters
        ----------
        group : str
            The name of the group to start from.
        full_path : bool, optional
            Whether to use full paths for the elements.

        Returns
        -------
        dict
            A dictionary representing the outliner elements hierarchy.

        Raises
        ------
        RuntimeError
            If retrieving outliner elements fails.
        """
        try:
            def add_children_to_dict(parent: str) -> dict:
                children = mc.listRelatives(parent, children=True, fullPath=True) or []
                return {child: add_children_to_dict(child) for child in children}

            return {group: add_children_to_dict(group)}
        except RuntimeError as e:
            raise RuntimeError(f"OutlinerLogics.dict_outliner_elements: Failed to get outliner elements: {str(e)}")

    @staticmethod
    def set_obj_data_type(item: QTreeWidgetItem, name: str, type_dict: dict) -> str:
        """
        Set the object data type for the given item.

        This method determines the object type based on its hierarchy and Maya object type,
        and sets the appropriate data for the tree widget item.

        Parameters
        ----------
        item : QTreeWidgetItem
            The tree widget item.
        name : str
            The name of the object.

        Raises
        ------
        RuntimeError
            If setting the object data type fails.
        """
        try:
            obj_type = None
            if name in type_dict.get("reference"):
                obj_type = OBJ_TYPE_DICT.get("reference")
            elif name in type_dict.get("instance"):
                obj_type = OBJ_TYPE_DICT.get("instance")
            elif name in type_dict.get("transfo_mesh"):
                obj_type = OBJ_TYPE_DICT.get("transfo_mesh")
            else:
                obj_type = mc.objectType(name)

            item.setData(0, Qt.UserRole, [name, obj_type])
        
        except RuntimeError as e:
            raise RuntimeError(f"OutlinerLogics.set_obj_data_type: Failed to set object data type: {str(e)}")

    @staticmethod
    def get_reference_elements(main_group: str) -> list:
        """
        Get all reference elements under the given main group.

        Parameters
        ----------
        main_group : str
            The name of the main group.

        Returns
        -------
        list
            A list of reference elements.

        Raises
        ------
        RuntimeError
            If retrieving reference elements fails.
        """
        try:
            all_nodes = mc.ls(main_group, dag=True, long=True)
            references = [node for node in all_nodes if mc.referenceQuery(node, isNodeReferenced=True)]
            return references
        except RuntimeError as e:
            raise RuntimeError(f"OutlinerLogics.get_reference_elements: Failed to get reference elements: {str(e)}")

    @staticmethod
    def get_instance_elements(main_group: str) -> list:
        """
        Get all instance elements under the given main group.

        This method identifies mesh instances and their ancestors.

        Parameters
        ----------
        main_group : str
            The name of the main group.

        Returns
        -------
        list
            A list of instance elements.

        Raises
        ------
        RuntimeError
            If retrieving instance elements fails.
        """
        try:
            meshes = mc.ls(main_group, dag=True, type="mesh", long=True)
            instances = []
            if meshes:
                for mesh in meshes:
                    parents = mc.ls(mesh, long=True, ap=True)
                    if len(parents) > 1:
                        instances.append(mesh)
                        ancestors = OutlinerLogics.get_instance_ancestors(parents, instances)
                        instances.extend([ancestor for ancestor in ancestors if ancestor not in instances])
                        instances.extend([parent for parent in parents if parent not in instances])
            return instances
        except RuntimeError as e:
            raise RuntimeError(f"OutlinerLogics.get_instance_elements: Failed to get instance elements: {str(e)}")

    @staticmethod
    def get_instance_ancestors(parents: list, instances: list) -> list:
        """
        Get all ancestor nodes of the given parents that are instances.

        This method recursively traverses the hierarchy to find all instance ancestors.

        Parameters
        ----------
        parents : list
            A list of parent nodes.
        instances : list
            A list of known instance nodes.

        Returns
        -------
        list
            A list of ancestor nodes that are instances.

        Raises
        ------
        RuntimeError
            If retrieving instance ancestors fails.
        """
        try:
            all_ancestors = []
            for parent in parents:
                ancestors = mc.ls(parent, long=True, allPaths=True)[0].split('|')[1:-1]
                if ancestors:
                    for ancestor in ancestors:
                        full_path = '|' + '|'.join(ancestors[:ancestors.index(ancestor) + 1])
                        if full_path not in instances and OutlinerLogics.has_non_instance_mesh(full_path):
                            all_ancestors.append(full_path)
                            instances.append(full_path)
                            all_ancestors.extend(OutlinerLogics.get_instance_ancestors([full_path], instances))
            return all_ancestors
        except RuntimeError as e:
            raise RuntimeError(f"OutlinerLogics.get_instance_ancestors: Failed to get instance ancestors: {str(e)}")

    @staticmethod
    def has_non_instance_mesh(node: str) -> bool:
        """
        Check if the node has any non-instance mesh children.

        This method recursively checks the node and its children for non-instance meshes.

        Parameters
        ----------
        node : str
            The node to check.

        Returns
        -------
        bool
            True if the node has non-instance mesh children, False otherwise.

        Raises
        ------
        RuntimeError
            If checking for non-instance mesh fails.
        """
        try:
            children = mc.listRelatives(node, children=True, fullPath=True, type="mesh")
            if children:
                for child in children:
                    parents = mc.listRelatives(child, allParents=True, fullPath=True)
                    if len(parents) == 1:
                        return False
            child_groups = mc.listRelatives(node, children=True, fullPath=True, type="transform")
            if child_groups:
                for child_group in child_groups:
                    if not OutlinerLogics.has_non_instance_mesh(child_group):
                        return False
            return True
        except RuntimeError as e:
            raise RuntimeError(f"OutlinerLogics.has_non_instance_mesh: Failed to check for non-instance mesh: {str(e)}")

    @staticmethod
    def get_transfo_mesh(main_group: str) -> list:
        """
        Get all 'transform mesh' elements under the given main group.

        This method identifies all mesh transforms in the hierarchy.

        Parameters
        ----------
        main_group : str
            The name of the main group.

        Returns
        -------
        list
            A list of transform mesh elements.

        Raises
        ------
        RuntimeError
            If retrieving transform mesh elements fails.
        """
        try:
            meshes = mc.listRelatives(main_group, fullPath=True, allDescendents=True, type="mesh")
            transfo_mesh = []
            if meshes:
                for mesh in meshes:
                    parent = mc.listRelatives(mesh, allParents=True, fullPath=True)
                    transfo_mesh.append(parent[0])
            return transfo_mesh
        except RuntimeError as e:
            raise RuntimeError(f"OutlinerLogics.get_transfo_mesh: Failed to get transform mesh elements: {str(e)}")

    @staticmethod
    def set_new_long_name(item: QTreeWidgetItem, short_name: str) -> str:
        """
        Set a new long name for the item by renaming it in Maya.

        Parameters
        ----------
        item : QTreeWidgetItem
            The tree widget item to rename.
        short_name : str
            The new short name to set.

        Returns
        -------
        str
            The new long name.

        Raises
        ------
        RuntimeError
            If renaming fails in Maya.
        """
        try:
            old_long_name = item.data(0, Qt.UserRole)[0]
            mc.rename(old_long_name, short_name)
            before, sep, after = old_long_name.rpartition('|')
            new_long_name = f"{before}{sep}{short_name}"
            OutlinerLogics.update_children_data(item, old_long_name, new_long_name)

            return new_long_name if sep else short_name
        except RuntimeError as e:
            raise RuntimeError(f"OutlinerLogics.set_new_long_name: Failed to set new long name: {str(e)}")

    @staticmethod
    def update_children_data(item: QTreeWidgetItem, old_long_name: str, new_long_name: str) -> None:
        """
        Update the long name data for the item's children recursively.

        This method traverses the tree structure and updates the data for all child items,
        handling both mesh and non-mesh objects differently.

        Parameters
        ----------
        item : QTreeWidgetItem
            The tree widget item to update.
        old_long_name : str
            The old long name.
        new_long_name : str
            The new long name.

        Raises
        ------
        RuntimeError
            If updating children data fails.
        """
        try:
            child_count = item.childCount()
            for i in range(child_count):
                child = item.child(i)
                old_child_data = child.data(0, Qt.UserRole)[0]
                obj_type = child.data(0, Qt.UserRole)[1]
                if obj_type != OBJ_TYPE_DICT.get("mesh"):
                    OutlinerLogics.update_child_data(child, old_child_data, old_long_name, new_long_name)
                else:
                    old_shape_name = old_child_data.split("|")[-1]
                    parent_name = old_child_data.split("|")[-2]
                    if OutlinerLogics.check_shape_parent_names(parent_name, old_shape_name):
                        tmp_child_data = old_child_data.replace(old_long_name, new_long_name)
                        shape_name = tmp_child_data.split("|")[-2] + "Shape"
                        new_child_data = f"{tmp_child_data.rpartition('|')[0]}|{shape_name}"
                        child.setData(0, Qt.UserRole, [new_child_data, child.data(0, Qt.UserRole)[1]])
                        tree_widget = child.treeWidget()
                        if tree_widget:
                            tree_widget.edit_shape_name_item(child, shape_name)
                        OutlinerLogics.update_children_data(child, old_long_name, new_long_name)
                    else:
                        OutlinerLogics.update_child_data(child, old_child_data, old_long_name, new_long_name)
        except RuntimeError as e:
            raise RuntimeError(f"OutlinerLogics.update_children_data: Failed to update children data: {str(e)}")

    @staticmethod
    def update_child_data(child: QTreeWidgetItem, old_child_data: str, old_long_name: str, new_long_name: str) -> None:
        """
        Update the child data with the new long name.

        This method updates the data for a single child item and recursively updates its children.

        Parameters
        ----------
        child : QTreeWidgetItem
            The child item to update.
        old_child_data : str
            The old child data.
        old_long_name : str
            The old long name.
        new_long_name : str
            The new long name.

        Raises
        ------
        RuntimeError
            If updating child data fails.
        """
        try:
            new_child_data = old_child_data.replace(old_long_name, new_long_name)
            child.setData(0, Qt.UserRole, [new_child_data, child.data(0, Qt.UserRole)[1]])
            OutlinerLogics.update_children_data(child, old_long_name, new_long_name)
        except RuntimeError as e:
            raise RuntimeError(f"OutlinerLogics.update_child_data: Failed to update child data: {str(e)}")

    @staticmethod
    def rename_non_unique_name(long_name: str, name_part_dict: dict, a_inc = "A", n_inc = 1) -> str:
        """
        Generate a unique name by appending increments when the name already exists.

        This method checks if a name exists in Maya and generates a unique version by appending
        either alphabetical or numerical increments based on the name structure. It handles three cases:
        - Names with alphabetical increment slots (e.g. "name_A" -> "name_B")
        - Names with numerical increment slots (e.g. "name_001" -> "name_002") 
        - Names without increment slots (appends numbers at the end)

        Parameters
        ----------
        long_name : str
            The full path name to check for uniqueness
        name_part_dict : dict
            Dictionary containing the structured name parts
        a_inc : str, optional
            Starting letter for alphabetical increment, by default "A"
        n_inc : int, optional
            Starting number for numerical increment, by default 1

        Returns
        -------
        tuple
            A tuple containing:
            - str: The unique short name (without path)
            - dict: Updated name_part_dict with new increment values

        Notes
        -----
        The method will increment either alphabetically or numerically until finding
        a unique name. For numerical increments, it uses the INC_NUMBER_OF_DIGITS constant
        to pad the numbers with leading zeros.
        """
        a_inc_in_dict = False
        n_inc_in_dict = False
        found_index = None
        
        for index in name_part_dict:
            if "alphabetical_inc" in name_part_dict[index]:
                a_inc_in_dict = True
                found_index = index
                break
            if "numerical_inc" in name_part_dict[index]:
                n_inc_in_dict = True
                found_index = index
                break
                
        if a_inc_in_dict:   
            name_part_dict[found_index]["alphabetical_inc"] = a_inc
            before, sep, after = long_name.rpartition("|")
            new_short_name = NameStructureInspector.rebuilt_name(name_part_dict)
            long_name = f"{before}{sep}{new_short_name}"
            while mc.objExists(long_name):
                a_inc = chr(ord(a_inc) + 1)
                name_part_dict[found_index]["alphabetical_inc"] = a_inc
                before, sep, after = long_name.rpartition("|")
                new_short_name = NameStructureInspector.rebuilt_name(name_part_dict)
                long_name = f"{before}{sep}{new_short_name}"
                
            return new_short_name, name_part_dict
                
        if n_inc_in_dict:
            name_part_dict[found_index]["numerical_inc"] = str(f"{n_inc:0{INC_NUMBER_OF_DIGITS}d}")
            before, sep, after = long_name.rpartition("|")
            new_short_name = NameStructureInspector.rebuilt_name(name_part_dict)
            long_name = f"{before}{sep}{new_short_name}"
            while mc.objExists(long_name):
                n_inc += 1
                name_part_dict[found_index]["numerical_inc"] = str(f"{n_inc:0{INC_NUMBER_OF_DIGITS}d}")
                before, sep, after = long_name.rpartition("|")
                new_short_name = NameStructureInspector.rebuilt_name(name_part_dict)
                long_name = f"{before}{sep}{new_short_name}"
                
            return new_short_name, name_part_dict
                
        if long_name[-1].isdigit():
            suffix = int(long_name[-1]) + 1
            long_name = f"{long_name[:-1]}{suffix}"
            while mc.objExists(long_name):
                suffix += 1
                long_name = f"{long_name[:-1]}{suffix}"
        else:
            suffix = 1
            long_name = f"{long_name}1"
            while mc.objExists(long_name):
                suffix += 1
                long_name = f"{long_name[:-1]}{suffix}"

        new_short_name = long_name.split("|")[-1]

        return new_short_name, name_part_dict
    
    @staticmethod
    def check_shape_parent_names(parent_name: str, shape_name: str) -> bool:
        """
        Check if the shape name contains the parent name.

        Parameters
        ----------
        parent_name : str
            The parent name.
        shape_name : str
            The shape name.

        Returns
        -------
        bool
            True if the parent name is in the shape name, False otherwise.
        """
        return parent_name in shape_name

    @staticmethod
    def select_elements(item: QTreeWidgetItem) -> None:
        """
        Select the elements in Maya corresponding to the selected items in the tree widget.

        This method translates tree widget selections to Maya scene selections.

        Parameters
        ----------
        item : QTreeWidgetItem
            The tree widget item clicked.

        Raises
        ------
        RuntimeError
            If selecting elements in Maya fails.
        """
        try:
            tree_widget = item.treeWidget()
            items = tree_widget.selectedItems()
            names = [item.data(0, Qt.UserRole)[0] for item in items]
            mc.select(names, replace=True)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to select elements: {str(e)}")
        
