try:    
    from PySide6.QtWidgets import QPushButton, QHBoxLayout, QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFrame, QGridLayout, QSizePolicy, QMessageBox, QCheckBox, QLayout, QTextEdit, QSplitter, QWidget
    from PySide6.QtCore import Signal
except ImportError:
    from PySide2.QtWidgets import QPushButton, QHBoxLayout, QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFrame, QGridLayout, QSizePolicy, QMessageBox, QCheckBox, QLayout, QTextEdit, QSplitter, QWidget
    from PySide2.QtCore import Signal

from renameThemAll.user_settings_logics import UserSettingsLogics
from renameThemAll.default_settings import DefaultZoningSingle, DefaultOrientSingle, DefaultSymmetryOptions
from renameThemAll.constants import NO_PRESET, MANUAL_NAME_STRUCTURE, MANUAL_MAIN_GROUP, MANUAL_TYPE, MANUAL_ZONING, MANUAL_ORIENTATION, MANUAL_SYMMETRY, MANUAL_INC


class UserSettingsUI(QDialog):
    """
    A dialog for managing user settings.

    This class provides a user interface for creating, editing, and saving user presets
    for various settings related to 3D modeling and animation.

    Attributes
    ----------
    WIDTH_ENTRY_ZONING : int
        The width of zoning entry fields.
    settings_saved : Signal
        A signal emitted when settings are saved.
    restart_application : Signal
        A signal emitted when the application needs to be restarted.

    """

    WIDTH_ENTRY_ZONING = 50
    settings_saved = Signal()
    restart_application = Signal()

    def __init__(self) -> None:
        """
        Initialize the UserSettingsUI dialog.

        This method sets up the initial state of the dialog, including its title,
        size, and layout. It also loads initial settings and creates necessary widgets.
        """
        super().__init__()
        self.user_settings_logics = UserSettingsLogics()
        self.setWindowTitle("User Settings")
        self.no_preset = NO_PRESET
        self.setMinimumWidth(0)
        self.setMinimumHeight(0)  
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.adjustSize()  
        
        self.create_manual_widget()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.load_initial_settings()

    def create_widgets(self) -> None:
        """
        Create all widgets used in the dialog.

        This method initializes and creates all the UI widgets by calling specialized
        widget creation methods for each section of the interface.
        """
        self.create_preset_widgets()
        self.create_structure_widgets()
        self.create_main_group_widgets()
        self.create_type_widgets()
        self.create_zoning_widgets()
        self.create_orientation_widgets()
        self.create_symmetry_widgets()
        self.create_inc_widgets()
        self.create_save_widget()

    def create_preset_widgets(self) -> None:
        """
        Create widgets for preset management.

        Creates and initializes widgets related to preset creation and selection,
        including labels, entry fields and buttons.
        """
        self.lbl_new_preset = QLabel("Create New Preset:")
        self.entry_new_preset = QLineEdit()
        self.btn_create_preset = QPushButton("Create")

        self.lbl_presets = QLabel("Presets:")
        self.combo_presets = QComboBox()
        self.combo_presets.addItem(self.no_preset)

    def create_structure_widgets(self) -> None:
        """
        Create widgets for name structure.

        Creates and initializes widgets related to the naming structure configuration,
        including labels, entry fields and info buttons.
        """
        self.lbl_structure = QLabel("Name Structure:")
        self.entry_structure = QLineEdit()
        self.entry_structure.setPlaceholderText(r"[symmetry]_[type]_[name][zoning][orientation][alphabetical_inc]_[numerical_inc]")
        self.info_icon_structure = self.create_info_button()

    def create_main_group_widgets(self) -> None:
        """
        Create widgets for main group settings.
        """ 
        self.lbl_main_group = QLabel("Main Group:")
        self.entry_main_group = QLineEdit()
        self.entry_main_group.setPlaceholderText("ALL")
        self.info_icon_main_group = self.create_info_button()

    def create_type_widgets(self) -> None:
        """
        Create widgets for group settings.

        Creates and initializes widgets related to group configuration,
        including main group and custom group/mesh type settings.
        """
        self.lbl_type = QLabel("Type (optionnel")
        self.checkbox_type = QCheckBox()
        self.checkbox_type.setChecked(False)
        self.lbl_close_type = QLabel(")")
        self.info_icon_type = self.create_info_button()

        self.lbl_custom_grp_type = QLabel("Group types :")
        self.entry_custom_grp_type = QLineEdit()
        self.entry_custom_grp_type.setPlaceholderText("grp, ctrl, ...")

        self.lbl_custom_mesh_type = QLabel("Mesh types:")
        self.info_icon_mesh = self.create_info_button()
        self.entry_custom_mesh_type = QLineEdit()
        self.entry_custom_mesh_type.setPlaceholderText("hi, lo, ...")

    def create_zoning_widgets(self) -> None:
        """
        Create widgets for zoning settings.

        Creates and initializes widgets related to zoning configuration,
        including checkbox, labels and entry fields for different zones.
        """
        self.lbl_custom_zoning = QLabel("Custom Zoning (optionnel")
        self.info_icon_zoning = self.create_info_button()
        self.lbl_close_zoning = QLabel(")")
        self.checkbox_zoning = QCheckBox()
        self.checkbox_zoning.setChecked(True)

        self.entry_custom_zoning = QLineEdit()
        self.create_zoning_entry_widgets()

    def create_zoning_entry_widgets(self) -> None:
        """
        Create entry widgets for zoning.

        Creates and initializes entry fields for each zoning direction
        (Left, Center, Right, Top, Middle, Bottom, Front, Back).
        """
        zoning_labels_dict = {"Left": "Lt", "Center": "Ct", "Right": "Rt", "Top": "Tp", "Middle": "Md", "Bottom": "Bm", "Front": "Fr", "Back": "Bk"}
        for label, short_label in zoning_labels_dict.items():
            setattr(self, f"lbl_{label.lower()}", QLabel(f"{label}:"))
            entry = QLineEdit()
            entry.setFixedWidth(self.WIDTH_ENTRY_ZONING)
            entry.setPlaceholderText(short_label)
            setattr(self, f"entry_{label.lower()}", entry)

    def create_orientation_widgets(self) -> None:
        """
        Create widgets for orientation settings.

        Creates and initializes widgets related to orientation configuration,
        including checkbox, labels and entry fields for different orientations.
        """
        self.lbl_custom_orientation = QLabel("Custom Orientation (optionnel")
        self.info_icon_orientation = self.create_info_button()
        self.lbl_close_orientation = QLabel(")")
        self.checkbox_orientation = QCheckBox()
        self.checkbox_orientation.setChecked(True)

        orientation_labels_dict = {"North": "Nt", "South": "St", "East": "Et", "West": "Wt"}
        for label, short_label in orientation_labels_dict.items():
            setattr(self, f"lbl_{label.lower()}", QLabel(f"{label}:"))
            entry = QLineEdit()
            entry.setFixedWidth(self.WIDTH_ENTRY_ZONING)
            entry.setPlaceholderText(short_label)
            setattr(self, f"entry_{label.lower()}", entry)

    def create_symmetry_widgets(self) -> None:
        """
        Create widgets for symmetry settings.

        Creates and initializes widgets related to symmetry configuration,
        including checkbox, labels and entry fields for left/right symmetry.
        """
        self.lbl_symmetry = QLabel("Custom Symmetry (optionnel")
        self.info_icon_symmetry = self.create_info_button()
        self.lbl_close_symmetry = QLabel(")")
        self.checkbox_symmetry = QCheckBox()
        self.checkbox_symmetry.setChecked(True)

        symmetry_labels_dict = {"Left": "L", "Right": "R"}
        for label, short_label in symmetry_labels_dict.items():
            setattr(self, f"lbl_symmetry_{label.lower()}", QLabel(f"Symmetry {label}:"))
            entry = QLineEdit()
            entry.setFixedWidth(self.WIDTH_ENTRY_ZONING)
            entry.setPlaceholderText(short_label)
            setattr(self, f"entry_symmetry_{label.lower()}", entry)

    def create_inc_widgets(self) -> None:
        """
        Create widgets for alphabetical and numerical incrementation.
        """
        self.lbl_inc = QLabel("Incrementations")
        self.info_icon_inc = self.create_info_button()

        self.lbl_n_inc_lenght = QLabel("Numerical increment lenght:")
        self.entry_n_inc_lenght = QLineEdit()
        self.entry_n_inc_lenght.setPlaceholderText("3")
        self.entry_n_inc_lenght.setFixedWidth(self.WIDTH_ENTRY_ZONING)

    def create_save_widget(self) -> None:
        """
        Create save button widget.

        Creates and initializes the save button for the preset settings.
        """
        self.btn_delete_preset = QPushButton("Delete Preset")
        self.btn_delete_preset.setStyleSheet("color: #D94E3B;")
        self.btn_save_preset = QPushButton("Save Preset")

    def create_info_button(self) -> QPushButton:
        """
        Create a standard info button.

        Returns
        -------
        QPushButton
            A configured info button with standard styling.
        """
        button = QPushButton("?")
        button.setFixedSize(20, 20)
        button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                font-weight: bold;
                background-color: #5D5D5D;
                text-align: center;
                padding: 0px;
                line-height: 20px;
            }
            QPushButton:hover {
                background-color: #B9B9C9;
            }
        """)
        button.setToolTip("Click to display user manual")
        return button
    
    def create_manual_widget(self) -> None:
        """
        Create the manual widget.
        """
        self.manual_name_structure_widget = QTextEdit()
        self.manual_name_structure_widget.setReadOnly(True)
        self.manual_name_structure_widget.setMinimumWidth(400)     
        self.manual_name_structure_widget.hide()
        
        self.manual_main_group_widget = QTextEdit()
        self.manual_main_group_widget.setReadOnly(True)
        self.manual_main_group_widget.setMinimumWidth(400)
        self.manual_main_group_widget.hide()
        
        self.manual_type_widget = QTextEdit()
        self.manual_type_widget.setReadOnly(True)
        self.manual_type_widget.setMinimumWidth(400)
        self.manual_type_widget.hide()
        
        self.manual_zoning_widget = QTextEdit()
        self.manual_zoning_widget.setReadOnly(True)
        self.manual_zoning_widget.setMinimumWidth(400)
        self.manual_zoning_widget.hide()
        
        self.manual_orientation_widget = QTextEdit()
        self.manual_orientation_widget.setReadOnly(True)
        self.manual_orientation_widget.setMinimumWidth(400)
        self.manual_orientation_widget.hide()
        
        self.manual_symmetry_widget = QTextEdit()
        self.manual_symmetry_widget.setReadOnly(True)
        self.manual_symmetry_widget.setMinimumWidth(400)
        self.manual_symmetry_widget.hide()
        
        self.manual_inc_widget = QTextEdit()
        self.manual_inc_widget.setReadOnly(True)
        self.manual_inc_widget.setMinimumWidth(400)
        self.manual_inc_widget.hide()
        
        self.btn_hide_manual = QPushButton("Close Manual")
        self.btn_hide_manual.setVisible(False)

        try:
            with open(MANUAL_NAME_STRUCTURE, "r", encoding="utf-8") as f:
                manual_content = f.read()
            self.manual_name_structure_widget.setMarkdown(manual_content)
        except FileNotFoundError:
            self.manual_name_structure_widget.setPlainText("Manuel d'utilisation non trouvé.")
            
        try:
            with open(MANUAL_MAIN_GROUP, "r", encoding="utf-8") as f:
                manual_content = f.read()
            self.manual_main_group_widget.setMarkdown(manual_content)
        except FileNotFoundError:
            self.manual_main_group_widget.setPlainText("Manuel d'utilisation non trouvé.")
            
        try:
            with open(MANUAL_TYPE, "r", encoding="utf-8") as f:
                manual_content = f.read()
            self.manual_type_widget.setMarkdown(manual_content)
        except FileNotFoundError:
            self.manual_type_widget.setPlainText("Manuel d'utilisation non trouvé.")
            
        try:
            with open(MANUAL_ZONING, "r", encoding="utf-8") as f:
                manual_content = f.read()
            self.manual_zoning_widget.setMarkdown(manual_content)
        except FileNotFoundError:
            self.manual_zoning_widget.setPlainText("Manuel d'utilisation non trouvé.")
            
        try:
            with open(MANUAL_ORIENTATION, "r", encoding="utf-8") as f:
                manual_content = f.read()
            self.manual_orientation_widget.setMarkdown(manual_content)
        except FileNotFoundError:
            self.manual_orientation_widget.setPlainText("Manuel d'utilisation non trouvé.")
            
        try:
            with open(MANUAL_SYMMETRY, "r", encoding="utf-8") as f:
                manual_content = f.read()
            self.manual_symmetry_widget.setMarkdown(manual_content)
        except FileNotFoundError:
            self.manual_symmetry_widget.setPlainText("Manuel d'utilisation non trouvé.")
            
        try:
            with open(MANUAL_INC, "r", encoding="utf-8") as f:
                manual_content = f.read()
            self.manual_inc_widget.setMarkdown(manual_content)
        except FileNotFoundError:
            self.manual_inc_widget.setPlainText("Manuel d'utilisation non trouvé.")
            
    def create_manual_layout(self) -> None:
        """
        Create the manual layout.
        """
        self.vbox_manual.addWidget(self.manual_name_structure_widget)
        self.vbox_manual.addWidget(self.manual_main_group_widget)
        self.vbox_manual.addWidget(self.manual_type_widget)
        self.vbox_manual.addWidget(self.manual_zoning_widget)
        self.vbox_manual.addWidget(self.manual_orientation_widget)
        self.vbox_manual.addWidget(self.manual_symmetry_widget)
        self.vbox_manual.addWidget(self.manual_inc_widget)
        self.hbox_hide_manual = QHBoxLayout()
        self.hbox_hide_manual.addStretch()
        self.hbox_hide_manual.addWidget(self.btn_hide_manual)
        self.vbox_manual.addLayout(self.hbox_hide_manual)

    def create_layout(self) -> None:
        """
        Create and set up the layout for the dialog.
        """
        self.hbox_main = QHBoxLayout()
        self.setLayout(self.hbox_main)
        
        self.settings_widget = QWidget()
        self.settings_widget.setMinimumWidth(400)
        self.settings_layout = QVBoxLayout(self.settings_widget)
   
        self.vbox_manual = QVBoxLayout()
        
        self.hbox_main.addWidget(self.settings_widget)
        self.hbox_main.addLayout(self.vbox_manual)

        self.create_preset_layout()
        self.create_visibility_layout()
        self.create_manual_layout()


    def create_preset_layout(self) -> None:
        """
        Create layout for preset management.

        Creates and configures the layout for preset-related widgets.
        """
        hbox_new_preset = QHBoxLayout()
        hbox_new_preset.addWidget(self.lbl_new_preset)
        hbox_new_preset.addWidget(self.entry_new_preset)
        hbox_new_preset.addWidget(self.btn_create_preset)

        hbox_presets = QHBoxLayout()
        hbox_presets.addStretch()
        hbox_presets.addWidget(self.lbl_presets)
        hbox_presets.addWidget(self.combo_presets)

        self.settings_layout.addLayout(hbox_new_preset)
        self.settings_layout.addLayout(hbox_presets)

    def create_visibility_layout(self) -> None:
        """
        Create layout for all other settings.

        Creates and configures the layout for all settings widgets,
        including structure, group, zoning, orientation, and symmetry settings.
        """
        self.vbox_visibility = QVBoxLayout()
        self.settings_layout.addLayout(self.vbox_visibility)

        self.add_horizontal_line(self.vbox_visibility)
        self.create_structure_layout()
        self.add_horizontal_line(self.vbox_visibility)
        self.create_main_group_layout()
        self.add_horizontal_line(self.vbox_visibility)
        self.create_type_layout()
        self.add_horizontal_line(self.vbox_visibility)
        self.create_zoning_layout()
        self.add_horizontal_line(self.vbox_visibility)
        self.create_orientation_layout()
        self.add_horizontal_line(self.vbox_visibility)
        self.create_symmetry_layout()
        self.add_horizontal_line(self.vbox_visibility)
        self.create_inc_layout()
        self.add_horizontal_line(self.vbox_visibility)
        self.create_save_layout()

        self.vbox_visibility.addStretch()

    def create_structure_layout(self) -> None:
        """
        Create layout for name structure.

        Creates and configures the layout for name structure widgets.
        """
        hbox_a = QHBoxLayout()
        hbox_a.addWidget(self.lbl_structure)   
        hbox_a.addWidget(self.info_icon_structure)
        hbox_a.addStretch()

        hbox_b = QHBoxLayout()
        hbox_b.addWidget(self.entry_structure)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_a)
        vbox.addLayout(hbox_b)
        self.vbox_visibility.addLayout(vbox)

    def create_main_group_layout(self) -> None:
        """
        Create layout for main group settings.
        """
        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl_main_group)
        hbox.addWidget(self.entry_main_group)
        hbox.addWidget(self.info_icon_main_group)
        hbox.addStretch()
        self.vbox_visibility.addLayout(hbox)

    def create_type_layout(self) -> None:
        """
        Create layout for group settings.

        Creates and configures the layout for group-related widgets.
        """
        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl_type)
        hbox.addWidget(self.checkbox_type)
        hbox.addWidget(self.lbl_close_type)
        hbox.addWidget(self.info_icon_type)
        hbox.addStretch()
        self.vbox_visibility.addLayout(hbox)

        for attr in ['custom_grp_type', 'custom_mesh_type']:
            hbox = QHBoxLayout()
            hbox.addWidget(getattr(self, f'lbl_{attr}'))
            hbox.addWidget(getattr(self, f'entry_{attr}'))
            
            self.vbox_visibility.addLayout(hbox)

    def create_zoning_layout(self) -> None:
        """
        Create layout for zoning settings.

        Creates and configures the layout for zoning-related widgets.
        """
        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl_custom_zoning)
        hbox.addWidget(self.checkbox_zoning)
        hbox.addWidget(self.lbl_close_zoning)
        hbox.addWidget(self.info_icon_zoning)
        hbox.addStretch()
        self.vbox_visibility.addLayout(hbox)

        grid = QGridLayout()
        zoning_labels = ["left", "center", "right", "top", "middle", "bottom", "front", "back"]
        for i, label in enumerate(zoning_labels):
            hbox = QHBoxLayout()
            hbox.addWidget(getattr(self, f'lbl_{label}'))
            hbox.addWidget(getattr(self, f'entry_{label}'))
            grid.addLayout(hbox, i // 3, i % 3)

        hbox_grid = QHBoxLayout()
        hbox_grid.addStretch()
        hbox_grid.addLayout(grid)
        hbox_grid.addStretch()
        self.vbox_visibility.addLayout(hbox_grid)

    def create_orientation_layout(self) -> None:
        """
        Create layout for orientation settings.

        Creates and configures the layout for orientation-related widgets.
        """
        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl_custom_orientation)
        hbox.addWidget(self.checkbox_orientation)
        hbox.addWidget(self.lbl_close_orientation)
        hbox.addWidget(self.info_icon_orientation)
        hbox.addStretch()
        self.vbox_visibility.addLayout(hbox)

        grid = QGridLayout()
        orientation_labels = ["north", "south", "east", "west"]
        for i, label in enumerate(orientation_labels):
            hbox = QHBoxLayout()
            hbox.addWidget(getattr(self, f'lbl_{label}'))
            hbox.addWidget(getattr(self, f'entry_{label}'))
            grid.addLayout(hbox, i // 2, i % 2)

        hbox_grid = QHBoxLayout()
        hbox_grid.addStretch()
        hbox_grid.addLayout(grid)
        hbox_grid.addStretch()
        self.vbox_visibility.addLayout(hbox_grid)

    def create_symmetry_layout(self) -> None:
        """
        Create layout for symmetry settings.

        Creates and configures the layout for symmetry-related widgets.
        """
        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl_symmetry)
        hbox.addWidget(self.checkbox_symmetry)
        hbox.addWidget(self.lbl_close_symmetry)
        hbox.addWidget(self.info_icon_symmetry)
        hbox.addStretch()
        self.vbox_visibility.addLayout(hbox)

        grid = QGridLayout()
        for i, label in enumerate(["left", "right"]):
            hbox = QHBoxLayout()
            hbox.addWidget(getattr(self, f'lbl_symmetry_{label}'))
            hbox.addWidget(getattr(self, f'entry_symmetry_{label}'))
            grid.addLayout(hbox, i, 0)

        hbox_grid = QHBoxLayout()
        hbox_grid.addStretch()
        hbox_grid.addLayout(grid)
        hbox_grid.addStretch()
        self.vbox_visibility.addLayout(hbox_grid)

    def create_inc_layout(self) -> None:
        """
        Create layout for incrementation settings.
        """
        hbox_a = QHBoxLayout()
        hbox_a.addWidget(self.lbl_inc)
        hbox_a.addWidget(self.info_icon_inc)
        hbox_a.addStretch()
        self.vbox_visibility.addLayout(hbox_a)

        hbox_b = QHBoxLayout()
        hbox_b.addWidget(self.lbl_n_inc_lenght)
        hbox_b.addWidget(self.entry_n_inc_lenght)
        hbox_b.addStretch()
        self.vbox_visibility.addLayout(hbox_b)


    def create_save_layout(self) -> None:
        """
        Create layout for save button.

        Creates and configures the layout for the save button widget.
        """
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.btn_delete_preset)
        hbox.addWidget(self.btn_save_preset)
        self.vbox_visibility.addLayout(hbox)

    def add_horizontal_line(self, layout: QVBoxLayout) -> None:
        """
        Add a horizontal line to the given layout.

        Parameters
        ----------
        layout : QVBoxLayout
            The layout to add the horizontal line to.
        """
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

    def create_connections(self) -> None:
        """
        Create signal-slot connections for various widgets.

        This method connects user interactions with widgets to their corresponding
        handler methods.
        """
        self.btn_create_preset.clicked.connect(self.on_create_preset)
        self.combo_presets.currentTextChanged.connect(self.on_preset_changed)
        self.btn_delete_preset.clicked.connect(self.on_delete_preset)
        self.btn_save_preset.clicked.connect(self.save_and_emit)
        self.btn_hide_manual.clicked.connect(self.hide_manual)
        self.info_icon_structure.clicked.connect(lambda: self.toggle_layout_visibility_manual(self.info_icon_structure))
        self.info_icon_main_group.clicked.connect(lambda: self.toggle_layout_visibility_manual(self.info_icon_main_group))
        self.info_icon_type.clicked.connect(lambda: self.toggle_layout_visibility_manual(self.info_icon_type))
        self.info_icon_zoning.clicked.connect(lambda: self.toggle_layout_visibility_manual(self.info_icon_zoning))
        self.info_icon_orientation.clicked.connect(lambda: self.toggle_layout_visibility_manual(self.info_icon_orientation))
        self.info_icon_symmetry.clicked.connect(lambda: self.toggle_layout_visibility_manual(self.info_icon_symmetry))
        self.info_icon_inc.clicked.connect(lambda: self.toggle_layout_visibility_manual(self.info_icon_inc))

    def load_initial_settings(self) -> None:
        """
        Load initial settings when the dialog is first opened.

        This method populates the preset combo box, sets the last used preset,
        and loads its settings if applicable.
        """
        preset_names = self.user_settings_logics.get_preset_names()
        if preset_names:
            self.combo_presets.addItems(preset_names)
        last_preset = self.user_settings_logics.get_last_preset()
        self.combo_presets.setCurrentText(last_preset)

        self.set_settings_visibility = self.combo_presets.currentText() != self.no_preset
        self.toggle_user_settings(self.set_settings_visibility)

        if self.user_settings_logics.get_last_preset() != NO_PRESET:
            self.load_presets(self.user_settings_logics.get_last_preset())

    def on_create_preset(self) -> None:
        """
        Handle the creation of a new preset.

        This method is called when the user clicks the 'Create' button to make a new preset.
        """
        self.user_settings_logics.create_preset(self.entry_new_preset.text(), self.combo_presets)

    def on_preset_changed(self, combo_text: str) -> None:
        """
        Handle changes in the selected preset.

        Parameters
        ----------
        combo_text : str
            The text of the newly selected preset.
        """
        if combo_text == self.no_preset:    
            visibility = False
            self.user_settings_logics.set_last_preset(self.no_preset)
        else:
            visibility = True
            self.user_settings_logics.set_last_preset(combo_text)
            last_preset = self.user_settings_logics.get_last_preset()
            self.load_presets(last_preset)
        self.toggle_user_settings(visibility)

    def load_presets(self, last_preset: str) -> None:
        """
        Load settings for a given preset.

        Parameters
        ----------
        last_preset : str
            The name of the preset to load.
        """
        zoning_entries_dict = {"Left": self.entry_left, "Center": self.entry_center, "Right": self.entry_right, "Top": self.entry_top, "Middle": self.entry_middle, "Bottom": self.entry_bottom, "Front": self.entry_front, "Back": self.entry_back}
        orientation_entries_dict = {"North": self.entry_north, "South": self.entry_south, "East": self.entry_east, "West": self.entry_west}
        symmetry_entries_dict = {"Left": self.entry_symmetry_left, "Right": self.entry_symmetry_right}
        checkbox_entries_dict = {"type": self.checkbox_type, "zoning": self.checkbox_zoning, "orientation": self.checkbox_orientation, "symmetry": self.checkbox_symmetry}

        self.user_settings_logics.load_structure(self.entry_structure, last_preset)
        self.user_settings_logics.load_main_group(self.entry_main_group, last_preset)
        self.user_settings_logics.load_group_types(self.entry_custom_grp_type, last_preset)
        self.user_settings_logics.load_mesh_types(self.entry_custom_mesh_type, last_preset)
        self.user_settings_logics.load_zoning(zoning_entries_dict, last_preset)
        self.user_settings_logics.load_orientation(orientation_entries_dict, last_preset)
        self.user_settings_logics.load_symmetry(symmetry_entries_dict, last_preset)
        self.user_settings_logics.load_n_inc_lenght(self.entry_n_inc_lenght, last_preset)
        self.user_settings_logics.load_checkbox(checkbox_entries_dict, last_preset)
        
    def toggle_user_settings(self, visible: bool) -> None:
        """
        Toggle the visibility of user settings widgets.

        Parameters
        ----------
        visible : bool
            Whether the settings should be visible or not.
        """
        if visible:
            for i in range(self.vbox_visibility.count()):
                item = self.vbox_visibility.itemAt(i)
                if item.widget():
                    item.widget().setVisible(True)
                elif item.layout():
                    self.toggle_layout_visibility(item.layout(), True)
        else:
            for i in range(self.vbox_visibility.count()):
                item = self.vbox_visibility.itemAt(i)
                if item.widget():
                    item.widget().setVisible(False)
                elif item.layout():
                    self.toggle_layout_visibility(item.layout(), False)
        self.adjustSize()
        self.setFixedHeight(self.sizeHint().height())

    def toggle_layout_visibility(self, layout: QLayout, visible: bool) -> None:
        """
        Recursively toggle the visibility of widgets in a layout.

        Parameters
        ----------
        layout : QLayout
            The layout whose widgets' visibility should be toggled.
        visible : bool
            Whether the widgets should be visible or not.
        """
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget():
                item.widget().setVisible(visible)
            elif item.layout():
                self.toggle_layout_visibility(item.layout(), visible)
                
    def toggle_layout_visibility_manual(self, info_btn: QPushButton) -> None:
        """
        Toggle the visibility of the manual layout.
        """
        manual_dict = self.manual_dict()
        for key, value in manual_dict.items():
            if info_btn == key:
                value.setVisible(True)
                self.btn_hide_manual.setVisible(True)
                self.adjustSize()
                self.setFixedWidth(self.sizeHint().width())
            else:
                value.setVisible(False)
                
    def hide_manual(self) -> None:
        """
        Hide all manual widgets.
        """
        manual_dict = self.manual_dict()
        for value in manual_dict.values():
            value.setVisible(False)
        self.btn_hide_manual.setVisible(False)
        self.adjustSize()
        self.setFixedWidth(self.sizeHint().width())
        
    
    def manual_dict(self) -> dict:
        """
        Return a dictionary of manual widgets.
        """
        manual_dict = {self.info_icon_structure: self.manual_name_structure_widget,
                       self.info_icon_main_group: self.manual_main_group_widget,
                       self.info_icon_type: self.manual_type_widget,
                       self.info_icon_zoning: self.manual_zoning_widget,
                       self.info_icon_orientation: self.manual_orientation_widget,
                       self.info_icon_symmetry: self.manual_symmetry_widget,
                       self.info_icon_inc: self.manual_inc_widget
                       }
        return manual_dict

    def set_structure(self) -> str:
        """
        Set the structure of the name.

        Returns
        -------
        str
            The validated structure string or an error message.
        """
        structure = self.entry_structure.text().strip("_")
        valid_categories = ['[symmetry]', '[type]', '[name]', '[zoning]', '[orientation]', '[alphabetical_inc]', '[numerical_inc]']
        used_categories = []

        if structure == "":
            return ""
        if not all(character.isalpha() or character == "[" or character == "]" or character == '_' for character in structure):
            QMessageBox.critical(self,"Error", "Structure should only contain '_' and valid name categories")
            return "Bad characters"
        if "[name]" not in structure :
            QMessageBox.critical(self,"Error", "la structure doit au moins contenir un [name]")
            return "Bad characters"
        
        while structure:
            if used_categories:
                for category in used_categories:
                    if structure.startswith(category):
                        QMessageBox.critical(self, "Error", f"The category {category} is used more than once in the structure")
                        return "Bad characters"

            if structure.startswith("["):
                bracket_content = structure[1:structure.find("]")]
                if "_" in bracket_content and bracket_content != "alphabetical_inc" and bracket_content != "numerical_inc":
                    QMessageBox.critical(self, "Error", "Les catégories ne doivent pas contenir de underscore '_' entre les crochets")
                    return "Bad characters"

            if structure.startswith("_"):
                if structure[1] == "_":
                    QMessageBox.critical(self, "Error", "Les underscores multiples ne sont pas autorisés dans la structure")
                    return "Bad characters"
            if structure.startswith("_"):
                structure = structure[1:]
            else:
                for category in valid_categories:
                    if structure.startswith(category):
                        valid_categories.remove(category)
                        used_categories.append(category)
                        structure = structure[len(category):]
                        break
                else:
                    QMessageBox.critical(self, "Error", "Structure should only contain underscores and the following categories:\n[symmetry], [type], [name], [zoning], [orientation], [alphabetical_inc], [numerical_inc].")
                    return "Bad characters"
        return self.entry_structure.text().strip("_")
    
    def set_main_group(self) -> str:
        """
        Set and validate the main group name.

        Returns
        -------
        str
            The validated main group name or an error message.
        """
        main_group = self.entry_main_group.text()
        if not all(character.isalpha() or character == '_' for character in main_group):
            QMessageBox.critical(self, "Error", "Main group should only contain letters and underscores.")
            return "Bad characters"
        return main_group

    def set_group_types_dict(self) -> dict:
        """
        Set and validate the group types.

        Returns
        -------
        dict or str
            A dictionary of group types or an error message.
        """
        group_types = self.entry_custom_grp_type.text()
        if not all(character.isalpha() or character == ',' or character == ' ' for character in group_types):
            QMessageBox.critical(self, "Error", "Group types should only contain letters and commas.")
            return "Bad characters"

        group_types_dict = {type.strip().upper(): type.strip() for type in group_types.split(',') if type.strip()}
        
        return group_types_dict
    
    def set_mesh_types_dict(self) -> dict:
        """
        Set and validate the mesh types.

        Returns
        -------
        dict or str
            A dictionary of mesh types or an error message.
        """
        mesh_types = self.entry_custom_mesh_type.text()
        if not all(character.isalpha() or character == ',' or character == ' ' for character in mesh_types):
            QMessageBox.critical(self, "Error", "Mesh types should only contain letters and commas.")
            return "Bad characters"

        mesh_types_dict = {type.strip().upper(): type.strip() for type in mesh_types.split(',') if type.strip()}
        
        return mesh_types_dict

    def set_zoning_dict(self) -> dict:
        """
        Set and validate the zoning settings.

        Returns
        -------
        dict or str
            A dictionary of zoning settings or an error message.
        """
        zoning_dict = {}
        for enum_value in DefaultZoningSingle:
            entry_name = f"entry_{enum_value.name.lower()}"
            entry_widget = getattr(self, entry_name, None)
            if entry_widget and entry_widget.text():
                if not entry_widget.text().isalpha():
                    QMessageBox.critical(self, "Error", "Zoning should only contain letters.")
                    return "Bad characters"
                zoning_dict[enum_value.name.capitalize()] = entry_widget.text()
            else:
                zoning_dict[enum_value.name.capitalize()] = enum_value.value
        return zoning_dict
    
    def set_orientation_dict(self) -> dict:
        """
        Set and validate the orientation settings.

        Returns
        -------
        dict or str
            A dictionary of orientation settings or an error message.
        """
        orientation_dict = {}
        for enum_value in DefaultOrientSingle:
            entry_name = f"entry_{enum_value.name.lower()}"
            entry_widget = getattr(self, entry_name, None)
            if entry_widget and entry_widget.text():
                if not entry_widget.text().isalpha():
                    QMessageBox.critical(self, "Error", "Orientation should only contain letters.")
                    return "Bad characters"
                orientation_dict[enum_value.name.capitalize()] = entry_widget.text()
            else:
                orientation_dict[enum_value.name.capitalize()] = enum_value.value
        return orientation_dict
    
    def set_symmetry_dict(self) -> dict:
        """
        Set and validate the symmetry settings.

        Returns
        -------
        dict or str
            A dictionary of symmetry settings or an error message.
        """
        symmetry_dict = {}
        for enum_value in DefaultSymmetryOptions:
            entry_name = f"entry_symmetry_{enum_value.name.lower()}"
            entry_widget = getattr(self, entry_name, None)
            
            if entry_widget and entry_widget.text():
                if not entry_widget.text().isalpha():
                    QMessageBox.critical(self, "Error", "Symmetry should only contain letters.")
                    return "Bad characters"
                symmetry_dict[enum_value.name.capitalize()] = entry_widget.text()
            else:
                symmetry_dict[enum_value.name.capitalize()] = enum_value.value
        return symmetry_dict
    
    def set_n_inc_lenght(self) -> int:
        """
        Set and validate the numerical increment length.
        """
        n_inc_lenght = None
        entry_widget = self.entry_n_inc_lenght
        if entry_widget and entry_widget.text():
            if not entry_widget.text().isdigit():
                QMessageBox.critical(self, "Error", "Numerical increment length should only contain digits.")
                return "Bad characters"
            elif int(entry_widget.text()) < 1:
                QMessageBox.critical(self, "Error", "Numerical increment length should be greater than 0.")
                return "Bad characters"
        if entry_widget.text() == "":
            n_inc_lenght = "3"
        else:
            n_inc_lenght = entry_widget.text()
        return int(n_inc_lenght)
    
    def set_checkbox_dict(self) -> dict:
        """
        Set and validate the checkbox settings.

        Returns
        -------
        dict
            A dictionary containing the state of all checkboxes.
        """
        checkbox_dict = {"type": self.checkbox_type.isChecked(), "zoning": self.checkbox_zoning.isChecked(), "orientation": self.checkbox_orientation.isChecked(), "symmetry": self.checkbox_symmetry.isChecked()}
        return checkbox_dict

    def save_and_emit(self) -> None:
        """
        Save the current settings and emit a signal.

        This method validates all settings (structure, main group, group types, mesh types,
        zoning, orientation and symmetry), saves them if valid, and emits a signal to 
        indicate that settings have been saved. It also displays a message box to inform 
        the user about the need to restart the interface.

        Returns
        -------
        None
            The method returns nothing but may exit early if validation fails.

        Notes
        -----
        - The method will return early without saving if any validation fails
        - A message box is shown after successful save
        - The window closes after the user acknowledges the message
        """
        structure = self.set_structure()
        if structure == "Bad characters":
            return
        main_group = self.set_main_group()
        if main_group == "Bad characters":
            return
        group_types_dict = self.set_group_types_dict()
        if group_types_dict == "Bad characters":
            return
        mesh_types_dict = self.set_mesh_types_dict()
        if mesh_types_dict == "Bad characters":
            return
        zoning_dict = self.set_zoning_dict()
        if zoning_dict == "Bad characters":
            return
        orientation_dict = self.set_orientation_dict()  
        if orientation_dict == "Bad characters":
            return
        symmetry_dict = self.set_symmetry_dict()
        if symmetry_dict == "Bad characters":
            return
        n_inc_lenght = self.set_n_inc_lenght()
        if n_inc_lenght == "Bad characters":
            return
        checkbox_entries_dict = self.set_checkbox_dict()
        self.user_settings_logics.save_preset(
            self.combo_presets.currentText(),
            structure,
            main_group,
            group_types_dict,
            mesh_types_dict,
            zoning_dict,
            orientation_dict,
            symmetry_dict,
            checkbox_entries_dict,
            n_inc_lenght
        )
        
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Settings Saved")
        msg_box.setText("Settings have been saved successfully.")
        msg_box.setInformativeText("The interface needs to be restarted for the changes to take effect.")
        msg_box.setStandardButtons(QMessageBox.Ok)
        
        result = msg_box.exec_()
        
        if result == QMessageBox.Ok:
            self.settings_saved.emit()
            self.restart_application.emit()
            self.close()


    def on_delete_preset(self) -> None:
        """
        Handle the deletion of a preset.
        """
        self.user_settings_logics.delete_preset(self.combo_presets)
