# BindCraft GUI Development Plan

## 1. Vision and Goals

The goal is to create an intuitive, transparent desktop application for BindCraft using PySide6. This GUI will expose the three-stage protein design pipeline, allowing users to review and control each step: backbone generation (hallucination), physics validation, and sequence optimization (MPNN). The application provides visual feedback and interactivity at each stage, making the design process transparent and controllable.

## 2. Tech Stack

*   **GUI Framework:** **PySide6** (Qt for Python) for the core application structure, widgets, and event handling.
*   **Backend Logic:** The existing **BindCraft Python scripts** (`bindcraft.py`, `functions/`) will be split into three separate workers for each pipeline stage.
*   **3D Visualization:** **PyVista** with `pyvistaqt.BackgroundPlotter` for rendering molecular structures from PDB files with interactive controls.
*   **2D Plotting:** **PyQtGraph** for high-performance real-time plotting of metrics, trajectories, and analytics.
*   **Trajectory Visualization:** Load pickle files from ColabDesign to create interactive trajectory viewers with iteration scrubbing.
*   **Concurrency:** **QThread** workers for each pipeline stage to keep the GUI responsive.
*   **Packaging:** **PyInstaller** to bundle the application into a standalone executable.

## 3. Core Architecture: Three-Stage Pipeline

The GUI is organized into **three sequential stages**, each with its own configuration panel and results panel. Users must complete one stage before proceeding to the next, but can go back to modify earlier stages.

```
Stage 1: Hallucination → Stage 2: Validation → Stage 3: MPNN Optimization
  (Generate Backbone)      (Physics Check)        (Sequence Design)
```

---

## 4. Main Window Layout

### **Top Navigation Bar**
*   **Stage Progress Indicator:** Visual breadcrumb showing current stage
    ```
    [1. Hallucination] → [2. Validation] → [3. MPNN Optimization]
         (Active)            (Locked)            (Locked)
    ```
*   **Stage Tabs:** `QTabWidget` with three tabs, locked until prerequisites are met

### **Each Stage Tab Structure**
```
┌─────────────────────────────────────────────────────────────┐
│  Stage X: [Name]                                            │
├──────────────────┬──────────────────────────────────────────┤
│                  │                                          │
│  Configuration   │  Results & Visualization                 │
│  Panel           │                                          │
│  (Left 1/3)      │  (Right 2/3)                            │
│                  │                                          │
│  - Settings      │  - Results Table                         │
│  - Parameters    │  - 3D Viewer                            │
│  - Run Controls  │  - Plots/Analytics                      │
│                  │                                          │
└──────────────────┴──────────────────────────────────────────┘
```

---

## 5. Stage 1: Hallucination (Backbone Generation)

### **Purpose**
Generate 3D protein backbone structures that bind to the target using AlphaFold2-based optimization.

### **Configuration Panel (Left)**

*   **Target Setup**
    *   Load Target PDB button
    *   3D preview of target structure (PyVista widget, small)
    *   Target Chains input (e.g., "A,B")
    *   Target Hotspot Residues input (e.g., "24,25,26")
    *   Binder Name input

*   **Design Parameters**
    *   Binder Length: Min/Max spin boxes
    *   Number of Trajectories to generate (e.g., 10, 50, 100)
    *   Advanced Settings dropdown (load different `advanced.json` profiles)
    *   Helicity preference slider (optional)

*   **Run Controls**
    *   **[Generate Trajectories]** button
    *   Progress bar (X/Y trajectories complete)
    *   **[Stop]** button during execution
    *   Log viewer (collapsible, shows real-time output)

### **Results Panel (Right)**

*   **Trajectory Table** (`QTableWidget`, top half)
    *   Columns: `[✓] Name | pLDDT | pTM | i_pTM | PAE | i_PAE | Length | Status`
    *   Checkboxes for selecting trajectories to validate
    *   Click row to view in detail below
    *   Sortable by columns

*   **Trajectory Detail Viewer** (`QTabWidget`, bottom half)
    *   **Tab: 3D Structure**
        *   PyVista viewer showing trajectory structure
        *   Target (gray) + Binder (colored by pLDDT)
        *   Controls: rotate, zoom, color scheme selector

    *   **Tab: Optimization Trajectory**
        *   Load from pickle file (`Trajectory/Pickle/{name}.pickle`)
        *   PyQtGraph plot: pLDDT, pTM, PAE, loss over iterations
        *   Iteration slider to scrub through optimization
        *   3D structure updates as slider moves (show structure evolution)

    *   **Tab: Metrics**
        *   Display all metrics from `trajectory_stats.csv` for selected design
        *   Text-based summary of quality indicators

*   **Navigation**
    *   **[Validate Selected (N) →]** button (bottom right)
        *   Enabled when ≥1 trajectory selected
        *   Moves to Stage 2 with selected trajectories

---

## 6. Stage 2: Validation (Physics Check)

### **Purpose**
Run physics-based validation on selected trajectories: relaxation, clash detection, interface scoring, secondary structure analysis.

### **Configuration Panel (Left)**

*   **Selected Trajectories Display**
    *   List of trajectories passed from Stage 1
    *   Shows: Name, pLDDT, pTM
    *   **[← Back to Stage 1]** to modify selection

*   **Validation Settings**
    *   PyRosetta relaxation options (checkboxes)
        *   Run relaxation (default: on)
        *   Calculate secondary structure
        *   Compute interface metrics
    *   Clash tolerance slider (Å)
    *   **[Load Validation Preset]** dropdown

*   **Run Controls**
    *   **[Run Validation]** button
    *   Progress bar (X/Y trajectories validated)
    *   **[Pause]** / **[Stop]** buttons
    *   Log viewer (collapsible)

### **Results Panel (Right)**

*   **Validation Results Table** (`QTableWidget`, top half)
    *   Columns: `[✓] Name | Clashes | dG | dSASA | Shape Comp | Interface Residues | Status`
    *   Status: ✅ Pass / ⚠️ Warning / ❌ Fail (based on thresholds)
    *   Checkboxes for selecting validated designs for MPNN
    *   Click row to view details

*   **Validation Detail Viewer** (`QTabWidget`, bottom half)
    *   **Tab: Interface Visualization**
        *   PyVista 3D viewer
        *   Highlight interface residues
        *   Color by: dG contribution, clash severity, or residue type
        *   Show relaxed vs unrelaxed structure (toggle)

    *   **Tab: Metrics Breakdown**
        *   Detailed scores from `score_interface()`:
            *   Binding energy (dG), dSASA, shape complementarity
            *   H-bonds, unsatisfied H-bonds
            *   Hydrophobicity, PackStat
        *   Secondary structure percentages (helix/beta/loop)
        *   Target RMSD (how much target moved)

    *   **Tab: Comparison**
        *   Compare multiple selected designs side-by-side
        *   Overlay structures in 3D
        *   Metric comparison table

*   **Filter Controls**
    *   **[Edit Filter Thresholds]** button → opens dialog
    *   Shows current pass/fail criteria
    *   Can adjust on-the-fly and re-evaluate

*   **Navigation**
    *   **[← Back to Hallucination]** (re-select trajectories)
    *   **[Optimize Selected (N) →]** button
        *   Moves to Stage 3 with validated designs

---

## 7. Stage 3: MPNN Optimization (Sequence Design)

### **Purpose**
Use ProteinMPNN to generate optimized amino acid sequences for validated backbones, then predict and filter with AlphaFold2.

### **Configuration Panel (Left)**

*   **Selected Designs Display**
    *   List of validated designs passed from Stage 2
    *   Shows: Name, dG, Shape Comp
    *   **[← Back to Stage 2]** to modify selection

*   **MPNN Settings**
    *   Number of sequences per design (default: 50)
    *   Sampling temperature slider (0.1 - 1.0)
    *   Backbone noise slider
    *   Fix interface residues checkbox
    *   Omit amino acids (e.g., "C" for no cysteines)
    *   **[Load MPNN Preset]** dropdown

*   **AF2 Validation Settings**
    *   Number of recycles for prediction
    *   Which AF2 models to use (checkboxes: model 1-5)
    *   Use multimer checkbox

*   **Filter Settings (Quick Access)**
    *   Key filters: pLDDT, pTM, i_pTM, dG, Shape Comp
    *   Sliders or spin boxes for thresholds
    *   **[Edit All Filters]** → full filter dialog

*   **Run Controls**
    *   **[Generate & Filter Sequences]** button
    *   Target accepted designs (stop when reached)
    *   Progress: "Design 1/3: Sequence 25/50 tested, 2 accepted"
    *   **[Pause]** / **[Stop]** buttons
    *   Log viewer (collapsible)

### **Results Panel (Right)**

*   **Accepted Designs Table** (`QTableWidget`, top half)
    *   Columns: `[✓] Name | Base Design | Sequence | pLDDT | pTM | i_pTM | dG | Shape Comp | Status`
    *   Real-time updates as designs pass filters
    *   Checkboxes for export selection
    *   Click row to view details
    *   Sortable by all metrics

*   **Design Detail Viewer** (`QTabWidget`, bottom half)
    *   **Tab: Structure Comparison**
        *   PyVista 3D viewer
        *   Show: MPNN design vs original trajectory
        *   Superimpose binder structures
        *   Color by: pLDDT, RMSD deviation, or sequence conservation

    *   **Tab: Sequence Analysis**
        *   Sequence alignment view (MPNN vs trajectory)
        *   Highlight mutations
        *   Show which residues are at interface
        *   Amino acid properties (hydrophobicity, charge)

    *   **Tab: Predictions**
        *   Show predictions from all 5 AF2 models (if run)
        *   Per-model metrics table
        *   Average vs individual model scores
        *   PAE/pLDDT plots from AF2

    *   **Tab: Binder Alone**
        *   Show binder monomer prediction
        *   Check if binder folds independently
        *   Compare binder-alone pLDDT to complex pLDDT

*   **Filter Analysis**
    *   Live statistics: "Tested: 150, Passed: 12 (8%), Failed pLDDT: 85, Failed dG: 43..."
    *   **[Show Failure Breakdown]** → chart of which filters reject most

*   **Export & Finalization**
    *   **[Export Selected PDBs]** → save to folder
    *   **[Generate Report]** → CSV/PDF summary
    *   **[Export FASTA Sequences]**
    *   **[← Back to Validation]**
    *   **[Start New Design]** → reset to Stage 1

---

## 8. Backend Integration: Worker Threads

### **Worker Architecture**

Each stage has a dedicated `QThread` worker:

*   **`HallucinationWorker(QThread)`**
    *   Input: target settings, design parameters
    *   Runs: Lines 72-163 of `bindcraft.py` (hallucination loop only)
    *   Signals: `trajectory_complete(dict)`, `log_message(str)`, `progress(int, int)`
    *   Output: List of trajectory data (PDB paths, metrics, pickle paths)

*   **`ValidationWorker(QThread)`**
    *   Input: Selected trajectory list, validation settings
    *   Runs: Lines 126-163 of `bindcraft.py` (relaxation + scoring)
    *   Signals: `validation_complete(dict)`, `log_message(str)`, `progress(int, int)`
    *   Output: Validation metrics for each trajectory

*   **`MPNNWorker(QThread)`**
    *   Input: Validated design list, MPNN settings, filters
    *   Runs: Lines 168-440 of `bindcraft.py` (MPNN + AF2 prediction + filtering)
    *   Signals: `design_accepted(dict)`, `sequence_tested(dict)`, `log_message(str)`, `progress(int, int, int, int)`
    *   Output: Final accepted designs with full metrics

### **Signal/Slot Communication**

Workers emit signals, main GUI connects to slots:

```python
# Example: Stage 1
self.hallucination_worker.trajectory_complete.connect(
    self.hallucination_panel.add_trajectory_to_table)

self.hallucination_worker.log_message.connect(
    self.hallucination_panel.append_log)

self.hallucination_worker.progress.connect(
    self.hallucination_panel.update_progress)
```

---

## 9. Data Flow Between Stages

### **Stage 1 → Stage 2**
```python
selected_trajectories = [
    {
        'name': 'design1_l80_s12345',
        'pdb_path': '/path/to/Trajectory/design1_l80_s12345.pdb',
        'relaxed_pdb_path': '/path/to/Trajectory/Relaxed/design1_l80_s12345.pdb',
        'pickle_path': '/path/to/Trajectory/Pickle/design1_l80_s12345.pickle',
        'metrics': {'plddt': 85.3, 'ptm': 0.82, ...},
        'length': 80,
        'seed': 12345
    },
    ...
]
```

### **Stage 2 → Stage 3**
```python
validated_designs = [
    {
        'name': 'design1_l80_s12345',
        'trajectory_pdb': '/path/to/Trajectory/design1_l80_s12345.pdb',
        'relaxed_pdb': '/path/to/Trajectory/Relaxed/design1_l80_s12345.pdb',
        'interface_residues': 'B24,B25,B26,B30',
        'validation_metrics': {'dG': -18.3, 'clashes': 0, ...},
        'length': 80,
        'binder_chain': 'B'
    },
    ...
]
```

### **Stage 3 Output**
```python
final_designs = [
    {
        'name': 'design1_l80_s12345_mpnn1',
        'base_trajectory': 'design1_l80_s12345',
        'sequence': 'MLKEVQGADTN...',
        'pdb_path': '/path/to/MPNN/Relaxed/design1_l80_s12345_mpnn1_model3.pdb',
        'all_model_pdbs': [...],
        'metrics': {'plddt': 92.3, 'dG': -21.5, ...},
        'mpnn_score': 0.85,
        'seqid': 0.73
    },
    ...
]
```

---

## 10. Additional Features

### **Trajectory Animation Alternative**

Instead of HTML animations from `af_model.animate()`:

1. **Load pickle file** containing optimization trajectory
2. **Extract coordinates at each iteration**
3. **Use PyVista + slider widget**:
   ```python
   iteration_slider.valueChanged.connect(update_structure_at_iteration)
   ```
4. **Display in 3D viewer** with real-time updates
5. **Benefits**: Interactive rotation/zoom, no video encoding, higher quality

### **Configuration Presets**

*   **Load/Save Workflows**: Save entire 3-stage configuration as `.bcproj` file
*   **Preset Library**: Pre-configured settings for common use cases
    *   "High Quality (Slow)"
    *   "Fast Screening"
    *   "Beta-Sheet Binders"
    *   "Helical Binders"

### **Batch Mode**

*   Run multiple targets sequentially
*   Queue system for overnight runs
*   Email/notification on completion

### **Comparison Tools**

*   Compare designs across stages
*   Overlay multiple structures in 3D
*   Metric correlation plots (e.g., pLDDT vs dG)

---

## 11. File Structure

```
gui/
├── main.py                          # Application entry point
├── main_window.py                   # Main window with stage tabs
├── workers/
│   ├── hallucination_worker.py     # Stage 1 worker
│   ├── validation_worker.py        # Stage 2 worker
│   └── mpnn_worker.py              # Stage 3 worker
├── panels/
│   ├── hallucination_panel.py      # Stage 1 UI
│   ├── validation_panel.py         # Stage 2 UI
│   └── mpnn_panel.py               # Stage 3 UI
├── widgets/
│   ├── structure_viewer.py         # PyVista 3D viewer widget
│   ├── trajectory_viewer.py        # Pickle-based trajectory viewer
│   ├── metrics_table.py            # Reusable results table
│   └── filter_editor.py            # Filter threshold editor
└── utils/
    ├── config_manager.py           # Load/save JSON configs
    ├── pdb_utils.py                # PDB loading/parsing
    └── data_handler.py             # Pass data between stages
```

---

## 12. Development Phases

### **Phase 1: Core Structure** ✅ (Mock complete)
- [x] Main window with 3 stage tabs
- [x] Basic configuration panels
- [x] Mock worker threads
- [x] Results tables

### **Phase 2: Stage 1 Integration**
- [ ] Real `HallucinationWorker` calling `binder_hallucination()`
- [ ] PyVista 3D structure viewer
- [ ] Pickle-based trajectory viewer with iteration slider
- [ ] PyQtGraph metrics plotting

### **Phase 3: Stage 2 Integration**
- [ ] `ValidationWorker` for physics validation
- [ ] Interface visualization (highlight residues)
- [ ] Detailed metrics display
- [ ] Filter evaluation UI

### **Phase 4: Stage 3 Integration**
- [ ] `MPNNWorker` for sequence optimization
- [ ] Sequence alignment viewer
- [ ] Multi-model AF2 prediction display
- [ ] Export functionality

### **Phase 5: Polish**
- [ ] Configuration presets
- [ ] Comparison tools
- [ ] Error handling & validation
- [ ] Documentation & tooltips

---

## 13. Key Design Principles

1. **Transparency**: Show the pipeline, don't hide it
2. **Control**: User decides what to validate/optimize, not automatic
3. **Visibility**: Real-time feedback at each stage
4. **Simplicity**: Clean interface, minimal tutorial text
5. **Interactivity**: Explore results through 3D viewers and plots
6. **Modularity**: Each stage independent, can iterate on one stage
