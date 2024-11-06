import json
import os

try:
    from PySide6.QtWidgets import QComboBox, QLabel, QListWidget, QLineEdit, QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import Qt
except ImportError:
    from PySide2.QtWidgets import QComboBox, QLabel, QListWidget, QLineEdit, QTreeWidget, QTreeWidgetItem
    from PySide2.QtCore import Qt

from renameThemAll.constants import DEFAULT_COLORS, OBJ_TYPE_DICT, NO_LEXICON
from renameThemAll.renamer_logics import RenamerLogics
from renameThemAll.name_structure_inspector import NameStructureInspector
from renameThemAll.outliner_custom_tree_widget import OutlinerCustomTreeWidget



class LexiconLogics:
    @staticmethod
    def load_lexicon_names(combo_lexicon: QComboBox) -> None:
        """
        Loads lexicon names from the database and populates the combo box.

        Parameters
        ----------
        combo_lexicon : QComboBox
            The combo box to be filled with lexicon names.

        Returns
        -------
        None
        """
        database_path = os.path.join(os.path.dirname(__file__), "lexicon_database.json")
        with open(database_path, 'r') as f:
            data = json.load(f)
        combo_lexicon.addItems(list(data.keys()))

    @staticmethod
    def load_lexicon_words(tree_widget: QTreeWidget, list_groups: QListWidget, list_meshes: QListWidget,
                           combo_lexicon: QComboBox) -> None:
        """
        Loads words from the selected lexicon into the group and mesh lists.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the elements.
        list_groups : QListWidget
            The list widget for group words.
        list_meshes : QListWidget
            The list widget for mesh words.
        combo_lexicon : QComboBox
            The combo box containing the selected lexicon.

        Returns
        -------
        None
        """
        lexicon_name = combo_lexicon.currentText()
        list_groups.clear()
        list_meshes.clear()
        if lexicon_name != NO_LEXICON:
            database_path = os.path.join(os.path.dirname(__file__), "lexicon_database.json")
            with open(database_path, 'r') as f:
                data = json.load(f)
            if lexicon_name in data:
                list_groups.addItems(data[lexicon_name]["groups"])
                list_meshes.addItems(data[lexicon_name]["meshes"])
            LexiconLogics.update_tree_items_by_lexicon(tree_widget)

    @staticmethod
    def update_tree_items_by_lexicon(tree_widget: QTreeWidget) -> None:
        """
        Updates all tree items based on the current lexicon.

        This method recursively traverses all items in the tree
        and applies lexicon-based editing to each item.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the items to be updated.

        Returns
        -------
        None
        """
        top_item = tree_widget.topLevelItem(0)
        items = []
        child_count = top_item.childCount()
        for i in range(child_count):
            child = top_item.child(i)
            RenamerLogics.get_items_recursive(child, items)
        for item in items:
            OutlinerCustomTreeWidget.start_editing_by_lexicon(tree_widget, item)

    @staticmethod
    def create_new_lexicon(combo_lexicon: QComboBox, entry_create_lexicon: QLineEdit) -> None:
        """
        Creates a new lexicon and adds it to the combo box and database.

        Parameters
        ----------
        combo_lexicon : QComboBox
            The combo box to which the new lexicon should be added.
        entry_create_lexicon : QLineEdit
            The input field containing the name of the new lexicon.

        Returns
        -------
        None
        """
        new_lexicon = entry_create_lexicon.text()
        if combo_lexicon.findText(new_lexicon) == -1:
            position = 0
            for i in range(combo_lexicon.count()):
                if new_lexicon < combo_lexicon.itemText(i):
                    break
                position += 1
            combo_lexicon.insertItem(position, new_lexicon)
            combo_lexicon.setCurrentText(new_lexicon)
            LexiconLogics.add_lexicon_to_database(new_lexicon)

    @staticmethod
    def add_lexicon_to_database(lexicon_name: str) -> None:
        """
        Adds a new lexicon to the database.

        Parameters
        ----------
        lexicon_name : str
            The name of the new lexicon to add.

        Returns
        -------
        None
        """
        database_path = os.path.join(os.path.dirname(__file__), "lexicon_database.json")
        with open(database_path, 'r') as f:
            data = json.load(f)

        position = 0
        for existing_lexicon in sorted(data.keys()):
            if lexicon_name < existing_lexicon:
                break
            position += 1

        new_data = {}
        for i, (key, value) in enumerate(data.items()):
            if i == position:
                new_data[lexicon_name] = {
                    "groups": [],
                    "meshes": []
                }
            new_data[key] = value

        if position == len(data):
            new_data[lexicon_name] = {
                "groups": [],
                "meshes": []
            }

        with open(database_path, 'w') as f:
            json.dump(new_data, f, indent=4)

    @staticmethod
    def remove_lexicon(combo_lexicon: QComboBox) -> None:
        """
        Removes the selected lexicon from the combo box and database.

        Parameters
        ----------
        combo_lexicon : QComboBox
            The combo box containing the lexicon to be removed.

        Returns
        -------
        None
        """
        lexicon_name = combo_lexicon.currentText()
        if lexicon_name:
            LexiconLogics.remove_lexicon_from_database(lexicon_name)
            combo_lexicon.removeItem(combo_lexicon.currentIndex())

    @staticmethod
    def remove_lexicon_from_database(lexicon_name: str) -> None:
        """
        Removes a lexicon from the database.

        Parameters
        ----------
        lexicon_name : str
            The name of the lexicon to remove.

        Returns
        -------
        None
        """
        database_path = os.path.join(os.path.dirname(__file__), "lexicon_database.json")
        with open(database_path, 'r') as f:
            data = json.load(f)
        if lexicon_name in data:
            del data[lexicon_name]
        with open(database_path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def add_word_to_lexicon(tree_widget: QTreeWidget, combo_lexicon: QComboBox, list_groups: QListWidget,
                            list_meshes: QListWidget, entry_add: QLineEdit, type: str) -> None:
        """
        Adds a word to the selected lexicon and updates the corresponding list.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the elements.
        combo_lexicon : QComboBox
            The combo box containing the selected lexicon.
        list_groups : QListWidget
            The list widget for group words.
        list_meshes : QListWidget
            The list widget for mesh words.
        entry_add : QLineEdit
            The input field containing the word to add.
        type : str
            The type of the word ('group' or 'mesh').

        Returns
        -------
        None
        """
        if combo_lexicon.currentText() == NO_LEXICON:
            print("No lexicon selected")
            return
        word = entry_add.text()
        if word and type:
            target_list = list_groups if type == "group" else list_meshes
            word_exists = False
            for i in range(target_list.count()):
                if target_list.item(i).text() == word:
                    word_exists = True
                    break
                
            if not word_exists:
                position = 0
                for i in range(target_list.count()):
                    if word < target_list.item(i).text():
                        break
                    position += 1
                target_list.insertItem(position, word)
                LexiconLogics.add_word_to_database(combo_lexicon.currentText(), word, type)
                LexiconLogics.update_tree_items_by_lexicon(tree_widget)
            else:
                print("The word already exists in the list")
        else:
            print("Please enter a word and select a type.")

    @staticmethod
    def add_yellow_words_to_lexicon(tree_widget: QTreeWidget, list_groups: QListWidget, list_meshes: QListWidget,
                                    combo_lexicon: QComboBox) -> None:
        """
        Adds yellow words from the tree widget to the selected lexicon.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the elements.
        list_groups : QListWidget
            The list widget for group words.
        list_meshes : QListWidget
            The list widget for mesh words.
        combo_lexicon : QComboBox
            The combo box containing the selected lexicon.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If no top-level item is found in the tree widget.
        """
        if combo_lexicon.currentText() == NO_LEXICON:
            print("No lexicon selected")
            return
        top_level_item = tree_widget.topLevelItem(0)
        if not top_level_item:
            raise ValueError("No top-level item found")
        items = []
        child_count = top_level_item.childCount()
        for i in range(child_count):
            child = top_level_item.child(i)
            RenamerLogics.get_items_recursive(child, items)
        for item in items:
            short_name = LexiconLogics.get_yellow_words_from_tree(item)
            if item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT.get("transform"):
                target_list = list_groups
                type = "group"
            elif item.data(0, Qt.UserRole)[1] == OBJ_TYPE_DICT.get("transfo_mesh"):
                target_list = list_meshes
                type = "mesh"
            else:
                continue
            if not target_list.findItems(short_name, Qt.MatchFlag.MatchExactly):
                position = 0
                for i in range(target_list.count()):
                    if short_name < target_list.item(i).text():
                        break
                    position += 1
                target_list.insertItem(position, short_name)
                LexiconLogics.add_word_to_database(combo_lexicon.currentText(), short_name, type)
        LexiconLogics.update_tree_items_by_lexicon(tree_widget)

    @staticmethod
    def add_word_to_database(lexicon_name: str, word: str, type: str) -> None:
        """
        Adds a word to the specified lexicon in the database.

        Parameters
        ----------
        lexicon_name : str
            The name of the lexicon to which the word should be added.
        word : str
            The word to add.
        type : str
            The type of the word ('group' or 'mesh').

        Returns
        -------
        None
        """
        database_path = os.path.join(os.path.dirname(__file__), "lexicon_database.json")
        with open(database_path, 'r') as f:
            data = json.load(f)
        if not lexicon_name:
            return
        if type == "group":
            data[lexicon_name]["groups"] = sorted(data[lexicon_name]["groups"] + [word])
        else:
            data[lexicon_name]["meshes"] = sorted(data[lexicon_name]["meshes"] + [word])
        with open(database_path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def remove_word_from_lexicon(tree_widget: QTreeWidget, list_groups: QListWidget, list_meshes: QListWidget,
                                 combo_lexicon: QComboBox, lbl_name_selected: QLabel) -> None:
        """
        Removes the selected word from the lexicon and updates the corresponding list.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the elements.
        list_groups : QListWidget
            The list widget for group words.
        list_meshes : QListWidget
            The list widget for mesh words.
        combo_lexicon : QComboBox
            The combo box containing the selected lexicon.
        lbl_name_selected : QLabel
            The label to display the selected name.

        Returns
        -------
        None
        """
        no_name_selected = f"<span style='color: {DEFAULT_COLORS['to_check']};'>no name selected</span>"
        if list_groups.currentItem():
            word = list_groups.currentItem().text()
            type = "group"
            list_groups.takeItem(list_groups.currentRow())
            list_groups.clearSelection()
        elif list_meshes.currentItem():
            word = list_meshes.currentItem().text()
            type = "mesh"
            list_meshes.takeItem(list_meshes.currentRow())
            list_meshes.clearSelection()
        else:
            print("No word selected")
            return
        LexiconLogics.remove_word_from_database(word, type, combo_lexicon.currentText())
        lbl_name_selected.setText(no_name_selected)
        LexiconLogics.update_tree_items_by_lexicon(tree_widget)

    @staticmethod
    def remove_word_from_database(word: str, type: str, lexicon_name: str) -> None:
        """
        Removes a word from the specified lexicon in the database.

        Parameters
        ----------
        word : str
            The word to remove.
        type : str
            The type of the word ('group' or 'mesh').
        lexicon_name : str
            The name of the lexicon from which to remove the word.

        Returns
        -------
        None
        """
        database_path = os.path.join(os.path.dirname(__file__), "lexicon_database.json")
        with open(database_path, 'r') as f:
            data = json.load(f)
        if lexicon_name in data:
            lexicon_data = data[lexicon_name]
            if type == "group":
                if word in lexicon_data["groups"]:
                    lexicon_data["groups"].remove(word)
            elif type == "mesh":
                if word in lexicon_data["meshes"]:
                    lexicon_data["meshes"].remove(word)
        with open(database_path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def replace_word(tree_widget: QTreeWidget, list_groups: QListWidget, list_meshes: QListWidget,
                     combo_lexicon: QComboBox, entry_replace_words: QLineEdit, lbl_name_selected: QLabel) -> None:
        """
        Replaces the selected word with a new word in the lexicon.

        Parameters
        ----------
        tree_widget : QTreeWidget
            The tree widget containing the elements.
        list_groups : QListWidget
            The list widget for group words.
        list_meshes : QListWidget
            The list widget for mesh words.
        combo_lexicon : QComboBox
            The combo box containing the selected lexicon.
        entry_replace_words : QLineEdit
            The input field containing the new word.
        lbl_name_selected : QLabel
            The label to display the selected name.

        Returns
        -------
        None
        """
        new_word = entry_replace_words.text()
        if not new_word:
            print("Please enter a new word")
            return

        if list_groups.currentItem():
            target_list = list_groups
            type = "group"
        elif list_meshes.currentItem():
            target_list = list_meshes
            type = "mesh"
        else:
            print("No word selected")
            return

        if not target_list.findItems(new_word, Qt.MatchFlag.MatchExactly):
            LexiconLogics.add_word_to_lexicon(tree_widget, combo_lexicon, list_groups, list_meshes, QLineEdit(new_word),
                                              type)
            LexiconLogics.remove_word_from_lexicon(tree_widget, list_groups, list_meshes, combo_lexicon,
                                                   lbl_name_selected)
            LexiconLogics.update_tree_items_by_lexicon(tree_widget)
        else:
            print("The word already exists in the list")

    @staticmethod
    def switch_tree_item_selection(list_groups: QListWidget, list_meshes: QListWidget, lbl_name_selected: QLabel,
                                   item_name: str, is_group: bool) -> None:
        """
        Selects an item in one list and deselects all items in the other list.

        Parameters
        ----------
        list_groups : QListWidget
            The list of groups.
        list_meshes : QListWidget
            The list of meshes.
        lbl_name_selected : QLabel
            The label to display the selected name.
        item_name : str
            The name of the item to select.
        is_group : bool
            True if the item is in the group list, False otherwise.

        Returns
        -------
        None
        """
        colors = DEFAULT_COLORS
        if is_group:
            list_meshes.clearSelection()
        else:
            list_groups.clearSelection()
        colored_name = f"<span style='color: {colors['valid']};'>{item_name}</span>"
        lbl_name_selected.setText(colored_name)

    @staticmethod
    def clear_entry_field(entry_field: QLineEdit) -> None:
        """
        Clears the text from the input field.

        Parameters
        ----------
        entry_field : QLineEdit
            The input field to clear.

        Returns
        -------
        None
        """
        entry_field.clear()
        entry_field.clearFocus()

    @staticmethod
    def get_yellow_words_from_tree(item: QTreeWidgetItem) -> str:
        """
        Extracts the short name (yellow words) from a tree widget item.

        Parameters
        ----------
        item : QTreeWidgetItem
            The tree widget item from which to extract the short name.

        Returns
        -------
        str
            The extracted short name.
        """
        long_name = item.data(0, Qt.UserRole)[0]
        long_name = long_name.split("|")[-1]
        name_part_dict = NameStructureInspector.inspect_name_structure(long_name)
        for index in name_part_dict:
            if "name" in name_part_dict[index] and name_part_dict[index]["name"] != "":
                return name_part_dict[index]["name"]
        return ""
