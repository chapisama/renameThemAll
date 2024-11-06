import json
import os
from typing import Dict, Any, List

try:
    from PySide6.QtWidgets import QLineEdit, QComboBox, QCheckBox
except ImportError:
    from PySide2.QtWidgets import QLineEdit, QComboBox, QCheckBox


from renameThemAll.constants import NO_PRESET

class UserSettingsLogics:
    """
    A class to manage user settings and presets.

    This class handles loading, saving, and manipulating user settings and presets,
    including group types, mesh types, zoning, and orientation settings.

    Attributes
    ----------
    settings_file : str
        The path to the user settings JSON file.
    settings : Dict[str, Any]
        The loaded user settings.

    Methods
    -------
    create_settings_file()
        Creates the user settings file if it doesn't exist.
    load_settings()
        Loads user settings from the JSON file.
    save_settings()
        Saves the current settings to the JSON file.
    get_preset_names()
        Returns a list of all preset names.
    get_last_preset()
        Returns the name of the last used preset.
    set_last_preset(preset_name)
        Sets the last used preset.
    create_preset(entry_new_preset, combo_presets)
        Creates a new preset and adds it to the combo box.
    save_preset(preset_name, group_types_dict, mesh_types_dict, zoning_dict, orientation_dict)
        Saves a preset with the given settings.
    load_group_types(entry_group_types, preset_name)
        Loads group types into a QLineEdit widget.
    load_mesh_types(entry_mesh_types, preset_name)
        Loads mesh types into a QLineEdit widget.
    get_user_group_types()
        Returns the group types for the current preset.
    get_user_mesh_types()
        Returns the mesh types for the current preset.
    get_user_zoning()
        Returns the zoning settings for the current preset.
    get_user_orientation()
        Returns the orientation settings for the current preset.
    """

    def __init__(self):
        """
        Initialize the UserSettingsLogics class.

        This method sets up the settings file path, creates the file if it doesn't exist,
        and loads the settings.
        """
        try:
            self.settings_file = os.path.join(os.path.dirname(__file__), 'user_settings.json')
            self.create_settings_file()
            self.settings = self.load_settings()
        except Exception as e:
            raise RuntimeError(f"Error in __init__: {str(e)}")

    def create_settings_file(self):
        """
        Create the settings file if it doesn't exist.

        Raises
        ------
        RuntimeError
            If there's an error creating the settings file.
        """
        try:
            if not os.path.exists(self.settings_file):
                with open(self.settings_file, 'w', encoding='utf-8') as f:
                    json.dump({"last_preset": NO_PRESET, "presets": {}}, f, indent=4, ensure_ascii=False)
                print(f"The 'user_settings.json' file has been created in the directory: {os.path.dirname(__file__)}")
        except Exception as e:
            raise RuntimeError(f"Error in create_settings_file: {str(e)}")

    def load_settings(self):
        """
        Load settings from the JSON file.

        Returns
        -------
        Dict[str, Any]
            The loaded settings.

        Raises
        ------
        RuntimeError
            If there's an error loading the settings.
        """
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"The file {self.settings_file} was not found. Creating a new file.")
            self.create_settings_file()
            return {"last_preset": NO_PRESET, "presets": {}}
        except json.JSONDecodeError:
            print(f"JSON decoding error in {self.settings_file}. Creating a new file.")
            self.create_settings_file()
            return {"last_preset": NO_PRESET, "presets": {}}
        except Exception as e:
            raise RuntimeError(f"Error in load_settings: {str(e)}")

    def save_settings(self):
        """
        Save the current settings to the JSON file.

        Raises
        ------
        RuntimeError
            If there's an error saving the settings.
        """
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Error in save_settings: {str(e)}")
        
    def delete_preset(self, combo_presets: QComboBox) -> None:
        """
        Delete a preset.
        """
        try:
            preset_name = combo_presets.currentText()
            combo_presets.removeItem(combo_presets.currentIndex())
            del self.settings['presets'][preset_name]
            self.save_settings()
        except Exception as e:
            raise RuntimeError(f"Error in delete_preset: {str(e)}")

    def get_preset_names(self) -> List[str]:
        """
        Get a list of all preset names.

        Returns
        -------
        List[str]
            A list of all preset names.

        Raises
        ------
        RuntimeError
            If there's an error getting the preset names.
        """
        try:
            return list(self.settings.get('presets', {}).keys())
        except Exception as e:
            raise RuntimeError(f"Error in get_preset_names: {str(e)}")
    
    def get_last_preset(self) -> str:
        """
        Get the name of the last used preset.

        Returns
        -------
        str
            The name of the last used preset.

        Raises
        ------
        RuntimeError
            If there's an error getting the last preset.
        """
        try:
            return self.settings.get('last_preset', NO_PRESET)
        except Exception as e:
            raise RuntimeError(f"Error in get_last_preset: {str(e)}")

    def set_last_preset(self, preset_name: str) -> None:
        """
        Set the last used preset.

        Parameters
        ----------
        preset_name : str
            The name of the preset to set as the last used.

        Raises
        ------
        RuntimeError
            If there's an error setting the last preset.
        """
        try:
            self.settings['last_preset'] = preset_name
            self.save_settings()
        except Exception as e:
            raise RuntimeError(f"Error in set_last_preset: {str(e)}")

    def create_preset(self, entry_new_preset: str, combo_presets: QComboBox) -> None:
        """
        Create a new preset and add it to the combo box.

        Parameters
        ----------
        entry_new_preset : str
            The name of the new preset.
        combo_presets : QComboBox
            The combo box to add the new preset to.

        Raises
        ------
        RuntimeError
            If there's an error creating the preset.
        """
        try:
            if not entry_new_preset:
                print("No preset name provided.")
                return
            
            self.settings['last_preset'] = entry_new_preset
            
            if entry_new_preset not in self.settings.get('presets', {}):
                self.settings.setdefault('presets', {})[entry_new_preset] = {
                    "structure": "",
                    "main_group": "",
                    "group_types": {},
                    "mesh_types": {},
                    "zoning": {},
                    "orientation": {},
                    "symmetry": {},
                    "checkbox_entries": {"type": False, "zoning": True, "orientation": True, "symmetry": True},
                    "n_inc_lenght": 3
                }
            
            self.save_settings()
            
            combo_presets.addItem(entry_new_preset)
            combo_presets.setCurrentText(entry_new_preset)
        except Exception as e:
            raise RuntimeError(f"Error in create_preset: {str(e)}")

    def save_preset(self, preset_name: str, structure: str, main_group: str, group_types_dict: Dict[str, Any], mesh_types_dict: Dict[str, Any], zoning_dict: Dict[str, Any], orientation_dict: Dict[str, Any], symmetry_dict: Dict[str, Any], checkbox_entries_dict: Dict[str, Any], n_inc_lenght: int) -> None:
        """
        Save a preset with the given settings.

        Parameters
        ----------
        preset_name : str
            The name of the preset to save.
        main_group : str
            The main group to save.
        structure : str
            The structure to save.
        group_types_dict : Dict[str, Any]
            The group types to save.
        mesh_types_dict : Dict[str, Any]
            The mesh types to save.
        zoning_dict : Dict[str, Any]
            The zoning settings to save.
        orientation_dict : Dict[str, Any]
            The orientation settings to save.
        symmetry_dict : Dict[str, Any]
            The symmetry settings to save.
        checkbox_entries_dict : Dict[str, Any]
            The checkbox entries to save.
        n_inc_lenght : int
            The numerical increment length to save.

        Raises
        ------
        RuntimeError
            If there's an error saving the preset.
        """
        try:
            self.settings['last_preset'] = preset_name
            
            self.settings.setdefault('presets', {})[preset_name] = {
                "structure": structure,
                "main_group": main_group,
                "group_types": group_types_dict,
                "mesh_types": mesh_types_dict,
                "zoning": zoning_dict,
                "orientation": orientation_dict,
                "symmetry": symmetry_dict,
                "checkbox_entries": checkbox_entries_dict,
                "n_inc_lenght": n_inc_lenght
            }
            self.save_settings()
        except Exception as e:
            raise RuntimeError(f"Error in save_preset: {str(e)}")
        
    def load_structure(self, entry_structure: QLineEdit, preset_name: str) -> None:
        """
        Load structure into a QLineEdit widget.
        """
        try:
            if preset_name in self.settings.get('presets', {}):
                structure = self.settings['presets'][preset_name].get('structure', "")
                entry_structure.setText(structure)
        except Exception as e:
            raise RuntimeError(f"Error in load_structure: {str(e)}")
        
    def load_main_group(self, entry_main_group: QLineEdit, preset_name: str) -> None:
        """
        Load main group into a QLineEdit widget.

        Parameters
        ----------
        entry_main_group : QLineEdit
            The QLineEdit widget to load the main group into.
        preset_name : str
            The name of the preset to load the main group from.

        Raises
        ------
        RuntimeError
            If there's an error loading the main group.
        """
        try:
            if preset_name in self.settings.get('presets', {}):
                main_group = self.settings['presets'][preset_name].get('main_group', "")
                entry_main_group.setText(main_group)
        except Exception as e:
            raise RuntimeError(f"Error in load_main_group: {str(e)}")
        
    def load_group_types(self, entry_group_type: QLineEdit, preset_name: str) -> None:
        """
        Load group types into a QLineEdit widget.

        Parameters
        ----------
        entry_group_types : QLineEdit
            The QLineEdit widget to load the group types into.
        preset_name : str
            The name of the preset to load the group types from.

        Raises
        ------
        RuntimeError
            If there's an error loading the group types.
        """
        try:
            if preset_name in self.settings.get('presets', {}):
                group_types_dict = self.settings['presets'][preset_name].get('group_types', {})
                group_types_list = list(group_types_dict.values())
                entry_group_type.setText(", ".join(group_types_list))
        except Exception as e:
            raise RuntimeError(f"Error in load_group_types: {str(e)}")

    def load_mesh_types(self, entry_mesh_type: QLineEdit, preset_name: str) -> None:
        """
        Load mesh types into a QLineEdit widget.

        Parameters
        ----------
        entry_mesh_types : QLineEdit
            The QLineEdit widget to load the mesh types into.
        preset_name : str
            The name of the preset to load the mesh types from.

        Raises
        ------
        RuntimeError
            If there's an error loading the mesh types.
        """
        try:
            if preset_name in self.settings.get('presets', {}):
                mesh_types_dict = self.settings['presets'][preset_name].get('mesh_types', {})
                mesh_types_list = list(mesh_types_dict.values())
                entry_mesh_type.setText(", ".join(mesh_types_list))
        except Exception as e:
            raise RuntimeError(f"Error in load_mesh_types: {str(e)}")
        
    def load_zoning(self, zoning_entries_dict: Dict[str, QLineEdit], preset_name: str) -> None:
        """
        Load zoning settings into QLineEdit widgets.

        Parameters
        ----------
        zoning_entries_dict : Dict[str, QLineEdit]
            The dictionary of QLineEdit widgets to load the zoning settings into.
        preset_name : str   
            The name of the preset to load the zoning settings from.

        Raises
        ------
        RuntimeError
            If there's an error loading the zoning settings.
        """
        try:
            if preset_name in self.settings.get('presets', {}):
                zoning_dict = self.settings['presets'][preset_name].get('zoning', {})
                for key, entry in zoning_entries_dict.items():
                    entry.setText(zoning_dict.get(key, ""))
        except Exception as e:
            raise RuntimeError(f"Error in load_zoning: {str(e)}")
        
    def load_orientation(self, orientation_entries_dict: Dict[str, QLineEdit], preset_name: str) -> None:
        """
        Load orientation settings into QLineEdit widgets.

        Parameters
        ----------
        orientation_entries_dict : Dict[str, QLineEdit]
            The dictionary of QLineEdit widgets to load the orientation settings into.
        preset_name : str
            The name of the preset to load the orientation settings from.

        Raises
        ------
        RuntimeError
            If there's an error loading the orientation settings.
        """
        try:
            if preset_name in self.settings.get('presets', {}):
                orientation_dict = self.settings['presets'][preset_name].get('orientation', {})
                for key, entry in orientation_entries_dict.items():
                    entry.setText(orientation_dict.get(key, ""))
        except Exception as e:
            raise RuntimeError(f"Error in load_orientation: {str(e)}")  

    def load_symmetry(self, symmetry_entries_dict: Dict[str, QLineEdit], preset_name: str) -> None:
        """
        Load symmetry settings into QLineEdit widgets.
        """
        try:
            if preset_name in self.settings.get('presets', {}):
                symmetry_dict = self.settings['presets'][preset_name].get('symmetry', {})
                for key, entry in symmetry_entries_dict.items():
                    entry.setText(symmetry_dict.get(key, ""))
        except Exception as e:
            raise RuntimeError(f"Error in load_symmetry: {str(e)}")
        
    def load_n_inc_lenght(self, entry_n_inc_lenght: QLineEdit, preset_name: str) -> None:
        """
        Load numerical increment length into a QLineEdit widget.
        """
        try:
            if preset_name in self.settings.get('presets', {}):
                n_inc_lenght = self.settings['presets'][preset_name].get('n_inc_lenght', None)
                entry_n_inc_lenght.setText(str(n_inc_lenght))
        except Exception as e:
            raise RuntimeError(f"Error in load_n_inc_lenght: {str(e)}")
        
    def load_checkbox(self, checkbox_entries_dict: Dict[str, QCheckBox], preset_name: str) -> None:
        """
        Load checkbox entries into QCheckBox widgets.
        """
        try:
            if preset_name in self.settings.get('presets', {}):
                saved_checkbox_entries = self.settings['presets'][preset_name].get('checkbox_entries', {})
                for key, checkbox in checkbox_entries_dict.items():
                    if isinstance(checkbox, QCheckBox):  # Vérifiez que c'est bien un QCheckBox
                        value = saved_checkbox_entries.get(key)
                        checkbox.setChecked(value if value is not None else True)
                    else:
                        print(f"Warning: {key} is not a QCheckBox")
        except Exception as e:
            raise RuntimeError(f"Error in load_checkbox: {str(e)}")

    def get_user_group_types(self) -> Dict[str, Any]:
        """
        Get the group types for the current preset.

        Returns
        -------
        Dict[str, Any]
            The group types for the current preset.

        Raises
        ------
        RuntimeError
            If there's an error getting the user group types.
        """
        try:
            last_preset = self.get_last_preset()
            return self.settings.get('presets', {}).get(last_preset, {}).get('group_types', {})
        except Exception as e:
            raise RuntimeError(f"Error in get_user_group_types: {str(e)}")
    
    def get_user_mesh_types(self) -> Dict[str, Any]:
        """
        Get the mesh types for the current preset.

        Returns
        -------
        Dict[str, Any]
            The mesh types for the current preset.

        Raises
        ------
        RuntimeError
            If there's an error getting the user mesh types.
        """
        try:
            last_preset = self.get_last_preset()
            return self.settings.get('presets', {}).get(last_preset, {}).get('mesh_types', {})
        except Exception as e:
            raise RuntimeError(f"Error in get_user_mesh_types: {str(e)}")
    
    def get_user_zoning(self) -> Dict[str, Any]:
        """
        Get the zoning settings for the current preset.

        Returns
        -------
        Dict[str, Any]
            The zoning settings for the current preset.

        Raises
        ------
        RuntimeError
            If there's an error getting the user zoning settings.
        """
        try:
            last_preset = self.get_last_preset()
            return self.settings.get('presets', {}).get(last_preset, {}).get('zoning', {})
        except Exception as e:
            raise RuntimeError(f"Error in get_user_zoning: {str(e)}")
    
    def get_user_orientation(self) -> Dict[str, Any]:
        """
        Get the orientation settings for the current preset.

        Returns
        -------
        Dict[str, Any]
            The orientation settings for the current preset.

        Raises
        ------
        RuntimeError
            If there's an error getting the user orientation settings.
        """
        try:
            last_preset = self.get_last_preset()
            return self.settings.get('presets', {}).get(last_preset, {}).get('orientation', {})
        except Exception as e:
            raise RuntimeError(f"Error in get_user_orientation: {str(e)}")
        
    def get_user_symmetry(self) -> Dict[str, Any]:
        """
        Get the symmetry settings for the current preset.

        Returns
        -------
        Dict[str, Any]
            The symmetry settings for the current preset.

        Raises
        ------
        RuntimeError
            If there's an error getting the user symmetry settings.
        """
        try:
            last_preset = self.get_last_preset()
            return self.settings.get('presets', {}).get(last_preset, {}).get('symmetry', {})
        except Exception as e:
            raise RuntimeError(f"Error in get_user_symmetry: {str(e)}")
        
    def get_user_checkbox(self) -> Dict[str, Any]:
        """
        Get the checkbox entries for the current preset.

        Returns
        -------
        Dict[str, Any]
            The checkbox entries for the current preset.
        """
        try:
            last_preset = self.get_last_preset()
            return self.settings.get('presets', {}).get(last_preset, {}).get('checkbox_entries', {})
        except Exception as e:
            raise RuntimeError(f"Error in get_user_checkbox: {str(e)}")


