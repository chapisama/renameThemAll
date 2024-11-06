try:
    from PySide6.QtWidgets import QDialog, QWidget, QLabel, QComboBox, QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QLineEdit, QFrame
    from PySide6.QtGui import QIntValidator
    from PySide6.QtCore import Qt
except ImportError:
    from PySide2.QtWidgets import QDialog, QWidget, QLabel, QComboBox, QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QLineEdit, QFrame
    from PySide2.QtGui import QIntValidator
    from PySide2.QtCore import Qt


from renameThemAll.renamer_logics import RenamerLogics
from renameThemAll.constants import OPTIONS_A, OPTIONS_B, ALL_TYPES_DICT, ZONING_DICT, ORIENT_DICT, INC_OPTIONS, SYMMETRY_OPTIONS, OPTIONAL_CATEGORIES, INC_NUMBER_OF_DIGITS, USED_CATEGORIES


class RenamerUI(QDialog):
    """
    A dialog for renaming items based on prefix, zoning, orientation, and increment options.

    This class provides a user interface for renaming items in a tree widget
    using various options such as prefixes, zoning, orientation, and increments.

    Attributes
    ----------
    tree_widget : QWidget
        The tree widget to be used for renaming.
    zoning : str
        The current zoning option selected.
    orient : str
        The current orientation option selected.
    BUTTON_WIDTH : int
        The width of buttons in the UI.
    WIDGET_HEIGHT : int
        The height of widgets in the UI.
    """

    BUTTON_WIDTH = 30
    WIDGET_HEIGHT = 20 

    def __init__(self, tree_widget: QWidget, lexicon_ui: QWidget = None, parent: QWidget = None) -> None:
        """
        Initialise le dialogue Renamer.

        Paramètres
        ----------
        tree_widget : QWidget
            Le widget d'arborescence à utiliser pour le renommage.
        lexicon_ui : QWidget, optionnel
            L'interface utilisateur du lexique. Par défaut est None.
        parent : QWidget, optionnel
            Le widget parent. Par défaut est None.
        """
        super().__init__(parent)

        self.tree_widget = tree_widget
        self.lexicon_ui = lexicon_ui

        self.setFixedWidth(360)
        self.setMinimumHeight(500)

        self.create_widget_switch()
        self.create_layout_switch()

        self.create_widget_prefix()
        self.create_layout_prefix()

        self.create_widget_zoning()
        self.create_layout_zoning()
        self.zoning = ""

        self.create_widget_orient()
        self.create_layout_orient()
        self.orient = ""

        self.create_widget_symmetry()
        self.create_layout_symmetry()
        self.symmetry = ""

        self.create_widget_increment()
        self.create_layout_increment()

        self.create_widget_short_name()
        self.create_layout_short_name()

        self.create_widget_hidden_categories()
        self.create_layout_hidden_categories()

        if self.lexicon_ui:
            self.lexicon_ui.setParent(self)
            self.lexicon_ui.hide() 

        self.create_main_layout()

        self.setLayout(self.main_layout)
        self.apply_stylesheet()
        self.create_connections()

    def create_widget_switch(self) -> None:
        """
        Create the switch widget components.

        This method initializes and configures the widgets related to switching between normal and lexicon modes.
        """
        self.lbl_normal_mode = QLabel("Normal mod")
        self.rbtn_normal_mode = QRadioButton()
        self.rbtn_lexicon_mode = QRadioButton()
        self.lbl_lexicon_mode = QLabel("Lexicon mod")

    def create_layout_switch(self) -> None:
        """
        Create the layout for the switch widgets.

        This method sets up the layout for the mode switching section.
        """
        self.switch_layout = QHBoxLayout()
        self.switch_layout.addStretch()
        self.switch_layout.addWidget(self.lbl_normal_mode)
        self.switch_layout.addWidget(self.rbtn_normal_mode)
        self.switch_layout.addWidget(self.rbtn_lexicon_mode)
        self.switch_layout.addWidget(self.lbl_lexicon_mode)
        self.switch_layout.addStretch()
        self.rbtn_normal_mode.setChecked(True)
        
        self.gbox_switch = QGroupBox()
        self.gbox_switch.setLayout(self.switch_layout)

    def create_widget_prefix(self) -> None:
        """
        Create the prefix widget components.

        This method initializes and configures the widgets related to prefix selection.
        """
        prefixes = ALL_TYPES_DICT.values()
        options = OPTIONS_A.values()
        self.lbl_assign_prefix = QLabel("Assign")

        self.combo_prefix = QComboBox(self)
        self.combo_prefix.setStyleSheet(f"width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")
        self.combo_prefix.addItems(prefixes)

        self.lbl_to_prefix = QLabel("to")

        self.combo_rename_mod_prefix = QComboBox(self)
        self.combo_rename_mod_prefix.setStyleSheet(f"height:{self.WIDGET_HEIGHT}px;")
        self.combo_rename_mod_prefix.addItems(options)

        self.btn_validate_prefix = QPushButton("OK")
        self.btn_validate_prefix.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")
        self.btn_clear_prefix = QPushButton("Clear")
        self.btn_clear_prefix.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")

    def create_layout_prefix(self) -> None:
        """
        Create the layout for the prefix widgets.

        This method sets up the layout for the prefix selection section.
        """
        if "type" in OPTIONAL_CATEGORIES:
            gbox_label = "Type (optional)"
        else:
            gbox_label = "Type"
        self.prefix_layout = QGridLayout()
        self.prefix_layout.addWidget(self.lbl_assign_prefix, 0, 0)

        prefixes_layout = QHBoxLayout() 
        prefixes_layout.addWidget(self.combo_prefix)
        prefixes_layout.addWidget(self.lbl_to_prefix)
        prefixes_layout.addWidget(self.combo_rename_mod_prefix)
        self.prefix_layout.addLayout(prefixes_layout, 0, 1)
                   
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()      
        buttons_layout.addWidget(self.btn_validate_prefix)
        buttons_layout.addWidget(self.btn_clear_prefix)
        
        self.prefix_layout.addLayout(buttons_layout, 0, 2)
        self.prefix_layout.setColumnStretch(2, 1)
        self.gbox_prefix = QGroupBox(gbox_label)
        self.gbox_prefix.setLayout(self.prefix_layout)
        
        if "type" not in USED_CATEGORIES:
            self.gbox_prefix.hide()

    def create_widget_zoning(self) -> None:
        """
        Create the zoning widget components.

        This method initializes and configures the widgets related to zoning selection.
        """
        options = OPTIONS_B.values()

        self.rbtn_lt = QRadioButton()
        self.rbtn_ct = QRadioButton()
        self.rbtn_rt = QRadioButton()

        self.lbl_lt = QLabel("Left")
        self.lbl_ct = QLabel("Center")
        self.lbl_rt = QLabel("Right")
        self.lbl_tp = QLabel("Top")
        self.lbl_md = QLabel("Middle")
        self.lbl_bt = QLabel("Bottom")

        self.lbl_ft = QLabel("Front")
        self.lbl_bk = QLabel("Back")

        self.rbtn_tp = QRadioButton()
        self.rbtn_tp_lt = QRadioButton()
        self.rbtn_tp_ct = QRadioButton()
        self.rbtn_tp_rt = QRadioButton()

        self.rbtn_md = QRadioButton()
        self.rbtn_md_lt = QRadioButton()
        self.rbtn_md_ct = QRadioButton()
        self.rbtn_md_rt = QRadioButton()

        self.rbtn_bt = QRadioButton()
        self.rbtn_bt_lt = QRadioButton()
        self.rbtn_bt_md = QRadioButton()
        self.rbtn_bt_rt = QRadioButton()

        self.rbtn_ft = QRadioButton()
        self.rbtn_ft_lt = QRadioButton()
        self.rbtn_ft_md = QRadioButton()
        self.rbtn_ft_rt = QRadioButton()

        self.rbtn_bk = QRadioButton()
        self.rbtn_bk_lt = QRadioButton()
        self.rbtn_bk_md = QRadioButton()
        self.rbtn_bk_rt = QRadioButton()

        self.button_zoning_dict = {
            ZONING_DICT.get("Left"): self.rbtn_lt,
            ZONING_DICT.get("Center"): self.rbtn_ct,
            ZONING_DICT.get("Right"): self.rbtn_rt,
            ZONING_DICT.get("Top"): self.rbtn_tp,
            ZONING_DICT.get("Top_Left"): self.rbtn_tp_lt,
            ZONING_DICT.get("Top_Center"): self.rbtn_tp_ct,
            ZONING_DICT.get("Top_Right"): self.rbtn_tp_rt,
            ZONING_DICT.get("Middle"): self.rbtn_md,
            ZONING_DICT.get("Middle_Left"): self.rbtn_md_lt,
            ZONING_DICT.get("Middle_Center"): self.rbtn_md_ct,
            ZONING_DICT.get("Middle_Right"): self.rbtn_md_rt,
            ZONING_DICT.get("Bottom"): self.rbtn_bt,
            ZONING_DICT.get("Bottom_Left"): self.rbtn_bt_lt,
            ZONING_DICT.get("Bottom_Center"): self.rbtn_bt_md,
            ZONING_DICT.get("Bottom_Right"): self.rbtn_bt_rt,
            ZONING_DICT.get("Front"): self.rbtn_ft,
            ZONING_DICT.get("Front_Left"): self.rbtn_ft_lt,
            ZONING_DICT.get("Front_Center"): self.rbtn_ft_md,
            ZONING_DICT.get("Front_Right"): self.rbtn_ft_rt,
            ZONING_DICT.get("Back"): self.rbtn_bk,
            ZONING_DICT.get("Back_Left"): self.rbtn_bk_lt,
            ZONING_DICT.get("Back_Center"): self.rbtn_bk_md,
            ZONING_DICT.get("Back_Right"): self.rbtn_bk_rt
        }

        self.lbl_assign_zoning = QLabel("Assign zoning to")

        self.combo_rename_mod_zoning = QComboBox(self)
        self.combo_rename_mod_zoning.setStyleSheet(f"height:{self.WIDGET_HEIGHT}px;")
        self.combo_rename_mod_zoning.addItems(options)

        self.btn_validate_zoning = QPushButton("OK")
        self.btn_validate_zoning.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")
        self.btn_clear_zoning = QPushButton("Clear")
        self.btn_clear_zoning.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")
        

    def create_layout_zoning(self) -> None:
        """
        Create the layout for the zoning widgets.

        This method sets up the layout for the zoning selection section.
        """
        if "zoning" in OPTIONAL_CATEGORIES:
            gbox_label = "Zoning (optional)"
        else:
            gbox_label = "Zoning"
        self.vbox_main_zoning_layout = QVBoxLayout()
        self.hbox_grid_zoning = QHBoxLayout()
        self.zoning_grid_layout = QGridLayout()

        self.zoning_grid_layout.addWidget(self.lbl_lt, 0, 2, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.lbl_ct, 0, 3, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.lbl_rt, 0, 4, alignment=Qt.AlignCenter)

        self.zoning_grid_layout.addWidget(self.rbtn_lt, 1, 2, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_ct, 1, 3, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_rt, 1, 4, alignment=Qt.AlignCenter)

        self.zoning_grid_layout.addWidget(self.lbl_tp, 2, 0, alignment=Qt.AlignRight)
        self.zoning_grid_layout.addWidget(self.rbtn_tp, 2, 1, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_tp_lt, 2, 2, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_tp_ct, 2, 3, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_tp_rt, 2, 4, alignment=Qt.AlignCenter)

        self.zoning_grid_layout.addWidget(self.lbl_md, 3, 0, alignment=Qt.AlignRight)
        self.zoning_grid_layout.addWidget(self.rbtn_md, 3, 1, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_md_lt, 3, 2, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_md_ct, 3, 3, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_md_rt, 3, 4, alignment=Qt.AlignCenter)

        self.zoning_grid_layout.addWidget(self.lbl_bt, 4, 0, alignment=Qt.AlignRight)
        self.zoning_grid_layout.addWidget(self.rbtn_bt, 4, 1, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_bt_lt, 4, 2, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_bt_md, 4, 3, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_bt_rt, 4, 4, alignment=Qt.AlignCenter)

        self.zoning_grid_layout.addWidget(self.lbl_ft, 5, 0, alignment=Qt.AlignRight)
        self.zoning_grid_layout.addWidget(self.rbtn_ft, 5, 1, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_ft_lt, 5, 2, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_ft_md, 5, 3, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_ft_rt, 5, 4, alignment=Qt.AlignCenter)

        self.zoning_grid_layout.addWidget(self.lbl_bk, 6, 0, alignment=Qt.AlignRight)
        self.zoning_grid_layout.addWidget(self.rbtn_bk, 6, 1, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_bk_lt, 6, 2, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_bk_md, 6, 3, alignment=Qt.AlignCenter)
        self.zoning_grid_layout.addWidget(self.rbtn_bk_rt, 6, 4, alignment=Qt.AlignCenter)

        for col in range(self.zoning_grid_layout.columnCount()):
            self.zoning_grid_layout.setColumnMinimumWidth(col, 30)
        for row in range(self.zoning_grid_layout.rowCount()):
            self.zoning_grid_layout.setRowMinimumHeight(row, 17)

        self.grid_confirm_zoning = QGridLayout()
        self.grid_confirm_zoning.addWidget(self.lbl_assign_zoning, 0, 0)
        self.grid_confirm_zoning.addWidget(self.combo_rename_mod_zoning, 0, 1)
        zoning_buttons_layout = QHBoxLayout()
        zoning_buttons_layout.addStretch()
        zoning_buttons_layout.addWidget(self.btn_validate_zoning)
        zoning_buttons_layout.addWidget(self.btn_clear_zoning)
        self.grid_confirm_zoning.addLayout(zoning_buttons_layout, 0, 2)
        self.grid_confirm_zoning.setColumnStretch(2, 1)

        self.hbox_grid_zoning.addStretch()
        self.hbox_grid_zoning.addLayout(self.zoning_grid_layout)
        self.hbox_grid_zoning.addStretch()
        self.vbox_main_zoning_layout.addLayout(self.hbox_grid_zoning)
        self.vbox_main_zoning_layout.addLayout(self.grid_confirm_zoning)

        self.gbox_zoning = QGroupBox(gbox_label)
        self.gbox_zoning.setLayout(self.vbox_main_zoning_layout)
        
        if "zoning" not in USED_CATEGORIES:
            self.gbox_zoning.hide()

    def create_widget_orient(self) -> None:
        """
        Create the orientation widget components.

        This method initializes and configures the widgets related to orientation selection.
        """
        options = OPTIONS_B.values()

        self.rbtn_nt = QRadioButton()
        self.rbtn_st = QRadioButton()

        self.lbl_nt = QLabel("North")
        self.lbl_st = QLabel("South")
        self.lbl_et = QLabel("East")
        self.lbl_wt = QLabel("West")

        self.rbtn_et = QRadioButton()
        self.rbtn_nt_et = QRadioButton()
        self.rbtn_st_et = QRadioButton()

        self.rbtn_wt = QRadioButton()
        self.rbtn_nt_wt = QRadioButton()
        self.rbtn_st_wt = QRadioButton()
        
        self.button_orient_dict = {
            ORIENT_DICT.get("North"): self.rbtn_nt,
            ORIENT_DICT.get("South"): self.rbtn_st,
            ORIENT_DICT.get("West"): self.rbtn_wt,
            ORIENT_DICT.get("East"): self.rbtn_et,
            ORIENT_DICT.get("North_East"): self.rbtn_nt_et,
            ORIENT_DICT.get("North_West"): self.rbtn_nt_wt,
            ORIENT_DICT.get("South_East"): self.rbtn_st_et,
            ORIENT_DICT.get("South_West"): self.rbtn_st_wt,
        }
        
        self.lbl_assign_orient = QLabel("Assign orient to")

        self.combo_rename_mod_orient = QComboBox(self)
        self.combo_rename_mod_orient.setStyleSheet(f"height:{self.WIDGET_HEIGHT}px;")
        self.combo_rename_mod_orient.addItems(options)

        self.btn_validate_orient = QPushButton("OK")
        self.btn_validate_orient.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")
        self.btn_clear_orient = QPushButton("Clear")
        self.btn_clear_orient.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")
        

    def create_layout_orient(self) -> None:
        """
        Create the layout for the orientation widgets.

        This method sets up the layout for the orientation selection section.
        """
        if "orientation" in OPTIONAL_CATEGORIES:
            gbox_label = "Orientation (optional)"
        else:
            gbox_label = "Orientation"
        self.vbox_main_orient_layout = QVBoxLayout()
        self.hbox_grid_orient = QHBoxLayout()
        self.orient_grid_layout = QGridLayout()

        self.orient_grid_layout.addWidget(self.lbl_nt, 0, 2, alignment=Qt.AlignCenter)

        self.orient_grid_layout.addWidget(self.rbtn_nt_wt, 1, 1, alignment=Qt.AlignCenter)
        self.orient_grid_layout.addWidget(self.rbtn_nt, 1, 2, alignment=Qt.AlignCenter)
        self.orient_grid_layout.addWidget(self.rbtn_nt_et, 1, 3, alignment=Qt.AlignCenter)

        self.orient_grid_layout.addWidget(self.lbl_wt, 2, 0, alignment=Qt.AlignRight)
        self.orient_grid_layout.addWidget(self.rbtn_wt, 2, 1, alignment=Qt.AlignCenter)
        self.orient_grid_layout.addWidget(self.rbtn_et, 2, 3, alignment=Qt.AlignCenter)
        self.orient_grid_layout.addWidget(self.lbl_et, 2, 4, alignment=Qt.AlignLeft)

        self.orient_grid_layout.addWidget(self.rbtn_st_wt, 3, 1, alignment=Qt.AlignCenter)
        self.orient_grid_layout.addWidget(self.rbtn_st, 3, 2, alignment=Qt.AlignCenter)
        self.orient_grid_layout.addWidget(self.rbtn_st_et, 3, 3, alignment=Qt.AlignCenter)

        self.orient_grid_layout.addWidget(self.lbl_st, 4, 2, alignment=Qt.AlignCenter)

        for col in range(self.orient_grid_layout.columnCount()):
            self.orient_grid_layout.setColumnMinimumWidth(col, 10)
        for row in range(self.orient_grid_layout.rowCount()):
            self.orient_grid_layout.setRowMinimumHeight(row, 17)

        self.hbox_grid_orient.addStretch()
        self.hbox_grid_orient.addLayout(self.orient_grid_layout)
        self.hbox_grid_orient.addStretch()

        self.grid_confirm_orient = QGridLayout()
        self.grid_confirm_orient.addWidget(self.lbl_assign_orient, 0, 0)
        self.grid_confirm_orient.addWidget(self.combo_rename_mod_orient, 0, 1)
        orient_buttons_layout = QHBoxLayout()
        orient_buttons_layout.addStretch()
        orient_buttons_layout.addWidget(self.btn_validate_orient)
        orient_buttons_layout.addWidget(self.btn_clear_orient)
        self.grid_confirm_orient.addLayout(orient_buttons_layout, 0, 2)
        self.grid_confirm_orient.setColumnStretch(2, 1)

        self.vbox_main_orient_layout.addLayout(self.hbox_grid_orient)
        self.vbox_main_orient_layout.addLayout(self.grid_confirm_orient)

        self.gbox_orient = QGroupBox(gbox_label)
        self.gbox_orient.setLayout(self.vbox_main_orient_layout)
        
        if "orientation" not in USED_CATEGORIES:
            self.gbox_orient.hide()

    def create_widget_symmetry(self) -> None:
        """
        Create the symmetry widget components.
        """
        options = OPTIONS_B.values() 
        self.symmetry_option = SYMMETRY_OPTIONS.get("Left")

        self.lbl_symmetry_left = QLabel("Left")
        self.rbtn_symmetry_left = QRadioButton()
        self.lbl_symmetry_right = QLabel("Right")
        self.rbtn_symmetry_right = QRadioButton()

        self.symmetry_option_dict = {
            SYMMETRY_OPTIONS.get("Left"): self.rbtn_symmetry_left,
            SYMMETRY_OPTIONS.get("Right"): self.rbtn_symmetry_right,
        }
        self.lbl_assign_symmetry = QLabel(f"Assign {self.symmetry_option} to")
        self.combo_rename_mod_symmetry = QComboBox(self)
        self.combo_rename_mod_symmetry.setStyleSheet(f"height:{self.WIDGET_HEIGHT}px;")
        self.combo_rename_mod_symmetry.addItems(options)
        self.btn_validate_symmetry = QPushButton("OK")
        self.btn_validate_symmetry.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")
        self.btn_clear_symmetry = QPushButton("Clear")
        self.btn_clear_symmetry.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")

    def create_layout_symmetry(self) -> None:
        """
        Create the layout for the symmetry widgets.
        """
        if "symmetry" in OPTIONAL_CATEGORIES:
            gbox_label = "Symmetry (optional)"
        else:
            gbox_label = "Symmetry"
        self.vbox_main_symmetry_layout = QVBoxLayout()
        self.hbox_grid_symmetry = QHBoxLayout()
        self.grid_symmetry_layout = QGridLayout()   
        self.grid_symmetry_layout.addWidget(self.lbl_symmetry_left, 0, 0)
        self.grid_symmetry_layout.addWidget(self.rbtn_symmetry_left, 0, 1)
        self.grid_symmetry_layout.addWidget(self.rbtn_symmetry_right, 0, 2)
        self.grid_symmetry_layout.addWidget(self.lbl_symmetry_right, 0, 3)
        

        self.hbox_grid_symmetry.addStretch()
        self.hbox_grid_symmetry.addLayout(self.grid_symmetry_layout)
        self.hbox_grid_symmetry.addStretch()

        self.grid_confirm_symmetry = QGridLayout()
        self.grid_confirm_symmetry.addWidget(self.lbl_assign_symmetry, 0, 0)
        self.grid_confirm_symmetry.addWidget(self.combo_rename_mod_symmetry, 0, 1)
        symmetry_buttons_layout = QHBoxLayout()
        symmetry_buttons_layout.addStretch()
        symmetry_buttons_layout.addWidget(self.btn_validate_symmetry)
        symmetry_buttons_layout.addWidget(self.btn_clear_symmetry)
        self.grid_confirm_symmetry.addLayout(symmetry_buttons_layout, 0, 2)
        self.grid_confirm_symmetry.setColumnStretch(2, 1)

        self.vbox_main_symmetry_layout.addLayout(self.hbox_grid_symmetry)
        self.vbox_main_symmetry_layout.addLayout(self.grid_confirm_symmetry)

        self.rbtn_symmetry_left.setChecked(True)

        self.gbox_symmetry = QGroupBox(gbox_label)
        self.gbox_symmetry.setLayout(self.vbox_main_symmetry_layout)
        
   
    def create_widget_increment(self) -> None:
        """
        Create the increment widget components.

        This method initializes and configures the widgets related to increment selection,
        including both alphabetical and numerical increments.
        """
        options = OPTIONS_B.values()
        letters = [chr(i) for i in range(65, 91)]
        default_number = f"{1:0{INC_NUMBER_OF_DIGITS}d}"
        number_of_nine = ""
        for _ in range (INC_NUMBER_OF_DIGITS):
            number_of_nine += "9"

        self.inc_option = INC_OPTIONS.get("A_TO_Z")

        self.rbtn_auto_a_inc = QRadioButton()
        self.lbl_auto_a_inc = QLabel("A to Z")

        self.rbtn_a_inc = QRadioButton()
        self.combo_a_inc = QComboBox(self)
        self.combo_a_inc.addItems(letters)
        self.combo_a_inc.setStyleSheet(f"padding: 2px 2px 2px 2px; width: 20px; height:{self.WIDGET_HEIGHT}px;")

        self.rbtn_n_inc = QRadioButton()
        self.entry_n_inc = QLineEdit(self)
        self.entry_n_inc.setStyleSheet(f"padding: 2px 2px 2px 2px; width:20px; width:40px; height:{self.WIDGET_HEIGHT}px;") 
        self.entry_n_inc.setText(default_number)    
        self.entry_n_inc.setValidator(QIntValidator())
        self.entry_n_inc.setMaxLength(INC_NUMBER_OF_DIGITS)

        self.rbtn_auto_n_inc = QRadioButton()
        self.lbl_auto_n_inc = QLabel(f"0 to {number_of_nine}")

        self.inc_options_dict = {
            INC_OPTIONS.get("A_TO_Z"): self.rbtn_auto_a_inc,
            INC_OPTIONS.get("LETTERS"): self.rbtn_a_inc,
            INC_OPTIONS.get("NUMBERS"): self.rbtn_n_inc,
            INC_OPTIONS.get("ZERO_TO_999"): self.rbtn_auto_n_inc,
        }

        self.lbl_assign_inc = QLabel(f"Assign {self.inc_option} to")

        self.combo_rename_mod_inc = QComboBox(self)
        self.combo_rename_mod_inc.setStyleSheet(f"height:{self.WIDGET_HEIGHT}px;")
        self.combo_rename_mod_inc.addItems(options)
        
        self.btn_validate_inc = QPushButton("OK")
        self.btn_validate_inc.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")
        self.btn_clear_inc = QPushButton("Clear")
        self.btn_clear_inc.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")

    def create_layout_increment(self) -> None:
        """
        Create the layout for the increment widgets.

        This method sets up the layout for both alphabetical and numerical increment sections.
        """
        if "increment" in OPTIONAL_CATEGORIES:
            gbox_label = "Increments (optional)"
        else:
            gbox_label = "Increments"
        self.vbox_main_inc_layout = QVBoxLayout()
        self.hbox_option_inc_layout = QHBoxLayout()
        self.option_inc_layout = QGridLayout()
        self.hbox_option_inc_layout.addStretch()
        self.hbox_option_inc_layout.addLayout(self.option_inc_layout)
        self.hbox_option_inc_layout.addStretch()     
        self.increment_layout = QGridLayout()
        
        if "alphabetical_inc" in USED_CATEGORIES:   
            self.option_inc_layout.addWidget(self.rbtn_auto_a_inc, 0, 0)      
            self.option_inc_layout.addWidget(self.lbl_auto_a_inc, 0, 1)
            self.option_inc_layout.addWidget(self.rbtn_a_inc, 0, 2)
            self.option_inc_layout.addWidget(self.combo_a_inc, 0, 3)
        else:
            self.rbtn_a_inc.hide()
            self.rbtn_auto_a_inc.hide()
            self.lbl_auto_a_inc.hide()
            self.combo_a_inc.hide()

        if "numerical_inc" in USED_CATEGORIES:
            self.option_inc_layout.addWidget(self.rbtn_n_inc, 0, 4)
            self.option_inc_layout.addWidget(self.entry_n_inc, 0, 5)
            self.option_inc_layout.addWidget(self.rbtn_auto_n_inc, 0, 6)
            self.option_inc_layout.addWidget(self.lbl_auto_n_inc, 0, 7)      
        else:
            self.rbtn_n_inc.hide()
            self.rbtn_auto_n_inc.hide()
            self.lbl_auto_n_inc.hide()
            self.entry_n_inc.hide()

        self.increment_layout.addWidget(self.lbl_assign_inc, 0, 0)    
        inc_widgets = QHBoxLayout()
        inc_widgets.addWidget(self.combo_rename_mod_inc)
        self.increment_layout.addLayout(inc_widgets, 0, 1)
        inc_buttons = QHBoxLayout()
        inc_buttons.addStretch()
        inc_buttons.addWidget(self.btn_validate_inc)
        inc_buttons.addWidget(self.btn_clear_inc)
        self.increment_layout.addLayout(inc_buttons, 0, 2)
        self.increment_layout.setColumnStretch(2, 1)

        self.vbox_main_inc_layout.addLayout(self.hbox_option_inc_layout)
        self.vbox_main_inc_layout.addLayout(self.increment_layout)

        self.rbtn_auto_a_inc.setChecked(True)

        self.gbox_increment = QGroupBox(gbox_label)
        self.gbox_increment.setLayout(self.vbox_main_inc_layout)


    def create_widget_short_name(self) -> None:
        """
        Create the short name widget components.

        This method initializes and configures the widgets related to short name assignment.
        """
        self.lbl_assign_short_name = QLabel("Assign")
        self.line_edit_short_name = QLineEdit()
        self.line_edit_short_name.setStyleSheet(f"padding: 2px 2px 2px 2px; width:100px; height:{self.WIDGET_HEIGHT}px;")
        self.line_edit_short_name.setPlaceholderText("name")
        self.lbl_to_short_name = QLabel("to selection(s)")
        self.btn_validate_short_name = QPushButton("OK")
        self.btn_validate_short_name.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")
        self.btn_clear_short_name = QPushButton("Clear")
        self.btn_clear_short_name.setStyleSheet(f"padding-left: 2px; padding-right: 2px; width:{self.BUTTON_WIDTH}px; height:{self.WIDGET_HEIGHT}px;")

    def create_layout_short_name(self) -> None:
        """
        Create the layout for the short name widgets.

        This method sets up the layout for the short name section, including
        labels, input fields, and buttons.

        Returns
        -------
        None
        """
        self.short_name_layout = QGridLayout()
        self.short_name_layout.addWidget(self.lbl_assign_short_name, 0, 0)
        self.short_name_layout.addWidget(self.line_edit_short_name, 0, 1)
        self.short_name_layout.addWidget(self.lbl_to_short_name, 0, 2)
        short_name_buttons = QHBoxLayout()
        short_name_buttons.addStretch()
        short_name_buttons.addWidget(self.btn_validate_short_name)
        short_name_buttons.addWidget(self.btn_clear_short_name)
        self.short_name_layout.addLayout(short_name_buttons, 0, 3)
        self.short_name_layout.setColumnStretch(3, 1)

        self.gbox_short_name = QGroupBox("Short name")
        self.gbox_short_name.setLayout(self.short_name_layout)

    def create_widget_hidden_categories(self) -> None:
        hidden_categories = ""
        if "type" not in USED_CATEGORIES:
            hidden_categories += "Type, "
        if "zoning" not in USED_CATEGORIES:
            hidden_categories += "Zoning, "
        if "orientation" not in USED_CATEGORIES:
            hidden_categories += "Orientation, "
        if "alphabetical_inc" not in USED_CATEGORIES and "numerical_inc" not in USED_CATEGORIES:
            hidden_categories += "Increments, "
        elif "alphabetical_inc" not in USED_CATEGORIES:
            hidden_categories += "Alphabetical increment, "
        elif "numerical_inc" not in USED_CATEGORIES:
            hidden_categories += "Numerical increment, "
        if "symmetry" not in USED_CATEGORIES:
            hidden_categories += "Symmetry, "

        if hidden_categories:
            hidden_categories = hidden_categories[:-2]
        
        if hidden_categories:
            self.lbl_hidden_categories = QLabel(f"Hidden options: {hidden_categories}. These options are not displayed in the outliner because they are not present in the name structure. (Config / Configuration / Create preset / Name structure)")
            self.lbl_hidden_categories.setWordWrap(True)
           

    def create_layout_hidden_categories(self) -> None:
        """
        Create the layout for the hidden categories widget.
        """
        self.gbox_hidden_categories = QGroupBox("Hidden categories")
        self.hbox_hidden_categories = QHBoxLayout()
        if hasattr(self, "lbl_hidden_categories"):
            self.hbox_hidden_categories.addWidget(self.lbl_hidden_categories)
        self.gbox_hidden_categories.setLayout(self.hbox_hidden_categories)

    def create_main_layout(self) -> None:
        """
        Create the main layout containing all widget layouts.

        This method sets up the main layout of the dialog, combining all sections
        including prefix, zoning, orientation, and increment.

        Returns
        -------
        None
        """
        self.main_layout = QVBoxLayout()
        line_A = QFrame()
        line_A.setFrameShape(QFrame.HLine)
        line_A.setFrameShadow(QFrame.Sunken)
        line_A.setLineWidth(3)
        line_A.setFixedHeight(3)
        
        layout_line_A = QVBoxLayout()
        layout_line_A.addSpacing(10)
        layout_line_A.addWidget(line_A)
        layout_line_A.addSpacing(5)

        self.main_layout.addWidget(self.gbox_switch) 
        self.main_layout.addLayout(layout_line_A)
        
        if "type" in USED_CATEGORIES:
            self.main_layout.addWidget(self.gbox_prefix)
        if "zoning" in USED_CATEGORIES:
            self.main_layout.addWidget(self.gbox_zoning)
        if "orientation" in USED_CATEGORIES:
            self.main_layout.addWidget(self.gbox_orient)
        if "symmetry" in USED_CATEGORIES:
            self.main_layout.addWidget(self.gbox_symmetry)  
        if "alphabetical_inc" in USED_CATEGORIES or "numerical_inc" in USED_CATEGORIES:
            self.main_layout.addWidget(self.gbox_increment)

        self.main_layout.addWidget(self.gbox_short_name)

        categories = ["type", "zoning", "orientation", "alphabetical_inc", "numerical_inc", "symmetry"]
        if any(category not in USED_CATEGORIES for category in categories):
            self.main_layout.addWidget(self.gbox_hidden_categories)


        self.main_layout.addWidget(self.lexicon_ui)
        self.switch_mode()
        self.main_layout.setContentsMargins(2, 10, 2, 2)
        self.main_layout.setSpacing(2)
        self.main_layout.addStretch()

    def create_connections(self) -> None:
        """
        Create signal-slot connections for widget interactions.

        This method sets up the connections between user actions and their corresponding functions
        for all sections including prefix, zoning, orientation, and increments.

        Returns
        -------
        None
        """
        self.rbtn_normal_mode.toggled.connect(self.switch_mode)

        self.btn_validate_prefix.clicked.connect(
            lambda: RenamerLogics.set_name_with_type(self.tree_widget, self.combo_prefix.currentText(),
                                                       self.combo_rename_mod_prefix.currentText()))
        self.btn_clear_prefix.clicked.connect(
            lambda: RenamerLogics.set_name_with_type(self.tree_widget, "",
                                                       self.combo_rename_mod_prefix.currentText()))
        for key, value in self.button_zoning_dict.items():
            value.toggled.connect(lambda checked, key=key: self.set_zoning(key, checked))

        self.btn_validate_zoning.clicked.connect(
            lambda: RenamerLogics.set_name_with_zoning(self.tree_widget, self.zoning,
                                                       self.combo_rename_mod_zoning.currentText()))
        self.btn_clear_zoning.clicked.connect(
            lambda: RenamerLogics.set_name_with_zoning(self.tree_widget, "",
                                                       self.combo_rename_mod_zoning.currentText()))
        for key, value in self.button_orient_dict.items():
            value.toggled.connect(lambda checked, key=key: self.set_orient(key, checked))

        self.btn_validate_orient.clicked.connect(
            lambda: RenamerLogics.set_name_with_orient(self.tree_widget, self.orient,
                                                       self.combo_rename_mod_orient.currentText()))
        self.btn_clear_orient.clicked.connect(
            lambda: RenamerLogics.set_name_with_orient(self.tree_widget, "",
                                                       self.combo_rename_mod_orient.currentText()))   
        for key, value in self.symmetry_option_dict.items():
            value.toggled.connect(lambda checked, key=key: self.set_symmetry_option(key, checked))
        self.btn_validate_symmetry.clicked.connect(
            lambda: RenamerLogics.set_name_with_symmetry(self.tree_widget, self.symmetry_option,
                                                       self.combo_rename_mod_symmetry.currentText()))
        self.btn_clear_symmetry.clicked.connect(
            lambda: RenamerLogics.set_name_with_symmetry(self.tree_widget, "",
                                                       self.combo_rename_mod_symmetry.currentText()))
        self.btn_validate_inc.clicked.connect(
            lambda: RenamerLogics.set_name_with_inc(self.tree_widget, self.combo_a_inc.currentText(), self.entry_n_inc.text(),
                                                    self.combo_rename_mod_inc.currentText(), self.inc_option))
        self.btn_clear_inc.clicked.connect(
            lambda: RenamerLogics.set_name_with_inc(self.tree_widget, "", "",
                                                    self.combo_rename_mod_inc.currentText(), self.inc_option)) 
        for key, value in self.inc_options_dict.items():
            value.toggled.connect(lambda checked, key=key: self.set_inc_option(key, checked, self.entry_n_inc.text(), self.combo_a_inc.currentText()))
            
        self.combo_a_inc.currentTextChanged.connect(lambda text: self.update_radio_a_inc_selection(text))

        self.entry_n_inc.textChanged.connect(lambda text: self.update_radio_n_inc_selection(text))

        self.btn_validate_short_name.clicked.connect(
            lambda: RenamerLogics.set_name_with_short_name(self.tree_widget, self.line_edit_short_name.text()))
        self.btn_clear_short_name.clicked.connect(
            lambda: RenamerLogics.set_name_with_short_name(self.tree_widget, ""))
        self.line_edit_short_name.returnPressed.connect(
            lambda: RenamerLogics.set_name_with_short_name(self.tree_widget, self.line_edit_short_name.text()))

    def set_zoning(self, key: str, checked: bool) -> None:
        """
        Set the zoning based on the selected radio button.

        Parameters
        ----------
        key : str
            The zoning key corresponding to the selected radio button.
        checked : bool
            Whether the radio button is checked or not.

        Returns
        -------
        None
        """
        if checked:
            self.zoning = key

    def set_orient(self, key: str, checked: bool) -> None:
        """
        Set the orientation based on the selected radio button.

        Parameters
        ----------
        key : str
            The orientation key corresponding to the selected radio button.
        checked : bool
            Whether the radio button is checked or not.

        Returns
        -------
        None
        """
        if checked:
            self.orient = key

    def update_radio_a_inc_selection(self, text: str) -> None:
        """
        Update the radio button selection based on the current text of the combo box.
        """
        self.rbtn_a_inc.setChecked(True)
        self.set_text_inc(INC_OPTIONS.get("LETTERS"), "", text)

    def update_radio_n_inc_selection(self, text: str) -> None:
        """
        Update the radio button selection based on the current text of the entry field.
        """
        self.rbtn_n_inc.setChecked(True)
        self.set_text_inc(INC_OPTIONS.get("NUMBERS"), text, "")

    def set_inc_option(self, key: str, checked: bool, n_inc: str, a_inc: str) -> None:
        """
        Set the increment based on the selected radio button.

        Parameters
        ----------
        key : str
            The increment key corresponding to the selected radio button.
        checked : bool
            Whether the radio button is checked or not. 

        Returns
        -------
        None
        """
        if checked:
            self.inc_option = key
            self.set_text_inc(key, n_inc, a_inc)

    def set_symmetry_option(self, key: str, checked: bool) -> None:
        """
        Set the symmetry option based on the selected radio button.
        """
        if checked:
            self.symmetry_option = key
            self.set_text_symmetry(key)

    def set_text_symmetry(self, key: str) -> None:
        """
        Set the text of the symmetry label.
        """
        self.lbl_assign_symmetry.setText(f"Assign {key} to")

    def set_text_inc(self, key: str, n_inc: str, a_inc: str) -> None:
        """
        Set the text of the increment entry field.

        Parameters
        ----------
        key : str
            The increment key corresponding to the selected radio button.
        n_inc : str
            The text to be set in the increment entry field.
        a_inc : str
            The text to be set in the increment entry field.
        Returns
        -------
        None
        """
        if key == INC_OPTIONS.get("A_TO_Z") or key == INC_OPTIONS.get("ZERO_TO_999"):
            self.lbl_assign_inc.setText(f"Assign {key} to")
        elif key == INC_OPTIONS.get("LETTERS"):
            self.lbl_assign_inc.setText(f"Assign {a_inc} to")
        else:
            self.lbl_assign_inc.setText(f"Assign {n_inc} to")

    def switch_mode(self) -> None:
        """
        Switch between normal and simplified mode.

        This method toggles the visibility of various UI elements based on the selected mode.

        Returns
        -------
        None
        """
        if self.rbtn_normal_mode.isChecked():
            if "type" in USED_CATEGORIES:
                self.gbox_prefix.setVisible(True)
            if "zoning" in USED_CATEGORIES:
                self.gbox_zoning.setVisible(True)
            if "orientation" in USED_CATEGORIES:
                self.gbox_orient.setVisible(True)
            if "alphabetical_inc" in USED_CATEGORIES or "numerical_inc" in USED_CATEGORIES:
                self.gbox_increment.setVisible(True)
            self.gbox_short_name.setVisible(True)
            self.gbox_hidden_categories.setVisible(True)
            if "symmetry" in USED_CATEGORIES:
                self.gbox_symmetry.setVisible(True)
            self.lexicon_ui.setVisible(False)
        else:
            if "type" in USED_CATEGORIES:
                self.gbox_prefix.setVisible(False)
            if "zoning" in USED_CATEGORIES:
                self.gbox_zoning.setVisible(False)
            if "orientation" in USED_CATEGORIES:
                self.gbox_orient.setVisible(False)
            if "alphabetical_inc" in USED_CATEGORIES or "numerical_inc" in USED_CATEGORIES:
                self.gbox_increment.setVisible(False)
            self.gbox_short_name.setVisible(False)
            self.gbox_hidden_categories.setVisible(False)
            if "symmetry" in USED_CATEGORIES:
                self.gbox_symmetry.setVisible(False)
            self.lexicon_ui.setVisible(True)

    def apply_stylesheet(self) -> None:
        """
        Apply stylesheets to widgets for consistent styling.

        This method sets up the visual appearance of the dialog and its components,
        including background colors, borders, and text colors.

        Returns
        -------
        None
        """
        stylesheet = """
        QGroupBox {
            background-color: #3e3e3e;  /* Background color */
            border: 1px solid #5e5e5e;   /* Border color and thickness */
            border-radius: 5px;        /* Optional: rounding the corners */
            margin-top: 7px;          /* Space between the title and the top border */
        }
        QGroupBox::title {
            color : white;     
            subcontrol-origin: margin;
            subcontrol-position: top left; /* position at the top left */
            padding: 0 10px;
        }
        """
        self.setStyleSheet(stylesheet)
