import tkinter as tk
import numpy as np

class LayerPreview:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, width=400, height=400, bg='white')
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<MouseWheel>', self.on_zoom)
        
        # View parameters
        self.offset_x = 200
        self.offset_y = 200
        self.scale = 5.0
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.current_layer = None  # Store current layer for redrawing
        
    def show_layer(self, layer):
        """Display a layer on the canvas"""
        self.current_layer = layer
        self._redraw()
        
    def _redraw(self):
        """Redraw the current layer"""
        self.canvas.delete("all")
        
        if not self.current_layer:
            return
            
        # Draw coordinate axes
        self._draw_axes()
        
        # Draw perimeters
        perimeter_count = 0
        for polygon in self.current_layer.perimeters:
            self._draw_polygon(polygon, 'blue', 2)
            perimeter_count += 1
            
        # Draw infill
        infill_count = 0
        for infill_line in self.current_layer.infill_lines:
            self._draw_line(infill_line, 'red', 1)
            infill_count += 1
            
        # Draw layer info
        info_text = f"Layer Z: {self.current_layer.z_height:.2f}mm"
        if perimeter_count > 0:
            info_text += f"\nPerimeters: {perimeter_count}"
        if infill_count > 0:
            info_text += f"\nInfill lines: {infill_count}"
        if perimeter_count == 0 and infill_count == 0:
            info_text += "\nNo geometry found"
            
        self.canvas.create_text(10, 10, anchor='nw', 
                              text=info_text, 
                              fill='black', font=('Arial', 10))
                              
    def _draw_axes(self):
        """Draw coordinate axes for reference"""
        # X axis (red)
        x1, y1 = self._world_to_screen(-50, 0)
        x2, y2 = self._world_to_screen(50, 0)
        self.canvas.create_line(x1, y1, x2, y2, fill='red', width=1, dash=(5, 5))
        self.canvas.create_text(x2 + 5, y2, text='X', fill='red', font=('Arial', 8))
        
        # Y axis (green)
        x1, y1 = self._world_to_screen(0, -50)
        x2, y2 = self._world_to_screen(0, 50)
        self.canvas.create_line(x1, y1, x2, y2, fill='green', width=1, dash=(5, 5))
        self.canvas.create_text(x2, y2 - 10, text='Y', fill='green', font=('Arial', 8))
        
    def _draw_polygon(self, polygon, color, width):
        """Draw a polygon on the canvas"""
        try:
            if hasattr(polygon, 'exterior'):
                coords = list(polygon.exterior.coords)
            else:
                coords = polygon
                
            if len(coords) < 3:
                return
                
            screen_coords = []
            for x, y in coords:
                sx, sy = self._world_to_screen(x, y)
                screen_coords.extend([sx, sy])
                
            if len(screen_coords) >= 6:  # At least 3 points
                self.canvas.create_polygon(screen_coords, outline=color, fill='', width=width)
                
        except Exception as e:
            print(f"Error drawing polygon: {e}")
            pass
            
    def _draw_line(self, line_coords, color, width):
        """Draw a line on the canvas"""
        if len(line_coords) < 2:
            return
            
        try:
            screen_coords = []
            for point in line_coords:
                if len(point) >= 2:
                    sx, sy = self._world_to_screen(point[0], point[1])
                    screen_coords.extend([sx, sy])
                    
            if len(screen_coords) >= 4:  # At least 2 points
                self.canvas.create_line(screen_coords, fill=color, width=width)
        except Exception as e:
            print(f"Error drawing line: {e}")
            pass
            
    def _world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x * self.scale + self.offset_x
        screen_y = -world_y * self.scale + self.offset_y  # Flip Y axis
        return screen_x, screen_y
        
    def _screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        world_x = (screen_x - self.offset_x) / self.scale
        world_y = -(screen_y - self.offset_y) / self.scale  # Flip Y axis
        return world_x, world_y
        
    def on_click(self, event):
        """Handle mouse click for panning"""
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        
    def on_drag(self, event):
        """Handle mouse drag for panning"""
        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y
        
        self.offset_x += dx
        self.offset_y += dy
        
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        
        # Redraw with new offset
        self._redraw()
        
    def on_zoom(self, event):
        """Handle mouse wheel for zooming"""
        if event.delta > 0:
            self.scale *= 1.1
        else:
            self.scale /= 1.1
            
        # Limit zoom range
        self.scale = max(0.1, min(50.0, self.scale))
        
        # Redraw with new scale
        self._redraw()

