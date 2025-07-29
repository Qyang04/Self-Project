# visualize_huffman.py

import tkinter as tk
from tkinter import simpledialog, messagebox
# Import the modified function and Node class from your original script
from huffman_encoder import huffman_encoding

# --- Constants for Drawing ---
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 700
NODE_RADIUS = 25
Y_SPACING = 90
NODE_COLOR = "#cceeff"
LEAF_COLOR = "#d4edda"
LINE_COLOR = "#555555"
TEXT_COLOR = "#000000"

# A Tkinter application to visualize a Huffman Tree.
class HuffmanVisualizer:
    def __init__(self, root_node):
        if not root_node or (not root_node.left and not root_node.right):
            messagebox.showinfo("Info", "Cannot visualize a tree for a single unique character.")
            return

        self.window = tk.Tk()
        self.window.title("Huffman Tree Visualization")
        
        self.canvas = tk.Canvas(self.window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.canvas.pack()

        self.draw_tree(root_node)
        
        self.window.mainloop()

    def draw_tree(self, root_node):
        """
        Kicks off the recursive drawing process for the tree.
        """
        # Start drawing from the top-center of the canvas
        initial_x = CANVAS_WIDTH / 2
        initial_y = 50
        # The initial horizontal offset is a quarter of the canvas width
        initial_x_offset = CANVAS_WIDTH / 4

        self._draw_node_recursive(root_node, initial_x, initial_y, initial_x_offset)

    def _draw_node_recursive(self, node, x, y, x_offset):
        """
        Recursively draws a node and the lines connecting to its children.
        """
        if node is None:
            return

        # --- 1. Draw the current node ---
        is_leaf = node.char is not None
        node_fill = LEAF_COLOR if is_leaf else NODE_COLOR
        
        # Draw the oval for the node
        self.canvas.create_oval(
            x - NODE_RADIUS, y - NODE_RADIUS,
            x + NODE_RADIUS, y + NODE_RADIUS,
            fill=node_fill, outline=LINE_COLOR, width=2
        )

        # Prepare and draw the text inside the node
        if is_leaf:
            display_text = f"'{node.char}'\n({node.freq})"
        else:
            display_text = f"({node.freq})"
            
        self.canvas.create_text(x, y, text=display_text, fill=TEXT_COLOR, font=("Arial", 10, "bold"))

        # --- 2. Process and draw children nodes ---
        child_y = y + Y_SPACING
        
        # Draw left child
        if node.left:
            child_x = x - x_offset
            # Draw line to child
            self.canvas.create_line(x, y + NODE_RADIUS, child_x, child_y - NODE_RADIUS, fill=LINE_COLOR, width=2)
            # Draw '0' label on the path
            self.canvas.create_text((x + child_x) / 2, (y + child_y) / 2 - 10, text="0", fill="blue", font=("Arial", 12, "bold"))
            # Recurse
            self._draw_node_recursive(node.left, child_x, child_y, x_offset / 2)

        # Draw right child
        if node.right:
            child_x = x + x_offset
            # Draw line to child
            self.canvas.create_line(x, y + NODE_RADIUS, child_x, child_y - NODE_RADIUS, fill=LINE_COLOR, width=2)
            # Draw '1' label on the path
            self.canvas.create_text((x + child_x) / 2, (y + child_y) / 2 - 10, text="1", fill="red", font=("Arial", 12, "bold"))
            # Recurse
            self._draw_node_recursive(node.right, child_x, child_y, x_offset / 2)


def main():
    """
    Main function to get user input and launch the visualizer.
    """
    # Create a dummy root window to host the dialog
    root_for_dialog = tk.Tk()
    root_for_dialog.withdraw() # Hide the dummy window

    text = simpledialog.askstring("Input", "Enter text to encode and visualize:")

    if not text:
        messagebox.showerror("Error", "Input text cannot be empty.")
        return
        
    if len(set(text)) <= 1:
        messagebox.showinfo("Info", f"The original string can be encoded, but a tree cannot be drawn for a single unique character.\n\nInput: '{text}'")
        return

    # Use the modified function to get both the root and the codes
    root_node, _ = huffman_encoding(text)

    # Launch the visualizer application
    HuffmanVisualizer(root_node)

if __name__ == "__main__":
    main()