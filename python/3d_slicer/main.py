import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from stl_loader import STLLoader
from slicer_engine import SlicerEngine
from gcode_generator import GCodeGenerator
from layer_preview import LayerPreview
import os

class SlicerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Print Slicer")
        self.root.geometry("1000x700")
        
        # Initialize components
        self.stl_loader = STLLoader()
        self.slicer = SlicerEngine()
        self.gcode_gen = GCodeGenerator()
        
        # Data storage
        self.mesh = None
        self.layers = None
        self.gcode = None
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create main frames
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        
        # Left panel for controls
        self.control_frame = ttk.LabelFrame(self.main_frame, text="Controls", padding="10")
        self.control_frame.grid(row=0, column=0, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # File operations
        ttk.Label(self.control_frame, text="File Operations", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.load_btn = ttk.Button(self.control_frame, text="Load STL File", command=self.load_stl)
        self.load_btn.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Slicer settings
        ttk.Label(self.control_frame, text="Slicer Settings", font=('Arial', 12, 'bold')).grid(row=2, column=0, columnspan=2, pady=(20, 10))
        
        ttk.Label(self.control_frame, text="Layer Height (mm):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.layer_height_var = tk.StringVar(value="2.0")  # Increased for better visibility
        ttk.Entry(self.control_frame, textvariable=self.layer_height_var, width=10).grid(row=3, column=1, sticky=tk.E, pady=2)
        
        ttk.Label(self.control_frame, text="Infill Density (%):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.infill_var = tk.StringVar(value="20")
        ttk.Entry(self.control_frame, textvariable=self.infill_var, width=10).grid(row=4, column=1, sticky=tk.E, pady=2)
        
        ttk.Label(self.control_frame, text="Print Speed (mm/s):").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.speed_var = tk.StringVar(value="50")
        ttk.Entry(self.control_frame, textvariable=self.speed_var, width=10).grid(row=5, column=1, sticky=tk.E, pady=2)
        
        ttk.Label(self.control_frame, text="Nozzle Temp (°C):").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.temp_var = tk.StringVar(value="200")
        ttk.Entry(self.control_frame, textvariable=self.temp_var, width=10).grid(row=6, column=1, sticky=tk.E, pady=2)
        
        ttk.Label(self.control_frame, text="Bed Temp (°C):").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.bed_temp_var = tk.StringVar(value="60")
        ttk.Entry(self.control_frame, textvariable=self.bed_temp_var, width=10).grid(row=7, column=1, sticky=tk.E, pady=2)
        
        # Process buttons
        self.slice_btn = ttk.Button(self.control_frame, text="Slice Model", command=self.slice_model, state='disabled')
        self.slice_btn.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 2))
        
        self.generate_gcode_btn = ttk.Button(self.control_frame, text="Generate G-Code", command=self.generate_gcode, state='disabled')
        self.generate_gcode_btn.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        self.save_gcode_btn = ttk.Button(self.control_frame, text="Save G-Code", command=self.save_gcode, state='disabled')
        self.save_gcode_btn.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Status and info
        ttk.Label(self.control_frame, text="Model Info", font=('Arial', 12, 'bold')).grid(row=11, column=0, columnspan=2, pady=(20, 10))
        
        self.info_text = tk.Text(self.control_frame, height=6, width=25, state='disabled')
        self.info_text.grid(row=12, column=0, columnspan=2, pady=2)
        
        # Right panel for preview
        self.preview_frame = ttk.LabelFrame(self.main_frame, text="Layer Preview", padding="10")
        self.preview_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Preview canvas
        self.preview = LayerPreview(self.preview_frame)
        self.preview.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Layer navigation
        nav_frame = ttk.Frame(self.preview_frame)
        nav_frame.grid(row=1, column=0, pady=10)
        
        ttk.Label(nav_frame, text="Layer:").grid(row=0, column=0, padx=5)
        self.layer_var = tk.IntVar()
        self.layer_scale = ttk.Scale(nav_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                   variable=self.layer_var, command=self.update_layer_preview,
                                   length=300, state='disabled')
        self.layer_scale.grid(row=0, column=1, padx=5)
        
        self.layer_label = ttk.Label(nav_frame, text="0/0")
        self.layer_label.grid(row=0, column=2, padx=5)
        
        # Status bar
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready to load STL file...")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress = ttk.Progressbar(self.status_frame, mode='determinate')
        self.progress.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        self.status_frame.columnconfigure(1, weight=1)
        
    def load_stl(self):
        file_path = filedialog.askopenfilename(
            title="Select STL File",
            filetypes=[("STL files", "*.stl"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.status_label.config(text="Loading STL file...")
                self.progress.config(value=0)
                self.root.update()
                
                self.mesh = self.stl_loader.load(file_path)
                print(f"Loaded mesh with {len(self.mesh.triangles)} triangles")
                
                # Update info display
                self.update_model_info()
                
                # Enable slice button
                self.slice_btn.config(state='normal')
                
                self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
                self.progress.config(value=100)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load STL file:\n{str(e)}")
                self.status_label.config(text="Error loading file")
                print(f"Error loading STL: {e}")
                
    def update_model_info(self):
        if self.mesh is None:
            return
            
        bounds = self.mesh.bounds
        size = bounds[1] - bounds[0]
        
        info = f"Triangles: {len(self.mesh.triangles)}\n"
        info += f"Size (mm):\n"
        info += f"  X: {size[0]:.1f}\n"
        info += f"  Y: {size[1]:.1f}\n"
        info += f"  Z: {size[2]:.1f}\n"
        info += f"Volume: {self.mesh.volume:.1f} mm³"
        
        self.info_text.config(state='normal')
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
        self.info_text.config(state='disabled')
        
    def slice_model(self):
        if self.mesh is None:
            return
            
        try:
            layer_height = float(self.layer_height_var.get())
            
            self.status_label.config(text="Slicing model...")
            self.progress.config(value=0)
            self.root.update()
            
            self.layers = self.slicer.slice(self.mesh, layer_height, progress_callback=self.update_progress)
            print(f"Created {len(self.layers)} layers")
            
            # Debug: Check first few layers
            for i, layer in enumerate(self.layers[:3]):
                print(f"Layer {i}: {len(layer.perimeters)} perimeters, {len(layer.infill_lines)} infill lines")
            
            # Update layer navigation
            if self.layers:
                self.layer_scale.config(to=len(self.layers)-1, state='normal')
                self.layer_var.set(0)
                self.update_layer_preview()
                
                # Enable G-code generation
                self.generate_gcode_btn.config(state='normal')
                
            self.status_label.config(text=f"Sliced into {len(self.layers)} layers")
            self.progress.config(value=100)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to slice model:\n{str(e)}")
            self.status_label.config(text="Error slicing model")
            print(f"Error slicing: {e}")
            
    def generate_gcode(self):
        if self.layers is None:
            return
            
        try:
            settings = {
                'layer_height': float(self.layer_height_var.get()),
                'infill_density': float(self.infill_var.get()) / 100.0,
                'print_speed': float(self.speed_var.get()),
                'nozzle_temp': int(self.temp_var.get()),
                'bed_temp': int(self.bed_temp_var.get())
            }
            
            self.status_label.config(text="Generating G-code...")
            self.progress.config(value=0)
            self.root.update()
            
            self.gcode = self.gcode_gen.generate(self.layers, settings, progress_callback=self.update_progress)
            
            # Enable save button
            self.save_gcode_btn.config(state='normal')
            
            self.status_label.config(text=f"Generated {len(self.gcode.split(chr(10)))} lines of G-code")
            self.progress.config(value=100)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate G-code:\n{str(e)}")
            self.status_label.config(text="Error generating G-code")
            
    def save_gcode(self):
        if self.gcode is None:
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save G-Code File",
            defaultextension=".gcode",
            filetypes=[("G-code files", "*.gcode"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.gcode)
                    
                self.status_label.config(text=f"Saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "G-code saved successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save G-code:\n{str(e)}")
                
    def update_layer_preview(self, *args):
        if self.layers is None:
            return
            
        layer_idx = self.layer_var.get()
        if 0 <= layer_idx < len(self.layers):
            layer = self.layers[layer_idx]
            print(f"Showing layer {layer_idx}: {len(layer.perimeters)} perimeters, {len(layer.infill_lines)} infill lines")
            self.preview.show_layer(layer)
            self.layer_label.config(text=f"{layer_idx + 1}/{len(self.layers)}")
            
    def update_progress(self, value):
        self.progress.config(value=value)
        self.root.update()

def main():
    root = tk.Tk()
    app = SlicerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()