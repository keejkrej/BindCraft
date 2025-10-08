# BindCraft GUI Demo

This is a **mock demo version** of the BindCraft GUI that demonstrates the user interface and workflow without actually performing structure generation.

## Overview

The GUI provides an intuitive interface for the BindCraft binder design pipeline with three main sections:

1. **Configuration Panel** (Left): Configure target setup, design parameters, and filter settings
2. **Run Management** (Center-Top): Control pipeline execution and view logs
3. **Results & Visualization** (Center-Bottom): View accepted designs, 3D structures, and analytics

## What This Demo Does

This demo **simulates** the BindCraft pipeline workflow:

- ✅ Interactive GUI with all planned components
- ✅ Configuration panels for all settings
- ✅ Mock pipeline execution with realistic log output
- ✅ Simulated design generation and filtering
- ✅ Results table with mock data
- ✅ Progress tracking

## What This Demo Does NOT Do

This is a **mock version** that does NOT:

- ❌ Actually run AlphaFold2, RFdiffusion, or ProteinMPNN
- ❌ Generate real protein structures
- ❌ Perform actual structure prediction
- ❌ Create PDB files or real analysis plots
- ❌ Include 3D visualization (PyVista integration)
- ❌ Include analytics plotting (PyQtGraph integration)

Instead, it displays messages like:
> "Mock: Would use AlphaFold2/RFdiffusion to generate 3D backbone"

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Install Dependencies

```bash
cd gui
pip install -r requirements.txt
```

## Running the Demo

```bash
cd gui
python main.py
```

## Usage

1. **Configure Target**:
   - Go to "Target Setup" tab
   - (Optional) Load a PDB file
   - Set binder name, target chains, and hotspot residues

2. **Set Parameters**:
   - Go to "Design Parameters" tab
   - Configure binder length, MPNN options, and trajectory settings

3. **Configure Filters**:
   - Go to "Filter Settings" tab
   - Adjust threshold values for pLDDT, dSASA, etc.

4. **Run Pipeline**:
   - Click "Start Run" button
   - Watch the log output showing simulated pipeline execution
   - See accepted designs appear in the results table

5. **View Results**:
   - Check the "Accepted Designs" table
   - (Placeholders shown for 3D viewer and analytics plots)

## Architecture

The demo follows the architecture outlined in `gui_plan.md`:

- **main.py**: Entry point
- **main_window.py**: Main application window with layout
- **config_panel.py**: Configuration panel with three tabs
- **results_panel.py**: Results display with table and placeholder tabs
- **mock_worker.py**: QThread worker that simulates pipeline execution

## Real Implementation Notes

To convert this demo into a real application, you would need to:

1. **Install Additional Dependencies**:
   ```
   pyvista>=0.40.0      # For 3D visualization
   pyqtgraph>=0.13.0    # For 2D plotting
   numpy
   ```

2. **Integrate Real Backend**:
   - Replace `mock_worker.py` with actual BindCraft pipeline calls
   - Import and call functions from `../bindcraft.py`
   - Handle real file I/O and model loading

3. **Add 3D Visualization**:
   - Integrate PyVista widgets in `results_panel.py`
   - Load and render PDB structures
   - Implement interactive controls

4. **Add Analytics Plotting**:
   - Integrate PyQtGraph widgets
   - Load and display PAE, pLDDT, and contact map plots
   - Support plot export

5. **Add File Management**:
   - Load/save JSON configuration files
   - Handle PDB file loading with structure validation
   - Manage output directories

## License

Same as parent BindCraft project.
