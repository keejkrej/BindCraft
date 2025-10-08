"""
Results Panel for BindCraft GUI
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem,
    QLabel, QHeaderView
)
from PySide6.QtCore import Qt


class ResultsPanel(QWidget):
    """Results panel with tabs for table, 3D viewer, and plots."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the results panel UI."""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("<h3>Results & Visualization</h3>")
        layout.addWidget(title)

        # Tab widget
        self.tabs = QTabWidget()

        # Add tabs
        self.tabs.addTab(self.create_table_tab(), "Accepted Designs")
        self.tabs.addTab(self.create_3d_tab(), "3D Structure Viewer")
        self.tabs.addTab(self.create_plots_tab(), "Analytics Plots")

        layout.addWidget(self.tabs)

    def create_table_tab(self):
        """Create the results table tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(8)
        self.results_table.setHorizontalHeaderLabels([
            "Design Name",
            "pLDDT",
            "PAE",
            "dSASA",
            "Shape Comp",
            "dG",
            "Length",
            "Status"
        ])

        # Make table sortable
        self.results_table.setSortingEnabled(True)

        # Resize columns to content
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        layout.addWidget(self.results_table)

        return widget

    def create_3d_tab(self):
        """Create the 3D structure viewer tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Placeholder for 3D viewer
        viewer_placeholder = QLabel(
            "(3D structure viewer would be displayed here using PyVista)\n\n"
            "Select a design from the 'Accepted Designs' table\n"
            "to view its 3D structure with the target complex.\n\n"
            "Features would include:\n"
            "• Color by pLDDT\n"
            "• Highlight interface residues\n"
            "• Rotate and zoom controls"
        )
        viewer_placeholder.setAlignment(Qt.AlignCenter)
        viewer_placeholder.setStyleSheet("QLabel { padding: 40px; background-color: #f0f0f0; }")
        layout.addWidget(viewer_placeholder)

        return widget

    def create_plots_tab(self):
        """Create the analytics plots tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Placeholder for plots
        plots_placeholder = QLabel(
            "(Analytics plots would be displayed here using PyQtGraph)\n\n"
            "Select a design from the 'Accepted Designs' table\n"
            "to view its analysis plots:\n\n"
            "• PAE (Predicted Aligned Error) heatmap\n"
            "• pLDDT per residue plot\n"
            "• Contact map\n"
            "• Interface analysis"
        )
        plots_placeholder.setAlignment(Qt.AlignCenter)
        plots_placeholder.setStyleSheet("QLabel { padding: 40px; background-color: #f0f0f0; }")
        layout.addWidget(plots_placeholder)

        return widget

    def add_design(self, design_data):
        """Add a new design to the results table."""
        row_position = self.results_table.rowCount()
        self.results_table.insertRow(row_position)

        # Add data to cells
        self.results_table.setItem(row_position, 0, QTableWidgetItem(design_data["name"]))
        self.results_table.setItem(row_position, 1, QTableWidgetItem(f"{design_data['plddt']:.1f}"))
        self.results_table.setItem(row_position, 2, QTableWidgetItem(f"{design_data['pae']:.1f}"))
        self.results_table.setItem(row_position, 3, QTableWidgetItem(f"{design_data['dsasa']:.0f}"))
        self.results_table.setItem(row_position, 4, QTableWidgetItem(f"{design_data['shape_comp']:.1f}"))
        self.results_table.setItem(row_position, 5, QTableWidgetItem(f"{design_data['dg']:.2f}"))
        self.results_table.setItem(row_position, 6, QTableWidgetItem(str(design_data['length'])))
        self.results_table.setItem(row_position, 7, QTableWidgetItem(design_data['status']))

        # Center align numeric values
        for col in range(1, 8):
            item = self.results_table.item(row_position, col)
            if item:
                item.setTextAlignment(Qt.AlignCenter)

    def clear_results(self):
        """Clear all results from the table."""
        self.results_table.setRowCount(0)
