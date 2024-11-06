import json
import os

try:
    from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGroupBox, QComboBox, QLabel, QLineEdit, \
        QHBoxLayout, QListWidget
except ImportError:
    from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGroupBox, QComboBox, QLabel, QLineEdit, \
        QHBoxLayout, QListWidget

from renameThemAll.renamer_logics import RenamerLogics
from renameThemAll.lexicon_logics import LexiconLogics
from renameThemAll.constants import DEFAULT_COLORS


class LexiconUI(QWidget):
    """
    A widget for managing lexicons.

    This class provides a user interface for creating, editing, and managing lexicons.
    It includes functionality for adding words to lexicons, creating new lexicons,
    and removing words or entire lexicons.

    Attributes
    ----------
    BUTTON_WIDTH : int
        The width of buttons in the UI.
    WIDGET_HEIGHT : int
        The height of widgets in the UI.

    Parameters
    ----------
    tree_widget : QWidget
        The tree widget associated with this lexicon UI.
    """

    BUTTON_WIDTH = 30
    WIDGET_HEIGHT = 20

    def __init__(self, tree_widget: QWidget, combo_lexicon: QComboBox):
        """
        Initialize the LexiconUI.

        Parameters
        ----------
        tree_widget : QWidget
            The tree widget associated with this lexicon UI.
        combo_lexicon : QComboBox
            The combo box associated with this lexicon UI.
        """
        super().__init__()
        self.tree_widget = tree_widget

        '''self.setMinimumWidth(220)
        self.setMinimumHeight(500)'''

        self.selected_text = ""
        self.main_layout = QVBoxLayout()
        self.combo_lexicon = combo_lexicon

        self.create_lexicon_database()

        self.create_widget_lexicon()
        self.create_layout_lexicon()

        self.create_widget_edit_word()
        self.create_layout_edit_word()

        self.create_widget_edit_lexicon()
        self.create_layout_edit_lexicon()

        self.create_connections()
        

    def create_widget_lexicon(self) -> None:
        """
        Create widgets for the main lexicon section.

        This method initializes the widgets used in the main lexicon section,
        including the lexicon selection combo box, group and mesh lists,
        and rename functionality.
        """
        no_name_selected = f"<span style='color: {DEFAULT_COLORS['to_check']};'>no name selected</span>"
        self.lbl_select_lexicon = QLabel("Select Lexicon: ")
        LexiconLogics.load_lexicon_names(self.combo_lexicon)
        self.lbl_groups = QLabel("Groups")
        self.list_groups = QListWidget()
        self.list_groups.setMinimumHeight(300)
        self.lbl_meshes = QLabel("Meshes")
        self.list_meshes = QListWidget()
        self.list_meshes.setMinimumHeight(300)
        LexiconLogics.load_lexicon_words(self.tree_widget, self.list_groups, self.list_meshes, self.combo_lexicon)

        self.lbl_rename_groups = QLabel("Rename selection(s) with")
        self.lbl_name_selected = QLabel(no_name_selected)
        self.btn_rename = QPushButton("OK")
        self.btn_rename.setStyleSheet(
            f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")

    def create_layout_lexicon(self) -> None:
        """
        Create the layout for the main lexicon section.

        This method sets up the layout for the main lexicon section,
        organizing the widgets created in create_widget_lexicon.
        """
        self.lexicon_layout = QVBoxLayout()
        self.hbox_select_lexicon = QHBoxLayout()
        self.hbox_select_lexicon.addStretch()
        self.hbox_select_lexicon.addWidget(self.lbl_select_lexicon)
        self.hbox_select_lexicon.addWidget(self.combo_lexicon)

        self.hbox_trees = QHBoxLayout()
        self.vbox_groups = QVBoxLayout()
        self.vbox_groups.addWidget(self.lbl_groups)
        self.vbox_groups.addWidget(self.list_groups)
        self.vbox_meshes = QVBoxLayout()
        self.vbox_meshes.addWidget(self.lbl_meshes)
        self.vbox_meshes.addWidget(self.list_meshes)
        self.hbox_trees.addLayout(self.vbox_groups)
        self.hbox_trees.addLayout(self.vbox_meshes)

        self.hbox_rename = QHBoxLayout()
        self.hbox_rename.addStretch()
        self.hbox_rename.addWidget(self.lbl_rename_groups)
        self.hbox_rename.addWidget(self.lbl_name_selected)
        self.hbox_rename.addWidget(self.btn_rename)

        self.lexicon_layout.addLayout(self.hbox_select_lexicon)
        self.lexicon_layout.addLayout(self.hbox_trees)
        self.lexicon_layout.addLayout(self.hbox_rename)

        self.gbox_lexicon = QGroupBox("Lexicon")
        self.gbox_lexicon.setLayout(self.lexicon_layout)

        self.main_layout.addWidget(self.gbox_lexicon)
        self.setLayout(self.main_layout)

    def create_widget_edit_word(self) -> None:
        """
        Create widgets for editing lexicons.

        This method initializes the widgets used for editing lexicons,
        including adding words, adding yellow words, and creating new lexicons.
        """
        type = ["group", "mesh"]
        self.lbl_add = QLabel("Add")
        self.entry_add = QLineEdit()
        self.lbl_to = QLabel("to")
        self.combo_type = QComboBox()
        self.combo_type.addItems(type)
        self.btn_add_from_entry = QPushButton("OK")
        self.btn_add_from_entry.setStyleSheet(
            f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")

        self.lbl_add_yellow = QLabel("Add Yellow words to lexicon")
        self.btn_add_yellow = QPushButton("OK")
        self.btn_add_yellow.setStyleSheet(
            f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")

        self.lbl_remove_words = QLabel("Remove selected word")
        self.btn_remove_words = QPushButton("OK")
        self.btn_remove_words.setStyleSheet(
            f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")

        '''self.lbl_replace_words = QLabel("Replace words with")
        self.entry_replace_words = QLineEdit()
        self.btn_replace_words = QPushButton("OK")
        self.btn_replace_words.setStyleSheet(
            f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")'''

    def create_layout_edit_word(self) -> None:
        """
        Create the layout for editing lexicons.

        This method sets up the layout for the lexicon editing section,
        organizing the widgets created in create_widget_edit_lexicon.
        """
        self.word_edit_layout = QVBoxLayout()

        self.hbox_add = QHBoxLayout()
        self.hbox_add.addStretch()
        self.hbox_add.addWidget(self.lbl_add)
        self.hbox_add.addWidget(self.entry_add)
        self.hbox_add.addWidget(self.lbl_to)
        self.hbox_add.addWidget(self.combo_type)
        self.hbox_add.addWidget(self.btn_add_from_entry)

        self.hbox_add_yellow = QHBoxLayout()
        self.hbox_add_yellow.addStretch()
        self.hbox_add_yellow.addWidget(self.lbl_add_yellow)
        self.hbox_add_yellow.addWidget(self.btn_add_yellow)

        self.hbox_remove_words = QHBoxLayout()
        self.hbox_remove_words.addStretch()
        self.hbox_remove_words.addWidget(self.lbl_remove_words)
        self.hbox_remove_words.addWidget(self.btn_remove_words)

        '''self.hbox_replace_words = QHBoxLayout()
        self.hbox_replace_words.addStretch()
        self.hbox_replace_words.addWidget(self.lbl_replace_words)
        self.hbox_replace_words.addWidget(self.entry_replace_words)
        self.hbox_replace_words.addWidget(self.btn_replace_words)'''

        self.word_edit_layout.addLayout(self.hbox_add)
        self.word_edit_layout.addLayout(self.hbox_add_yellow)
        self.word_edit_layout.addLayout(self.hbox_remove_words)
        '''self.word_edit_layout.addLayout(self.hbox_replace_words)'''

        self.gbox_edit = QGroupBox("Edit words")
        self.gbox_edit.setLayout(self.word_edit_layout)

        self.main_layout.addWidget(self.gbox_edit)
        self.setLayout(self.main_layout)

    def create_widget_edit_lexicon(self) -> None:
        """
        Create widgets for creating lexicons.

        This method initializes the widgets used for creating lexicons,
        removing words, and replacing words in the lexicon.
        """
        self.lbl_create_lexicon = QLabel("Create a new lexicon")
        self.entry_create_lexicon = QLineEdit()
        self.btn_create_lexicon = QPushButton("OK")
        self.btn_create_lexicon.setStyleSheet(
            f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")

        self.lbl_remove_lexicon = QLabel("Remove selected lexicon")
        self.btn_remove_lexicon = QPushButton("OK")
        self.btn_remove_lexicon.setStyleSheet(
            f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")

    def create_layout_edit_lexicon(self) -> None:
        """
        Create the layout for removing lexicons and words.

        This method sets up the layout for the lexicon and word removal section,
        organizing the widgets created in create_widget_edit_lexicon.
        """
        self.lexicon_edit_layout = QVBoxLayout()
        self.hbox_create_lexicon = QHBoxLayout()
        self.hbox_create_lexicon.addStretch()
        self.hbox_create_lexicon.addWidget(self.lbl_create_lexicon)
        self.hbox_create_lexicon.addWidget(self.entry_create_lexicon)
        self.hbox_create_lexicon.addWidget(self.btn_create_lexicon)

        self.hbox_remove_lexicon = QHBoxLayout()
        self.hbox_remove_lexicon.addStretch()
        self.hbox_remove_lexicon.addWidget(self.lbl_remove_lexicon)
        self.hbox_remove_lexicon.addWidget(self.btn_remove_lexicon)

        self.lexicon_edit_layout.addLayout(self.hbox_create_lexicon)
        self.lexicon_edit_layout.addLayout(self.hbox_remove_lexicon)

        self.gbox_edit = QGroupBox("Edit lexicon")
        self.gbox_edit.setLayout(self.lexicon_edit_layout)

        self.main_layout.addWidget(self.gbox_edit)
        self.setLayout(self.main_layout)

    def create_connections(self) -> None:
        """
        Create signal-slot connections for the UI elements.

        This method sets up the connections between UI elements and their
        corresponding functions in the LexiconLogics and RenamerLogics classes.
        """

        
        self.combo_lexicon.currentTextChanged.connect(
            lambda: LexiconLogics.load_lexicon_words(self.tree_widget, self.list_groups, self.list_meshes,
                                                     self.combo_lexicon))
        self.list_groups.itemClicked.connect(
            lambda item: LexiconLogics.switch_tree_item_selection(self.list_groups, self.list_meshes,
                                                                  self.lbl_name_selected, item.text(), True))
        self.list_meshes.itemClicked.connect(
            lambda item: LexiconLogics.switch_tree_item_selection(self.list_groups, self.list_meshes,
                                                                  self.lbl_name_selected, item.text(), False))
        self.list_groups.itemClicked.connect(lambda item: self.get_selected_text(item))
        self.list_meshes.itemClicked.connect(lambda item: self.get_selected_text(item))
        self.btn_rename.clicked.connect(
            lambda: RenamerLogics.set_name_with_short_name(self.tree_widget, self.selected_text))
        self.btn_add_from_entry.clicked.connect(
            lambda: LexiconLogics.add_word_to_lexicon(self.tree_widget, self.combo_lexicon, self.list_groups,
                                                      self.list_meshes, self.entry_add, self.combo_type.currentText()))
        self.btn_add_from_entry.clicked.connect(lambda: LexiconLogics.clear_entry_field(self.entry_add))
        self.btn_add_yellow.clicked.connect(
            lambda: LexiconLogics.add_yellow_words_to_lexicon(self.tree_widget, self.list_groups, self.list_meshes,
                                                              self.combo_lexicon))
        self.btn_create_lexicon.clicked.connect(
            lambda: LexiconLogics.create_new_lexicon(self.combo_lexicon, self.entry_create_lexicon))
        self.btn_create_lexicon.clicked.connect(lambda: LexiconLogics.clear_entry_field(self.entry_create_lexicon))
        self.btn_remove_lexicon.clicked.connect(lambda: LexiconLogics.remove_lexicon(self.combo_lexicon))
        self.btn_remove_words.clicked.connect(
            lambda: LexiconLogics.remove_word_from_lexicon(self.tree_widget, self.list_groups, self.list_meshes,
                                                           self.combo_lexicon, self.lbl_name_selected))
        #self.btn_replace_words.clicked.connect(
        #    lambda: LexiconLogics.replace_word(self.tree_widget, self.list_groups, self.list_meshes, self.combo_lexicon,
        #                                       self.entry_replace_words, self.lbl_name_selected))
        #self.btn_replace_words.clicked.connect(lambda: LexiconLogics.clear_entry_field(self.entry_replace_words))

    

    def get_selected_text(self, item) -> None:
        """
        Get the text of the selected item.

        Parameters
        ----------
        item : QListWidgetItem
            The selected item in the list widget.
        """
        self.selected_text = item.text()

    def get_current_lexicon(self) -> str:
        """
        Get the current lexicon.

        Returns
        -------
        str
            The current lexicon.
        """
        return self.combo_lexicon.currentText()

    def create_lexicon_database(self) -> None:
        """
        Create the lexicon database file if it doesn't exist.

        This method checks if the lexicon database file exists, and if not,
        creates an empty JSON file to store lexicon data.
        """
        database_path = os.path.join(os.path.dirname(__file__), "lexicon_database.json")

        if not os.path.exists(database_path):
            with open(database_path, 'w') as f:
                json.dump({}, f)
            print(f"The 'lexicon_database.json' file has been created in the directory: {os.path.dirname(__file__)}")
