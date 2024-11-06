import json
import os

try:
    from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTreeWidgetItem
    from PySide6.QtCore import Qt
except ImportError:
    from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QTreeWidgetItem
    from PySide2.QtCore import Qt

from renameThemAll.constants import (
    ORIENT_DICT,
    ZONING_DICT,
    OBJ_TYPE_DICT,
    ALL_TYPES_DICT,
    DEFAULT_COLORS,
    NO_LEXICON,
    SYMMETRY_OPTIONS,
    GROUP_TYPES_DICT,
    MESH_TYPES_DICT,
)
from renameThemAll.name_structure_inspector import NameStructureInspector

class OutlinerTextColored(QWidget):
    """
    A widget for displaying colored text in an outliner.

    This class provides functionality to parse and color different parts of an object's name
    based on naming conventions and object types.

    Attributes
    ----------
    item : QTreeWidgetItem
        The tree widget item associated with this widget.
    text : str
        The original text to be displayed and colored.
    editing : bool
        Flag indicating whether the widget is currently being edited.
    colors : dict
        Dictionary of colors for different parts of the text.
    name_part_dict : dict
        Dictionary containing the parsed parts of the name.
    lbl_colored : QLabel
        Label widget displaying the colored text.
    """

    def __init__(self, item: QTreeWidgetItem, text: str, colors: dict = None) -> None:
        """
        Initialize the OutlinerTextColored widget.

        Parameters
        ----------
        item : QTreeWidgetItem
            The tree widget item associated with this widget.
        text : str
            The text to display in the widget.
        colors : dict, optional
            A dictionary of colors for different types of text. If not provided,
            DEFAULT_COLORS will be used.

        Returns
        -------
        None
        """
        super().__init__()
        self.item = item
        self.text = text
        self.editing = False
        self.colors = colors or DEFAULT_COLORS
        self.name_part_dict = NameStructureInspector.inspect_name_structure(text)
        self.init_ui()

    def create_label_colored(self, txt_colored: str) -> QLabel:
        """
        Create a QLabel widget with colored text.

        Parameters
        ----------
        txt_colored : str
            The HTML string with colored text.

        Returns
        -------
        QLabel
            The QLabel widget with colored text.
        """
        self.lbl_colored = QLabel(self)
        self.lbl_colored.setText(txt_colored)
        return self.lbl_colored

    def create_layout(self, widget: QWidget) -> None:
        """
        Create the layout for the widget.

        This method sets up a vertical layout for the widget and adds the colored label to it.

        Parameters
        ----------
        widget : QWidget
            The widget to add to the layout.

        Returns
        -------
        None
        """
        layout_color = QVBoxLayout()
        layout_color.setContentsMargins(2, 2, 2, 2)
        layout_color.addWidget(self.lbl_colored)
        self.setLayout(layout_color)

    @staticmethod
    def set_colored_text(obj_data: tuple, name_part_dict: dict, lexicon_name: str = NO_LEXICON) -> str:
        """
        Set the text color based on the naming convention and object type.

        This method determines the appropriate coloring for the text based on the object type
        and naming convention, then applies the coloring.

        Parameters
        ----------
        obj_data : tuple
            A tuple containing object data, where the second element is the object type.
        name_part_dict : dict
            A dictionary containing the parts of the name.

        Returns
        -------
        str
            The HTML string with colored text.
        """
        obj_type = obj_data[1]
        colors = DEFAULT_COLORS
        if obj_type == OBJ_TYPE_DICT.get("reference"):
            txt_colored = OutlinerTextColored.set_reference_color(name_part_dict, colors)
        elif obj_type == OBJ_TYPE_DICT.get("instance"):
            txt_colored = OutlinerTextColored.set_instance_color(name_part_dict, colors)
        elif "bad_naming" in name_part_dict:
            txt_colored = f'<span style="color: {colors["invalid"]};">{name_part_dict["bad_naming"]}</span>'
        else:
            for index in name_part_dict:
                for key in name_part_dict[index]:
                    if key == "type" and name_part_dict[index][key]:
                        name_part_dict[index][key] = OutlinerTextColored.set_type_color(name_part_dict[index][key], colors, obj_type)
                    elif key == "name" and name_part_dict[index][key]:
                        name_part_dict[index][key] = OutlinerTextColored.set_name_color(name_part_dict[index][key], colors, lexicon_name, obj_type)
                    elif key == "zoning" and name_part_dict[index][key]:
                        name_part_dict[index][key] = OutlinerTextColored.set_zoning_color(name_part_dict[index][key], colors)
                    elif key == "orientation" and name_part_dict[index][key]:
                        name_part_dict[index][key] = OutlinerTextColored.set_orientation_color(name_part_dict[index][key], colors)
                    elif key == "alphabetical_inc" and name_part_dict[index][key]:
                        name_part_dict[index][key] = OutlinerTextColored.set_a_inc_color(name_part_dict[index][key], colors)
                    elif key == "numerical_inc" and name_part_dict[index][key]:
                        name_part_dict[index][key] = OutlinerTextColored.set_n_inc_color(name_part_dict[index][key], colors)
                    elif key == "symmetry" and name_part_dict[index][key]:
                        name_part_dict[index][key] = OutlinerTextColored.set_symmetry_color(name_part_dict[index][key], colors)
                    elif key == "bad_naming" and name_part_dict[index][key]:
                        txt_colored = f'<span style="color: {colors["invalid"]};">{name_part_dict[index][key]}</span>'
                        name_part_dict[index][key] = txt_colored

            txt_colored = NameStructureInspector.rebuilt_name(name_part_dict)

        return txt_colored

    @staticmethod
    def set_reference_color(name_part_dict: dict, colors: dict) -> str:
        """
        Set the text color for reference objects.

        Parameters
        ----------
        name_part_dict : dict
            A dictionary containing the parts of the name.
        colors : dict
            A dictionary of colors for different types of text.

        Returns
        -------
        str
            The HTML string with colored text for reference objects.
        """
        full_name = NameStructureInspector.rebuilt_name(name_part_dict)
        return f'<span style="color: {colors["reference"]};">{full_name}</span>'

    @staticmethod
    def set_instance_color(name_part_dict: dict, colors: dict) -> str:
        """
        Set the text color for instance objects.

        Parameters
        ----------
        name_part_dict : dict
            A dictionary containing the parts of the name.
        colors : dict
            A dictionary of colors for different types of text.

        Returns
        -------
        str
            The HTML string with colored text for instance objects.
        """
        full_name = NameStructureInspector.rebuilt_name(name_part_dict)
        return f'<span style="color: {colors["instance"]};">{full_name}</span>'

    @staticmethod
    def set_type_color(type:str, colors: dict, obj_type: str) -> dict:
        """
        Set the text color for the type part of the name.

        Parameters
        ----------
        name_part_dict : dict
            A dictionary containing the parts of the name.
        colors : dict
            A dictionary of colors for different types of text.

        Returns
        -------
        dict
            Updated name_part_dict with colored type.
        """
        if obj_type == "transform":
            types_dict = GROUP_TYPES_DICT
        elif obj_type == "transfo_mesh":
            types_dict = MESH_TYPES_DICT
        else:
            types_dict = ALL_TYPES_DICT
        if type and type in types_dict.values():
            return f'<span style="color: {colors["valid_suffixes"]};">{type}</span>'
        elif type and type not in types_dict.values():
            return f'<span style="color: {colors["invalid"]};">{type}</span>'

    @staticmethod
    def set_name_color(name: str, colors: dict, lexicon_name: str, obj_type: str) -> str:
        """
        Set the text color for the main part of the name.

        Parameters
        ----------
        name_part_dict : dict
            A dictionary containing the parts of the name.
        colors : dict
            A dictionary of colors for different types of text.
        lexicon_name : str
            The name of the lexicon.
        obj_type : str
            The type of the object.

        Returns
        -------
        str
            The HTML string with colored main name.
        """
        if lexicon_name == NO_LEXICON:
            return f'<span style="color: {colors["to_check"]};">{name}</span>'
        else:
            database_path = os.path.join(os.path.dirname(__file__), "lexicon_database.json")
            with open(database_path, 'r') as f:
                data = json.load(f)

            lexicon_words = []
            if obj_type == "transform":
                lexicon_words = data.get(lexicon_name, {}).get("groups", [])
            elif obj_type == "transfo_mesh":
                lexicon_words = data.get(lexicon_name, {}).get("meshes", [])

            if name in lexicon_words:
                return f'<span style="color: {colors["valid"]};">{name}</span>'
            else:
                return f'<span style="color: {colors["to_check"]};">{name}</span>'
            
    @staticmethod
    def set_symmetry_color(symmetry: str, colors: dict) -> str:
        """
        Set the text color for the symmetry part of the name.

        Parameters
        ----------
        symmetry : str
            The symmetry part of the name.
        colors : dict
            A dictionary of colors for different types of text.

        Returns
        -------
        str
            The HTML string with colored symmetry.
        """
        if symmetry and symmetry in SYMMETRY_OPTIONS.values():
            return f'<span style="color: {colors["valid_suffixes"]};">{symmetry}</span>'
        elif symmetry and symmetry not in SYMMETRY_OPTIONS.values():
            return f'<span style="color: {colors["invalid"]};">{symmetry}</span>'

    @staticmethod
    def set_zoning_color(zoning: str, colors: dict) -> str:
        """
        Set the text color for the zoning part of the name.

        Parameters
        ----------
        name_part_dict : dict
            A dictionary containing the parts of the name.
        colors : dict
            A dictionary of colors for different types of text.

        Returns
        -------
        str
            The HTML string with colored zoning.
        """
        if zoning and zoning in ZONING_DICT.values():
            return f'<span style="color: {colors["valid_suffixes"]};">{zoning}</span>'
        elif zoning and zoning not in ZONING_DICT.values():
            return f'<span style="color: {colors["invalid"]};">{zoning}</span>'

    @staticmethod
    def set_orientation_color(orientation: str, colors: dict) -> str:
        """
        Set the text color for the orientation part of the name.

        Parameters
        ----------
        orientation : str
            A dictionary containing the parts of the name.
        colors : dict
            A dictionary of colors for different types of text.

        Returns
        -------
        dict
            The HTML string with colored orientation.
        """
        if orientation and orientation in ORIENT_DICT.values():
            return f'<span style="color: {colors["valid_suffixes"]};">{orientation}</span>'
        elif orientation and orientation not in ORIENT_DICT.values():
            return f'<span style="color: {colors["invalid"]};">{orientation}</span>'

    @staticmethod
    def set_a_inc_color(a_inc: str, colors: dict) -> str:
        """
        Set the text color for the alphabetical increment part of the name.

        Parameters
        ----------
        name_part_dict : dict
            A dictionary containing the parts of the name.
        colors : dict
            A dictionary of colors for different types of text.

        Returns
        -------
        dict
            Updated name_part_dict with colored alphabetical increment.
        """
        if a_inc and len(a_inc) == 1 and a_inc.isupper():
            return f'<span style="color: {colors["valid_suffixes"]};">{a_inc}</span>'
        else:
            return f'<span style="color: {colors["invalid"]};">{a_inc}</span>'


    @staticmethod
    def set_n_inc_color(n_inc: str, colors: dict) -> str:
        """
        Set the text color for the numerical increment part of the name.

        This method is currently a placeholder and does not modify the name_part_dict.

        Parameters
        ----------
        name_part_dict : dict
            A dictionary containing the parts of the name.
        colors : dict
            A dictionary of colors for different types of text.

        Returns
        -------
        str
            The HTML string with colored numerical increment.
        """
        if n_inc:
            if n_inc.isdigit():
                return f'<span style="color: {colors["valid_suffixes"]};">{n_inc}</span>'
            else:
                return f'<span style="color: {colors["invalid"]};">{n_inc}</span>'
    

    
