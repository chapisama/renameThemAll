from enum import Enum, auto
import os
import json

from renameThemAll.default_settings import DefaultColor, DefaultGroupType, DefaultMeshType, DefaultZoningSingle, DefaultOrientSingle, DefaultMainGroup, DefaultSymmetryOptions, DefaultNameStructure, DefaultNumIncLenght

NO_PRESET = "Default preset"
NO_LEXICON = "No lexicon"

class ObjType(Enum):
    TRANSFORM = auto()
    REFERENCE = auto()
    INSTANCE = auto()
    TRANSFO_MESH = auto()
    MESH = auto()

OBJ_TYPE_DICT = {obj_type.name.lower(): obj_type.name.lower() for obj_type in ObjType}

DEFAULT_COLORS = {color.name.lower(): color.value for color in DefaultColor}

def get_user_settings():
    """
    Retrieves user settings from the user settings logics class.

    Returns:
    dict: A dictionary containing user settings.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'user_settings.json')
    if not os.path.exists(file_path):
        return {"last_preset": NO_PRESET, "presets": {}}
    with open(file_path, 'r') as f:
        return json.load(f)

def get_last_preset():
    """
    Retrieves the last user settings from the user settings logics class.

    Returns:
    dict: A dictionary containing the last user settings.
    """
    settings = get_user_settings()
    return settings['last_preset']

def get_user_name_structure():
    """
    Retrieves the user name structure from the user settings logics class.
    """
    settings = get_user_settings()
    if settings['presets'][get_last_preset()]['structure'] == "" or settings['presets'][get_last_preset()] == NO_PRESET:
        return DefaultNameStructure.NAME_STRUCTURE.value
    return settings['presets'][get_last_preset()]['structure']

def get_user_main_group():
    """
    Retrieves the user main group from the user settings logics class.

    Returns:
    dict: A dictionary containing the user main group.
    """
    settings = get_user_settings()
    if settings['presets'][get_last_preset()]['main_group'] == "" or settings['presets'][get_last_preset()] == NO_PRESET:
        return DefaultMainGroup.ALL.value
    return settings['presets'][get_last_preset()]['main_group']

def get_user_group_types():
    """
    Retrieves the user group types from the user settings logics class.

    Returns:
    dict: A dictionary containing the user group types.
    """
    settings = get_user_settings()
    if settings['presets'][get_last_preset()]['group_types'] == {} or settings['presets'][get_last_preset()] == NO_PRESET:
        return {type.value: type.value for type in DefaultGroupType}
    return settings['presets'][get_last_preset()]['group_types']

def get_user_mesh_types():
    """
    Retrieves the user mesh types from the user settings logics class.

    Returns:
    dict: A dictionary containing the user mesh types.
    """
    settings = get_user_settings()
    if settings['presets'][get_last_preset()]['mesh_types'] == {} or settings['presets'][get_last_preset()] == NO_PRESET:
        return {type.value: type.value for type in DefaultMeshType}
    return settings['presets'][get_last_preset()]['mesh_types']

def get_user_zoning():
    """
    Retrieves the user zoning from the user settings logics class.

    Returns:
    dict: A dictionary containing the user zoning.  
    """
    settings = get_user_settings()
    if settings['presets'][get_last_preset()]['zoning'] == {} or settings['presets'][get_last_preset()] == NO_PRESET:
        return {zoning.name.capitalize(): zoning.value for zoning in DefaultZoningSingle}
    return settings['presets'][get_last_preset()]['zoning']

def get_user_orientation():
    """
    Retrieves the user orientation from the user settings logics class. 

    Returns:
    dict: A dictionary containing the user orientation.
    """
    settings = get_user_settings()
    if settings['presets'][get_last_preset()]['orientation'] == {} or settings['presets'][get_last_preset()] == NO_PRESET:
        return {orient.name.capitalize(): orient.value for orient in DefaultOrientSingle}
    return settings['presets'][get_last_preset()]['orientation']

def get_user_symmetry():
    """
    Retrieves the user symmetry from the user settings logics class.
    """ 
    settings = get_user_settings()
    if settings['presets'][get_last_preset()]['symmetry'] == {} or settings['presets'][get_last_preset()] == NO_PRESET:
        return {option.name: option.value for option in DefaultSymmetryOptions}
    return settings['presets'][get_last_preset()]['symmetry']

def get_user_n_inc_lenght():
    """
    Retrieves the user numerical increment length from the user settings logics class.
    """
    settings = get_user_settings()
    if settings['presets'][get_last_preset()]['n_inc_lenght'] == None or settings['presets'][get_last_preset()] == NO_PRESET:
        return DefaultNumIncLenght.NUMBER_OF_DIGITS.value
    return settings['presets'][get_last_preset()]['n_inc_lenght']

def get_user_optional_checkbox():
    """
    Retrieves the user optional checkbox from the user settings logics class.
    """
    settings = get_user_settings()
    if settings['presets'][get_last_preset()] == NO_PRESET:
        return None
    return settings['presets'][get_last_preset()]['checkbox_entries']

def build_categories_dict():
    """
    Builds a dictionary for categories.
    """
    optional_categories = []
    mandatory_categories = []
    if not get_user_optional_checkbox():
        return DefaultNameStructure.OPTIONAL_CATEGORIES.value, DefaultNameStructure.MANDATORY_CATEGORIES.value
    else:
        for key, value in get_user_optional_checkbox().items():
            if value:
                optional_categories.append(key)
            else:
                mandatory_categories.append(key)
        for value in DefaultNameStructure.MANDATORY_CATEGORIES.value:
            if value not in mandatory_categories and value not in optional_categories:
                mandatory_categories.append(value)
        for value in DefaultNameStructure.OPTIONAL_CATEGORIES.value:
            if value not in optional_categories and value not in mandatory_categories:
                optional_categories.append(value)
    return optional_categories, mandatory_categories

def get_used_categories(name_structure: str):
    """
    Retrieves the used categories from the user settings logics class.
    """
    """
    Retrieves all categories (strings between square brackets) from the name structure.

    Parameters
    ----------
    name_structure : str
        The name structure to analyze

    Returns
    -------
    list
        List of strings found between square brackets in the name structure
    """
    import re
    return re.findall(r'\[([^\]]+)\]', name_structure)

NAME_STRUCTURE = get_user_name_structure() if get_last_preset() != NO_PRESET else DefaultNameStructure.NAME_STRUCTURE.value
USED_CATEGORIES = get_used_categories(NAME_STRUCTURE)
OPTIONAL_CATEGORIES, MANDATORY_CATEGORIES = build_categories_dict() if get_last_preset() != NO_PRESET else (DefaultNameStructure.OPTIONAL_CATEGORIES.value, DefaultNameStructure.MANDATORY_CATEGORIES.value)

MAIN_GROUP_DICT = get_user_main_group() if get_last_preset() != NO_PRESET and get_user_main_group() != "" else DefaultMainGroup.ALL.value
GROUP_TYPES_DICT = get_user_group_types() if get_last_preset() != NO_PRESET and get_user_group_types() != {} else {type.value: type.value for type in DefaultGroupType}
MESH_TYPES_DICT = get_user_mesh_types() if get_last_preset() != NO_PRESET and get_user_mesh_types() != {} else {type.value: type.value for type in DefaultMeshType}
ALL_TYPES_DICT = GROUP_TYPES_DICT | MESH_TYPES_DICT

class OptionsA(Enum):
    SELECTION = "selections"
    ALL_GROUPS = "all groups"
    ALL_MESHES = "all meshes"

OPTIONS_A = {option.name.lower(): option.value for option in OptionsA}

class OptionsB(Enum):
    SELECT_AND_CHILD = "selects and childs"
    SELECTION = "selections"

OPTIONS_B = {option.name.lower(): option.value for option in OptionsB}

class IncOptions(Enum):
    A_TO_Z = "A to Z"
    LETTERS = "letters"
    ZERO_TO_999 = "0 to 999"
    NUMBERS = "numbers"

INC_OPTIONS = {option.name: option.value for option in IncOptions}

INC_NUMBER_OF_DIGITS = get_user_n_inc_lenght() if get_last_preset() != NO_PRESET else DefaultNumIncLenght.NUMBER_OF_DIGITS.value

SYMMETRY_OPTIONS = get_user_symmetry() if get_last_preset() != NO_PRESET else {option.name.capitalize(): option.value for option in DefaultSymmetryOptions}
ZONING_SINGLE_DICT = get_user_zoning() if get_last_preset() != NO_PRESET else {zoning.name.capitalize(): zoning.value for zoning in DefaultZoningSingle}
ORIENT_SINGLE_DICT = get_user_orientation() if get_last_preset() != NO_PRESET else {orient.name.capitalize(): orient.value for orient in DefaultOrientSingle}

def build_zoning_dict():
    """
    Builds a dictionary for zoning suffixes.

    Returns:
    dict: A dictionary with combined zoning suffixes.
    """
    zoning_dict = ZONING_SINGLE_DICT.copy()
    
    zoning_dict["Top_Left"] = zoning_dict["Top"] + zoning_dict["Left"]
    zoning_dict["Top_Center"] = zoning_dict["Top"] + zoning_dict["Center"]
    zoning_dict["Top_Right"] = zoning_dict["Top"] + zoning_dict["Right"]
    zoning_dict["Middle_Left"] = zoning_dict["Middle"] + zoning_dict["Left"]
    zoning_dict["Middle_Center"] = zoning_dict["Middle"] + zoning_dict["Center"]
    zoning_dict["Middle_Right"] = zoning_dict["Middle"] + zoning_dict["Right"]
    zoning_dict["Bottom_Left"] = zoning_dict["Bottom"] + zoning_dict["Left"]
    zoning_dict["Bottom_Center"] = zoning_dict["Bottom"] + zoning_dict["Center"]
    zoning_dict["Bottom_Right"] = zoning_dict["Bottom"] + zoning_dict["Right"]
    zoning_dict["Front_Left"] = zoning_dict["Front"] + zoning_dict["Left"]
    zoning_dict["Front_Center"] = zoning_dict["Front"] + zoning_dict["Center"]
    zoning_dict["Front_Right"] = zoning_dict["Front"] + zoning_dict["Right"]
    zoning_dict["Back_Left"] = zoning_dict["Back"] + zoning_dict["Left"]
    zoning_dict["Back_Center"] = zoning_dict["Back"] + zoning_dict["Center"]
    zoning_dict["Back_Right"] = zoning_dict["Back"] + zoning_dict["Right"]
    
    return zoning_dict

ZONING_DICT = build_zoning_dict()

def build_orientation_dict():
    """
    Builds a dictionary for orientation suffixes.

    Returns:
    dict: A dictionary with combined orientation suffixes.
    """
    orient_dict = ORIENT_SINGLE_DICT.copy()
    
    orient_dict["North_East"] = orient_dict["North"] + orient_dict["East"]
    orient_dict["North_West"] = orient_dict["North"] + orient_dict["West"]
    orient_dict["South_East"] = orient_dict["South"] + orient_dict["East"]
    orient_dict["South_West"] = orient_dict["South"] + orient_dict["West"]

    return orient_dict

ORIENT_DICT = build_orientation_dict()

MANUAL_NAME_STRUCTURE = os.path.join(os.path.dirname(__file__), 'resources', 'manual_name_structure.md')
MANUAL_MAIN_GROUP = os.path.join(os.path.dirname(__file__), 'resources', 'manual_main_group.md')
MANUAL_TYPE = os.path.join(os.path.dirname(__file__), 'resources', 'manual_type.md')
MANUAL_ZONING = os.path.join(os.path.dirname(__file__), 'resources', 'manual_zoning.md')
MANUAL_ORIENTATION = os.path.join(os.path.dirname(__file__), 'resources', 'manual_orientation.md')
MANUAL_SYMMETRY = os.path.join(os.path.dirname(__file__), 'resources', 'manual_symmetry.md')
MANUAL_INC = os.path.join(os.path.dirname(__file__), 'resources', 'manual_inc.md')
ABOUT_TEXT = os.path.join(os.path.dirname(__file__), 'resources', 'about.md')