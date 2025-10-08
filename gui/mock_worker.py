"""
Mock Worker Thread for BindCraft GUI Demo
Simulates the pipeline execution without actually running structure prediction.
"""

import time
import random
from PySide6.QtCore import QThread, Signal


class MockWorker(QThread):
    """Mock worker thread that simulates BindCraft pipeline execution."""

    # Signals for communication with main thread
    signal_log_message = Signal(str)
    signal_progress_update = Signal(int)
    signal_design_accepted = Signal(dict)
    signal_run_finished = Signal()

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.is_running = True

    def run(self):
        """Execute the mock pipeline."""
        try:
            self.simulate_pipeline()
        except Exception as e:
            self.signal_log_message.emit(f"\n[ERROR] {str(e)}\n")
        finally:
            self.signal_run_finished.emit()

    def stop(self):
        """Stop the worker thread."""
        self.is_running = False

    def simulate_pipeline(self):
        """Simulate the BindCraft pipeline with mock output."""
        max_traj = self.config["max_trajectories"]
        target_designs = self.config["target_designs"]
        binder_name = self.config["binder_name"]

        # Initial setup messages
        self.signal_log_message.emit("=" * 60)
        self.signal_log_message.emit("BindCraft Pipeline Demo - Mock Execution")
        self.signal_log_message.emit("=" * 60)
        self.signal_log_message.emit("")
        self.signal_log_message.emit("[INFO] This is a DEMO version that simulates the pipeline.")
        self.signal_log_message.emit("[INFO] No actual structure generation will occur.")
        self.signal_log_message.emit("")
        self.signal_log_message.emit("Configuration:")
        self.signal_log_message.emit(f"  Binder Name: {binder_name}")
        self.signal_log_message.emit(f"  Target Chains: {self.config['target_chains']}")
        self.signal_log_message.emit(f"  Hotspot Residues: {self.config['hotspot_residues']}")
        self.signal_log_message.emit(f"  Binder Length: {self.config['min_length']}-{self.config['max_length']} aa")
        self.signal_log_message.emit(f"  Max Trajectories: {max_traj}")
        self.signal_log_message.emit(f"  Target Accepted: {target_designs}")
        self.signal_log_message.emit("")
        time.sleep(1)

        # Simulate initialization
        self.signal_log_message.emit("[INIT] Initializing BindCraft pipeline...")
        self.signal_log_message.emit("[INIT] Loading target structure...")
        time.sleep(0.5)
        self.signal_log_message.emit("[INIT] Setting up RFdiffusion model...")
        self.signal_log_message.emit("       → In real version: Use AlphaFold2/RFdiffusion for structure generation")
        time.sleep(0.5)
        self.signal_log_message.emit("[INIT] Setting up ProteinMPNN model...")
        self.signal_log_message.emit("       → In real version: Use ProteinMPNN for sequence design")
        time.sleep(0.5)
        self.signal_log_message.emit("[INIT] Setting up AlphaFold2 model...")
        self.signal_log_message.emit("       → In real version: Use AlphaFold2 for structure prediction and validation")
        time.sleep(0.5)
        self.signal_log_message.emit("[INIT] Setup complete!")
        self.signal_log_message.emit("")

        accepted_count = 0

        # Simulate trajectory generation
        for traj_num in range(1, max_traj + 1):
            if not self.is_running:
                break

            self.signal_log_message.emit(f"[TRAJ {traj_num}/{max_traj}] Starting trajectory {traj_num}...")

            # Simulate RFdiffusion
            time.sleep(0.3)
            self.signal_log_message.emit(f"[TRAJ {traj_num}] Running RFdiffusion for backbone generation...")
            self.signal_log_message.emit(f"            → Mock: Would use AlphaFold2/RFdiffusion to generate 3D backbone")

            # Simulate ProteinMPNN
            time.sleep(0.2)
            self.signal_log_message.emit(f"[TRAJ {traj_num}] Running ProteinMPNN for sequence design...")
            self.signal_log_message.emit(f"            → Mock: Would use ProteinMPNN to design optimal sequence")

            # Simulate AlphaFold2 prediction
            time.sleep(0.3)
            self.signal_log_message.emit(f"[TRAJ {traj_num}] Running AlphaFold2 structure prediction...")
            self.signal_log_message.emit(f"            → Mock: Would use AlphaFold2 to predict and validate structure")

            # Simulate filtering
            time.sleep(0.2)
            passed = random.random() < 0.15  # ~15% pass rate

            if passed:
                accepted_count += 1
                design_data = self.generate_mock_design(binder_name, accepted_count)

                self.signal_log_message.emit(f"[TRAJ {traj_num}] ✓ PASSED filters!")
                self.signal_log_message.emit(f"            → pLDDT: {design_data['plddt']:.1f}")
                self.signal_log_message.emit(f"            → PAE: {design_data['pae']:.1f}")
                self.signal_log_message.emit(f"            → dSASA: {design_data['dsasa']:.0f}")
                self.signal_log_message.emit(f"            → Shape Complementarity: {design_data['shape_comp']:.1f}")

                self.signal_design_accepted.emit(design_data)

                if accepted_count >= target_designs:
                    self.signal_log_message.emit("")
                    self.signal_log_message.emit(f"[SUCCESS] Reached target of {target_designs} accepted designs!")
                    break
            else:
                self.signal_log_message.emit(f"[TRAJ {traj_num}] ✗ Failed filters")

            # Update progress
            progress = int((traj_num / max_traj) * 100)
            self.signal_progress_update.emit(progress)

            time.sleep(0.1)

        # Final summary
        self.signal_log_message.emit("")
        self.signal_log_message.emit("=" * 60)
        self.signal_log_message.emit("Pipeline Complete!")
        self.signal_log_message.emit("=" * 60)
        self.signal_log_message.emit(f"Total trajectories run: {min(traj_num, max_traj)}")
        self.signal_log_message.emit(f"Accepted designs: {accepted_count}")
        self.signal_log_message.emit("")
        self.signal_log_message.emit("[DEMO] In the real version, this would:")
        self.signal_log_message.emit("  • Use AlphaFold2/RFdiffusion for de novo backbone generation")
        self.signal_log_message.emit("  • Use ProteinMPNN for sequence design")
        self.signal_log_message.emit("  • Use AlphaFold2 for structure prediction and validation")
        self.signal_log_message.emit("  • Generate 3D structures viewable in PyVista")
        self.signal_log_message.emit("  • Generate analysis plots (PAE, pLDDT, contacts)")
        self.signal_log_message.emit("  • Save PDB files and statistics to disk")
        self.signal_log_message.emit("")

        self.signal_progress_update.emit(100)

    def generate_mock_design(self, binder_name, design_num):
        """Generate mock design data."""
        # Generate realistic-looking random values
        plddt = random.uniform(75, 95)
        pae = random.uniform(2, 12)
        dsasa = random.uniform(500, 1200)
        shape_comp = random.uniform(55, 85)
        dg = random.uniform(-25, -10)
        length = random.randint(self.config["min_length"], self.config["max_length"])

        return {
            "name": f"{binder_name}_design_{design_num:03d}",
            "plddt": plddt,
            "pae": pae,
            "dsasa": dsasa,
            "shape_comp": shape_comp,
            "dg": dg,
            "length": length,
            "status": "Accepted"
        }
