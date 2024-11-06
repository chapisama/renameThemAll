import re
from typing import List, Dict, Tuple

from renameThemAll.constants import NAME_STRUCTURE, OPTIONAL_CATEGORIES, MANDATORY_CATEGORIES, SYMMETRY_OPTIONS, ORIENT_SINGLE_DICT, ZONING_SINGLE_DICT, ALL_TYPES_DICT, INC_NUMBER_OF_DIGITS


class NameStructureInspector:
    """
    A class used to inspect and manipulate the structure of names.

    This class provides various static methods to inspect, separate, and handle different parts of a name
    based on predefined categories such as symmetry, type, zoning, orientation, alphabetical increment, 
    and numerical increment. It also includes methods to handle bad naming conventions and to rebuild names 
    from their components.

    Methods
    -------
    inspect_name_structure() -> Dict[int, Dict[str, str]]:
        Inspects the structure of a name and divides it into its components.
    
    get_before_after_mandatory(mandatory_name: str, index: int, part_dict: Dict[int, Dict[str, str]]) -> Tuple[List[str], List[str]]:
        Retrieves the categories before and after a mandatory category in a part dictionary.
    
    handle_bad_naming(part_dict: Dict[int, Dict[str, str]], part_index: int) -> None:
        Handles bad naming by clearing all categories except 'bad_naming' in a part dictionary.
    
    separate_category(name: str, part_index: int, name_part_index: int, part_dict: Dict[int, Dict[str, str]], start: bool, prefix_name: str = "") -> Dict[int, Dict[str, str]]:
        Separates a category from a name based on its position and updates the part dictionary.
    
    separate_category_start(part_dict: Dict[int, Dict[str, str]], part_index: int, part_to_separate: str) -> Tuple[Dict[int, Dict[str, str]], str]:
        Separates categories from the start of a part and updates the part dictionary.
    
    separate_category_end(part_dict: Dict[int, Dict[str, str]], part_index: int, part_to_separate: str, prefix_name: str) -> Tuple[Dict[int, Dict[str, str]], str]:
        Separates categories from the end of a part and updates the part dictionary.
    
    process_category(key: str, part_dict: Dict[int, Dict[str, str]], part_index: int, part_to_separate: str, start: bool) -> str:
        Processes a category by separating its value from a part and updating the part dictionary.
    
    separate_value(part_to_separate: str, value_list: List[str], start: bool) -> Tuple[str, str]:
        Separates a value from a part based on a list of possible values and its position.
    
    remove_prefix(string: str, prefix: str) -> str:
        Removes a prefix from a string if it exists.
    
    handle_remaining_part(part_dict: Dict[int, Dict[str, str]], part_index: int, part_to_separate: str) -> None:
        Handles the remaining part of a name by marking it as 'bad_naming' if necessary.
    
    separate_value_recursive(part_to_separate: str, value_list: List[str], start: bool = False) -> Tuple[str, str]:
        Recursively separates values from a part based on a list of possible values and its position.
    
    separate_suffixes_recurcive(part_to_separate: str, value_list: List[str], backup_suffix: str = "", start: bool = False) -> Tuple[str, str]:
        Recursively separates suffixes from a part based on a list of possible values and its position.
    """
    
    @staticmethod
    def inspect_name_structure(name: str, name_structure: str = NAME_STRUCTURE) -> Dict[int, Dict[str, str]]:
        """
        Inspects the structure of a name and divides it into its components.

        Parameters
        ----------
        name : str
            The name to be inspected.
        name_structure : str, optional
            The structure of the name, by default NAME_STRUCTURE.

        Returns
        -------
        Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        """
        optional_categories = OPTIONAL_CATEGORIES
        optional_parts = [] #parts refers to text pieces separated by "_"
        mandatory_parts = []
        #TODO: handle the "or" case
        name_parts = re.split(r'_(?![^\[]*\])', name_structure) #split on "_" but not on "_" inside []

        len_name_parts = len(name_parts)
        part_index=0
        part_dict={}
        name_lenght=len(name.split("_"))

        for part in name_parts:
            part_dict[part_index] = {word.strip('[]'): '' for word in re.findall(r'\[([^\]]+)\]', part)} #gets the [] and replaces them with ''
            part_index+=1

        for part_index, categories in part_dict.items():
            if all(category in optional_categories for category in categories.keys()):
                optional_parts.append(part_index)
            else:
                mandatory_parts.append(part_index)

        if name_lenght < len(mandatory_parts):
            for index in part_dict:
                if "name" in part_dict[index]:
                    part_dict[index]["name"] = name
                    break
        elif name_lenght > len(name_parts):
            part_dict["bad_naming"] = name
        elif name_lenght == len(name_parts): 
            prefix_name=""           
            for index in list(part_dict.keys()):
                if 'name' in part_dict[index]:
                    before_name_categories, after_name_categories = NameStructureInspector.get_before_after_name(index, part_dict)               
                    if before_name_categories:
                        for category in before_name_categories:
                            in_name_pos = index
                            part_dict = NameStructureInspector.separate_category(name, index, in_name_pos, part_dict, start=True)
                    if after_name_categories:
                        if before_name_categories:
                            for category in before_name_categories:
                                prefix_name += part_dict[index][category]
                        for category in reversed(after_name_categories):
                            in_name_pos = index
                            part_dict = NameStructureInspector.separate_category(name, index, in_name_pos, part_dict, start=False, prefix_name=prefix_name)
                    if not before_name_categories and not after_name_categories:
                        part_dict[index]["name"] = name.split("_")[index]
                else:
                    categories = list(part_dict[index].keys())
                    for category in categories:
                        in_name_pos = index
                        part_dict = NameStructureInspector.separate_category(name, index, in_name_pos, part_dict, start=True)
        else:
            NameStructureInspector.traverse_name_parts(name, len_name_parts, 0, 0, optional_parts, mandatory_parts, part_dict)

        return part_dict

    @staticmethod
    def rebuilt_name(part_dict: Dict[int, Dict[str, str]]) -> str:
        """
        Rebuilds a name from its components in the part dictionary.

        Parameters
        ----------
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.

        Returns
        -------
        str
            The rebuilt name.
        """
        rebuilt_name=""
        if "bad_naming" in part_dict.keys():
            rebuilt_name = part_dict["bad_naming"]
            return rebuilt_name
        
        for index in list(part_dict.keys()):
            if all(value == '' for value in part_dict[index].values()):
                continue
            for key in part_dict[index]:
                rebuilt_name += part_dict[index][key]
            rebuilt_name += "_"
        rebuilt_name = rebuilt_name.strip("_")
        return rebuilt_name

    @staticmethod
    def traverse_name_parts(name: str, len_name_parts: int, part_index: int, in_name_pos: int, optional_parts: List[int], mandatory_parts: List[int], part_dict: Dict[int, Dict[str, str]]) -> None:
        """
        Traverses the name parts and updates the part dictionary accordingly.

        Parameters
        ----------
        name : str
            The name to be traversed.
        len_name_parts : int
            The length of the name parts.
        part_index : int
            The current part index.
        in_name_pos : int
            The current position in the name.
        optional_parts : List[int]
            A list of optional part indices.
        mandatory_parts : List[int]
            A list of mandatory part indices.
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        """
        if in_name_pos == len(name.split("_")):
            return
        
        if part_index in optional_parts:
            NameStructureInspector.check_optional_part(name, len_name_parts, part_index, in_name_pos, optional_parts, mandatory_parts, part_dict)
        elif part_index in mandatory_parts:
            NameStructureInspector.check_mandatory_part(name, len_name_parts, part_index, in_name_pos, optional_parts, mandatory_parts, part_dict)


    @staticmethod
    def check_optional_part(name: str, len_name_parts: int, part_index: int, in_name_pos: int, optional_parts: List[int], mandatory_parts: List[int], part_dict: Dict[int, Dict[str, str]]) -> None:
        """
        Checks and processes an optional part of the name.

        Parameters
        ----------
        name : str
            The name to be checked.
        len_name_parts : int
            The length of the name parts.
        part_index : int
            The current part index.
        in_name_pos : int
            The current position in the name.
        optional_parts : List[int]
            A list of optional part indices.
        mandatory_parts : List[int]
            A list of mandatory part indices.
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        """
        categories = list(part_dict[part_index].keys())
        part_filled=False

        for category in categories:
            part_dict = NameStructureInspector.separate_category(name, part_index, in_name_pos, part_dict, start=True)
            if part_dict[part_index][category] != "":
                part_filled = True
        
        if part_filled:
            in_name_pos += 1
            part_index += 1
            part_dict = NameStructureInspector.traverse_name_parts(name, len_name_parts, part_index, in_name_pos, optional_parts, mandatory_parts, part_dict)
        elif "bad_naming" in part_dict[part_index] and part_index != len_name_parts:
            NameStructureInspector.handle_bad_naming(part_dict, part_index)
            part_index += 1
            part_dict = NameStructureInspector.traverse_name_parts(name, len_name_parts, part_index, in_name_pos, optional_parts, mandatory_parts, part_dict)
        else:
            in_name_pos += 1
            part_index += 1
            part_dict = NameStructureInspector.traverse_name_parts(name, len_name_parts, part_index, in_name_pos, optional_parts, mandatory_parts, part_dict)

        return part_dict

    @staticmethod
    def check_mandatory_part(name: str, len_name_parts: int, part_index: int, in_name_pos: int, optional_parts: List[int], mandatory_parts: List[int], part_dict: Dict[int, Dict[str, str]]) -> None:
        """
        Checks and processes a mandatory part of the name.

        Parameters
        ----------
        name : str
            The name to be checked.
        len_name_parts : int
            The length of the name parts.
        part_index : int
            The current part index.
        in_name_pos : int
            The current position in the name.
        optional_parts : List[int]
            A list of optional part indices.
        mandatory_parts : List[int]
            A list of mandatory part indices.
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        """
        mandatory_categories = MANDATORY_CATEGORIES 
        
        if "name" in part_dict[part_index]:
            part_dict = NameStructureInspector.handle_name_category(name, len_name_parts, part_index, in_name_pos, optional_parts, mandatory_parts, part_dict)
        else:
            part_dict = NameStructureInspector.handle_other_mandatory_category(name, len_name_parts, part_index, in_name_pos, optional_parts, mandatory_parts, part_dict, mandatory_categories)

        return part_dict

    @staticmethod
    def handle_name_category(name: str, len_name_parts: int, part_index: int, in_name_pos: int, optional_parts: List[int], mandatory_parts: List[int], part_dict: Dict[int, Dict[str, str]]) -> None:
        """
        Handles the 'name' category in the part dictionary.

        Parameters
        ----------
        name : str
            The name to be handled.
        len_name_parts : int
            The length of the name parts.
        part_index : int
            The current part index.
        in_name_pos : int
            The current position in the name.
        optional_parts : List[int]
            A list of optional part indices.
        mandatory_parts : List[int]
            A list of mandatory part indices.
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        """
        before_name_categories, after_name_categories = NameStructureInspector.get_before_after_name(part_index, part_dict)
        prefix_name = ""
        
        if before_name_categories:
            for category in before_name_categories:
                part_dict = NameStructureInspector.separate_category(name, part_index, in_name_pos, part_dict, start=True)
        
        if after_name_categories:
            if before_name_categories:
                for category in before_name_categories:
                    prefix_name += part_dict[part_index][category]
            for category in reversed(after_name_categories):
                part_dict = NameStructureInspector.separate_category(name, part_index, in_name_pos, part_dict, start=False, prefix_name=prefix_name)
        
        if not before_name_categories and not after_name_categories:
            part_dict[part_index]["name"] = name.split("_")[in_name_pos]
        
        part_index += 1
        in_name_pos += 1
        NameStructureInspector.traverse_name_parts(name, len_name_parts, part_index, in_name_pos, optional_parts, mandatory_parts, part_dict)

        

    @staticmethod
    def handle_other_mandatory_category(name: str, len_name_parts: int, part_index: int, in_name_pos: int, optional_parts: List[int], mandatory_parts: List[int], part_dict: Dict[int, Dict[str, str]], mandatory_categories: List[str]) -> None:
        """
        Handles other mandatory categories in the part dictionary.

        Parameters
        ----------
        name : str
            The name to be handled.
        len_name_parts : int
            The length of the name parts.
        part_index : int
            The current part index.
        in_name_pos : int
            The current position in the name.
        optional_parts : List[int]
            A list of optional part indices.
        mandatory_parts : List[int]
            A list of mandatory part indices.
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        mandatory_categories : List[str]
            A list of mandatory categories.
        """
        prefix_name = ""
        for category in part_dict[part_index]:
            if category in mandatory_categories:
                before_name_categories, after_name_categories = NameStructureInspector.get_before_after_mandatory(category, part_index, part_dict)
        
        if before_name_categories:
            for category in before_name_categories:
                part_dict = NameStructureInspector.separate_category(name, part_index, in_name_pos, part_dict, start=True, prefix_name=prefix_name)
        
        if after_name_categories:
            for category in reversed(after_name_categories):
                part_dict = NameStructureInspector.separate_category(name, part_index, in_name_pos, part_dict, start=False, prefix_name=prefix_name)
        
        if not before_name_categories and not after_name_categories:
            part_dict[part_index][category] = name.split("_")[in_name_pos]
        
        part_index += 1
        in_name_pos += 1
        NameStructureInspector.traverse_name_parts(name, len_name_parts, part_index, in_name_pos, optional_parts, mandatory_parts, part_dict)



    @staticmethod
    def get_before_after_name(index: int, part_dict: Dict[int, Dict[str, str]]) -> Tuple[List[str], List[str]]:
        """
        Retrieves the categories before and after the 'name' category in a part dictionary.

        Parameters
        ----------
        index : int
            The index of the part in the part dictionary.
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.

        Returns
        -------
        Tuple[List[str], List[str]]
            A tuple containing two lists: the categories before and after the 'name' category.
        """
        categories_in_part = list(part_dict[index].keys())
        name_position = categories_in_part.index('name')
        before_name_categories = []
        after_name_categories = [] 
        if name_position == 0:
            after_name_categories = categories_in_part[name_position+1:]
        elif name_position == len(categories_in_part) - 1:
            before_name_categories = categories_in_part[:name_position]               
        else:
            before_name_categories = categories_in_part[:name_position]
            after_name_categories = categories_in_part[name_position+1:]
        return before_name_categories, after_name_categories

    @staticmethod
    def get_before_after_mandatory(mandatory_name: str, index: int, part_dict: Dict[int, Dict[str, str]]) -> Tuple[List[str], List[str]]:
        """
        Retrieves the categories before and after a mandatory category in a part dictionary.

        Parameters
        ----------
        mandatory_name : str
            The name of the mandatory category.
        index : int
            The index of the part in the part dictionary.
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.

        Returns
        -------
        Tuple[List[str], List[str]]
            A tuple containing two lists: the categories before and after the mandatory category.
        """
        categories_in_part = list(part_dict[index].keys())
        mandatory_position = categories_in_part.index(mandatory_name)
        before_name_categories = []
        after_name_categories = []
        if mandatory_position == 0:
            after_name_categories = categories_in_part[mandatory_position+1:]
        elif mandatory_position == len(categories_in_part) - 1:
            before_name_categories = categories_in_part[:mandatory_position]
        else:
            before_name_categories = categories_in_part[:mandatory_position]
            after_name_categories = categories_in_part[mandatory_position+1:]
        return before_name_categories, after_name_categories

    @staticmethod
    def handle_bad_naming(part_dict: Dict[int, Dict[str, str]], part_index: int) -> None:
        """
        Handles bad naming by clearing all categories except 'bad_naming' in a part dictionary.

        Parameters
        ----------
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        part_index : int
            The index of the part in the part dictionary.
        """
        for key in part_dict[part_index]:
            if key != "bad_naming":
                part_dict[part_index][key] = ""
        del part_dict[part_index]["bad_naming"]

    @staticmethod
    def separate_category(name: str, part_index: int, name_part_index: int, part_dict: Dict[int, Dict[str, str]], start: bool, prefix_name: str = "") -> Dict[int, Dict[str, str]]:
        """
        Separates a category from a name based on its position and updates the part dictionary.

        Parameters
        ----------
        name : str
            The name to be separated.
        part_index : int
            The index of the part in the part dictionary.
        name_part_index : int
            The index of the name part to be separated.
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        start : bool
            Whether to start separating from the beginning of the name part.
        prefix_name : str, optional
            The prefix name to be used for separation, by default "".

        Returns
        -------
        Dict[int, Dict[str, str]]
            The updated part dictionary.
        """
        name_parts = name.split("_")
        part_to_separate = name_parts[int(name_part_index)]
        
        if start:
            part_dict, part_to_separate = NameStructureInspector.separate_category_start(part_dict, int(part_index), part_to_separate)
        else:
            part_dict, part_to_separate = NameStructureInspector.separate_category_end(part_dict, int(part_index), part_to_separate, prefix_name)
        
        if part_to_separate:
            NameStructureInspector.handle_remaining_part(part_dict, int(part_index), part_to_separate)
        
        return part_dict

    @staticmethod
    def separate_category_start(part_dict: Dict[int, Dict[str, str]], part_index: int, part_to_separate: str) -> Tuple[Dict[int, Dict[str, str]], str]:
        """
        Separates categories from the start of a part and updates the part dictionary.

        Parameters
        ----------
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        part_index : int
            The index of the part in the part dictionary.
        part_to_separate : str
            The part to be separated.

        Returns
        -------
        Tuple[Dict[int, Dict[str, str]], str]
            A tuple containing the updated part dictionary and the remaining part to be separated.
        """
        for key in part_dict[part_index]:
            part_to_separate = NameStructureInspector.process_category(key, part_dict, part_index, part_to_separate, start=True)
            if key == "name":
                break
        return part_dict, part_to_separate

    @staticmethod
    def separate_category_end(part_dict: Dict[int, Dict[str, str]], part_index: int, part_to_separate: str, prefix_name: str) -> Tuple[Dict[int, Dict[str, str]], str]:
        """
        Separates categories from the end of a part and updates the part dictionary.

        Parameters
        ----------
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        part_index : int
            The index of the part in the part dictionary.
        part_to_separate : str
            The part to be separated.
        prefix_name : str
            The prefix name to be used for separation.

        Returns
        -------
        Tuple[Dict[int, Dict[str, str]], str]
            A tuple containing the updated part dictionary and the remaining part to be separated.
        """
        for key in reversed(part_dict[part_index]):
            if key == "name":
                part_dict[part_index][key] = NameStructureInspector.remove_prefix(part_to_separate, prefix_name)
                break
            part_to_separate = NameStructureInspector.process_category(key, part_dict, part_index, part_to_separate, start=False)
        return part_dict, part_to_separate

    @staticmethod
    def process_category(key: str, part_dict: Dict[int, Dict[str, str]], part_index: int, part_to_separate: str, start: bool) -> str:
        """
        Processes a category by separating its value from a part and updating the part dictionary.

        Parameters
        ----------
        key : str
            The category key to be processed.
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        part_index : int
            The index of the part in the part dictionary.
        part_to_separate : str
            The part to be separated.
        start : bool
            Whether to start separating from the beginning of the part.

        Returns
        -------
        str
            The remaining part to be separated.
        """
        category_lists = {
            "symmetry": SYMMETRY_OPTIONS.values(),
            "type": ALL_TYPES_DICT.values(),
            "zoning": ZONING_SINGLE_DICT.values(),
            "orientation": ORIENT_SINGLE_DICT.values(),
            "alphabetical_inc": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "numerical_inc": INC_NUMBER_OF_DIGITS
        }
        
        if key in category_lists:
            if key == "orientation" or key == "zoning":
                value, part_to_separate = NameStructureInspector.separate_value_recursive(part_to_separate, category_lists[key], start)
            elif key == "numerical_inc":
                value, part_to_separate = NameStructureInspector.separate_number(part_to_separate, INC_NUMBER_OF_DIGITS, start)
            else:
                value, part_to_separate = NameStructureInspector.separate_value(part_to_separate, category_lists[key], start)
            part_dict[part_index][key] = value
        elif key == "name":
            part_dict[part_index][key] = part_to_separate
            part_to_separate = ""
        
        return part_to_separate
    
    @staticmethod
    def separate_number(part_to_separate: str, number_of_digits: int, start: bool) -> Tuple[str, str]:
        """
        Separates a number from a part based on its position.

        Parameters
        ----------
        part_to_separate : str
            The part to be separated.
        number_of_digits : int
            The number of digits to be separated.
        start : bool
            Whether to start separating from the beginning of the part.

        Returns
        -------
        Tuple[str, str]
            A tuple containing the separated number and the remaining part to be separated.
        """
        if start and len(part_to_separate) >= number_of_digits and part_to_separate[:number_of_digits].isdigit():
            return part_to_separate[:number_of_digits], part_to_separate[number_of_digits:]
        elif not start and len(part_to_separate) >= number_of_digits and part_to_separate[-number_of_digits:].isdigit():
            return part_to_separate[-number_of_digits:], part_to_separate[:-number_of_digits]
        return "", part_to_separate

    @staticmethod
    def separate_value(part_to_separate: str, value_list: List[str], start: bool) -> Tuple[str, str]:
        """
        Separates a value from a part based on a list of possible values and its position.

        Parameters
        ----------
        part_to_separate : str
            The part to be separated.
        value_list : List[str]
            A list of possible values for the category.
        start : bool
            Whether to start separating from the beginning of the part.

        Returns
        -------
        Tuple[str, str]
            A tuple containing the separated value and the remaining part to be separated.
        """
        for value in value_list:       
            if start and part_to_separate.startswith(value):
                return value, part_to_separate[len(value):]
            elif not start and part_to_separate.endswith(value):
                return value, part_to_separate[:-len(value)]
            
        return "", part_to_separate

    @staticmethod
    def remove_prefix(string: str, prefix: str) -> str:
        """
        Removes a prefix from a string if it exists.

        Parameters
        ----------
        string : str
            The string from which the prefix will be removed.
        prefix : str
            The prefix to be removed.

        Returns
        -------
        str
            The string without the prefix.
        """
        return string[len(prefix):] if prefix and string.startswith(prefix) else string

    @staticmethod
    def handle_remaining_part(part_dict: Dict[int, Dict[str, str]], part_index: int, part_to_separate: str) -> None:
        """
        Handles the remaining part of a name by marking it as 'bad_naming' if necessary.

        Parameters
        ----------
        part_dict : Dict[int, Dict[str, str]]
            A dictionary where each key is an index and the value is another dictionary 
            containing the categories and their corresponding values.
        part_index : int
            The index of the part in the part dictionary.
        part_to_separate : str
            The remaining part to be handled.
        """
        if 'name' not in part_dict[part_index]:
            part_dict[part_index]["bad_naming"] = part_to_separate

    @staticmethod
    def separate_value_recursive(part_to_separate: str, value_list: List[str], start: bool = False) -> Tuple[str, str]:
        """
        Recursively separates values from a part based on a list of possible values and its position.

        Parameters
        ----------
        part_to_separate : str
            The part to be separated.
        value_list : List[str]
            A list of possible values for the category.
        start : bool, optional
            Whether to start separating from the beginning of the part, by default False.

        Returns
        -------
        Tuple[str, str]
            A tuple containing the separated value and the remaining part to be separated.
        """
        if start:
            backup_suffix, part_to_separate = NameStructureInspector.separate_suffixes_recurcive(part_to_separate, value_list, start=True)          
        else:
            backup_suffix, part_to_separate = NameStructureInspector.separate_suffixes_recurcive(part_to_separate, value_list, start=False)
        return backup_suffix, part_to_separate

    @staticmethod
    def separate_suffixes_recurcive(part_to_separate: str, value_list: List[str], backup_suffix: str = "", start: bool = False) -> Tuple[str, str]:
        """
        Recursively separates suffixes from a part based on a list of possible values and its position.

        Parameters
        ----------
        part_to_separate : str
            The part to be separated.
        value_list : List[str]
            A list of possible values for the category.
        backup_suffix : str, optional
            The backup suffix to be used for separation, by default "".
        start : bool, optional
            Whether to start separating from the beginning of the part, by default False.

        Returns
        -------
        Tuple[str, str]
            A tuple containing the separated suffix and the remaining part to be separated.
        """
        if start:
            for value in value_list:
                if part_to_separate.startswith(value):
                    backup_suffix = f"{backup_suffix}{value}"
                    part_to_separate = part_to_separate[len(value):]
                    backup_suffix, part_to_separate = NameStructureInspector.separate_suffixes_recurcive(part_to_separate, value_list, backup_suffix, start=True)
                    return backup_suffix, part_to_separate
        else:
            for value in value_list:
                if part_to_separate.endswith(value):
                    backup_suffix = f"{value}{backup_suffix}"
                    part_to_separate = part_to_separate[:-len(value)]
                    backup_suffix, part_to_separate = NameStructureInspector.separate_suffixes_recurcive(part_to_separate, value_list, backup_suffix, start=False)
                    return backup_suffix, part_to_separate
        return backup_suffix, part_to_separate

