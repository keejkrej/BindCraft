"""
Configuration Panel for BindCraft GUI
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLineEdit, QLabel,
    QPushButton, QSpinBox, QCheckBox, QComboBox, QFormLayout,
    QGroupBox, QFileDialog
)


class ConfigPanel(QWidget):
    """Configuration panel with tabs for all settings."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the configuration panel UI."""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("<h3>Configuration</h3>")
        layout.addWidget(title)

        # Tab widget
        self.tabs = QTabWidget()

        # Add tabs
        self.tabs.addTab(self.create_target_tab(), "Target Setup")
        self.tabs.addTab(self.create_design_tab(), "Design Parameters")
        self.tabs.addTab(self.create_filters_tab(), "Filter Settings")

        layout.addWidget(self.tabs)

    def create_target_tab(self):
        """Create the target setup tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # PDB Loader
        pdb_group = QGroupBox("Target Structure")
        pdb_layout = QVBoxLayout()

        self.pdb_path_label = QLabel("No PDB file loaded")
        pdb_layout.addWidget(self.pdb_path_label)

        load_pdb_btn = QPushButton("Load Target PDB")
        load_pdb_btn.clicked.connect(self.load_pdb)
        pdb_layout.addWidget(load_pdb_btn)

        pdb_group.setLayout(pdb_layout)
        layout.addWidget(pdb_group)

        # Target Configuration
        config_group = QGroupBox("Target Configuration")
        config_layout = QFormLayout()

        self.binder_name_input = QLineEdit("my_binder")
        config_layout.addRow("Binder Name:", self.binder_name_input)

        self.target_chains_input = QLineEdit("A")
        config_layout.addRow("Target Chains:", self.target_chains_input)

        self.hotspot_residues_input = QLineEdit("24,25,26,27")
        config_layout.addRow("Hotspot Residues:", self.hotspot_residues_input)

        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # 3D Viewer placeholder
        viewer_group = QGroupBox("3D Structure Viewer")
        viewer_layout = QVBoxLayout()
        viewer_placeholder = QLabel("(3D viewer would be displayed here using PyVista)\n\n"
                                   "In the full version, you could click residues\n"
                                   "to populate the hotspot field.")
        viewer_placeholder.setStyleSheet("QLabel { padding: 20px; background-color: #f0f0f0; }")
        viewer_layout.addWidget(viewer_placeholder)
        viewer_group.setLayout(viewer_layout)
        layout.addWidget(viewer_group)

        layout.addStretch()
        return widget

    def create_design_tab(self):
        """Create the design parameters tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Binder Length
        length_group = QGroupBox("Binder Length")
        length_layout = QFormLayout()

        self.min_length_input = QSpinBox()
        self.min_length_input.setRange(10, 200)
        self.min_length_input.setValue(50)
        length_layout.addRow("Minimum Length:", self.min_length_input)

        self.max_length_input = QSpinBox()
        self.max_length_input.setRange(10, 200)
        self.max_length_input.setValue(100)
        length_layout.addRow("Maximum Length:", self.max_length_input)

        length_group.setLayout(length_layout)
        layout.addWidget(length_group)

        # Advanced Settings
        advanced_group = QGroupBox("Advanced Settings")
        advanced_layout = QFormLayout()

        self.advanced_profile_input = QComboBox()
        self.advanced_profile_input.addItems([
            "default_4stage_multimer",
            "fast_2stage",
            "high_quality_6stage"
        ])
        advanced_layout.addRow("Profile:", self.advanced_profile_input)

        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)

        # MPNN Options
        mpnn_group = QGroupBox("ProteinMPNN Options")
        mpnn_layout = QVBoxLayout()

        self.mpnn_redesign_checkbox = QCheckBox("Enable ProteinMPNN Redesign")
        self.mpnn_redesign_checkbox.setChecked(True)
        mpnn_layout.addWidget(self.mpnn_redesign_checkbox)

        self.mpnn_save_fasta_checkbox = QCheckBox("Save MPNN FASTA files")
        mpnn_layout.addWidget(self.mpnn_save_fasta_checkbox)

        mpnn_group.setLayout(mpnn_layout)
        layout.addWidget(mpnn_group)

        # Trajectory Settings
        traj_group = QGroupBox("Trajectory Settings")
        traj_layout = QFormLayout()

        self.target_designs_input = QSpinBox()
        self.target_designs_input.setRange(1, 1000)
        self.target_designs_input.setValue(10)
        traj_layout.addRow("Target Accepted Designs:", self.target_designs_input)

        self.max_trajectories_input = QSpinBox()
        self.max_trajectories_input.setRange(1, 10000)
        self.max_trajectories_input.setValue(100)
        traj_layout.addRow("Max Trajectories:", self.max_trajectories_input)

        traj_group.setLayout(traj_layout)
        layout.addWidget(traj_group)

        layout.addStretch()
        return widget

    def create_filters_tab(self):
        """Create the filter settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Filter Profile Management
        profile_group = QGroupBox("Filter Profile")
        profile_layout = QVBoxLayout()

        btn_layout = QVBoxLayout()
        load_filters_btn = QPushButton("Load Filter Profile")
        save_filters_btn = QPushButton("Save Filter Profile")
        btn_layout.addWidget(load_filters_btn)
        btn_layout.addWidget(save_filters_btn)
        profile_layout.addLayout(btn_layout)

        profile_group.setLayout(profile_layout)
        layout.addWidget(profile_group)

        # Filter Parameters
        filters_group = QGroupBox("Filter Thresholds")
        filters_layout = QFormLayout()

        self.plddt_threshold = QSpinBox()
        self.plddt_threshold.setRange(0, 100)
        self.plddt_threshold.setValue(80)
        filters_layout.addRow("pLDDT (min):", self.plddt_threshold)

        self.dsasa_threshold = QSpinBox()
        self.dsasa_threshold.setRange(0, 2000)
        self.dsasa_threshold.setValue(600)
        filters_layout.addRow("dSASA (min):", self.dsasa_threshold)

        self.shape_comp_threshold = QSpinBox()
        self.shape_comp_threshold.setRange(0, 100)
        self.shape_comp_threshold.setValue(60)
        filters_layout.addRow("Shape Complementarity (min):", self.shape_comp_threshold)

        self.pae_threshold = QSpinBox()
        self.pae_threshold.setRange(0, 50)
        self.pae_threshold.setValue(10)
        filters_layout.addRow("PAE (max):", self.pae_threshold)

        filters_group.setLayout(filters_layout)
        layout.addWidget(filters_group)

        layout.addStretch()
        return widget

    def load_pdb(self):
        """Open file dialog to load a PDB file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Target PDB File",
            "",
            "PDB Files (*.pdb);;All Files (*)"
        )
        if file_path:
            self.pdb_path_label.setText(f"Loaded: {file_path}")
            self.pdb_file_path = file_path

    def get_config(self):
        """Get all configuration settings as a dictionary."""
        return {
            "binder_name": self.binder_name_input.text(),
            "target_chains": self.target_chains_input.text(),
            "hotspot_residues": self.hotspot_residues_input.text(),
            "min_length": self.min_length_input.value(),
            "max_length": self.max_length_input.value(),
            "advanced_profile": self.advanced_profile_input.currentText(),
            "mpnn_redesign": self.mpnn_redesign_checkbox.isChecked(),
            "mpnn_save_fasta": self.mpnn_save_fasta_checkbox.isChecked(),
            "target_designs": self.target_designs_input.value(),
            "max_trajectories": self.max_trajectories_input.value(),
            "filters": {
                "plddt": self.plddt_threshold.value(),
                "dsasa": self.dsasa_threshold.value(),
                "shape_comp": self.shape_comp_threshold.value(),
                "pae": self.pae_threshold.value()
            }
        }
