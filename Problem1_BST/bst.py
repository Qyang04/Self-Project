import tkinter as tk
from tkinter import messagebox

class Node:
    # A node in the binary search tree.
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key

# A binary search tree with insert, delete, search, and inorder traversal.
class BST:
    def __init__(self):
        self.root = None

    # Insert a key into the BST. Duplicates go to the right.
    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:  # key >= node.key - duplicates go to right
            node.right = self._insert(node.right, key)
        return node

    # Delete node with the given key from the BST.
    def delete(self, key):
        self.root, _ = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node, False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
            return node, deleted
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
            return node, deleted
        else:  # key == node.key - found the node to delete
            # Case 1: No children - simply remove the node
            if node.left is None and node.right is None:
                return None, True
            # Case 2: One child - replace with the child
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            # Case 3: Two children - replace with inorder successor
            succ = self._min_value_node(node.right)
            node.key = succ.key
            node.right, _ = self._delete(node.right, succ.key)
            return node, True

    def _min_value_node(self, node):
        # Find the leftmost node (minimum value) in the subtree.
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Search for a value in the BST and return the node with the given key, or None if not found.
    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    # Return a list of keys in sorted (inorder) order.
    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    # Recursively traverse: left subtree, current node, right subtree.
    def _inorder_recursive(self, node, result):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

# Uses Tkinter GUI for visualizing and interacting with a BST
class BSTApp:
    def __init__(self, root):
        self.bst = BST()
        self.root = root
        self.root.title("BST Visualizer")
        
        # Create canvas for tree visualization
        self.canvas = tk.Canvas(root, width=800, height=400, bg="white")
        self.canvas.pack()

        # Create control panel (insert, delete, search, print sorted)
        frame = tk.Frame(root)
        frame.pack()
        self.entry = tk.Entry(frame, width=10)
        self.entry.pack(side=tk.LEFT)
        tk.Button(frame, text="Insert", command=self.insert).pack(side=tk.LEFT)
        tk.Button(frame, text="Delete", command=self.delete).pack(side=tk.LEFT)
        tk.Button(frame, text="Search", command=self.search).pack(side=tk.LEFT)
        tk.Button(frame, text="Print Sorted", command=self.print_sorted).pack(side=tk.LEFT)

        # Status display (shows the status of the BST)
        self.status = tk.Label(root, text="", fg="blue")
        self.status.pack()

    # Insert a value from the entry field into the BST
    def insert(self):
        val = self.entry.get()
        if not val.isdigit():
            messagebox.showerror("Error", "Please enter an integer.")
            return
        val = int(val)
        self.bst.insert(val)
        self.status.config(text=f"Inserted {val}")
        self.redraw()
        self.entry.delete(0, tk.END)

    # Delete a value from the BST
    def delete(self):
        val = self.entry.get()
        if not val.isdigit():
            messagebox.showerror("Error", "Please enter an integer.")
            return
        val = int(val)
        self.bst.delete(val)
        self.status.config(text=f"Deleted {val}")
        self.redraw()
        self.entry.delete(0, tk.END)

    # Search for a value in the BST and highlight it
    def search(self):
        val = self.entry.get()
        if not val.isdigit():
            messagebox.showerror("Error", "Please enter an integer.")
            return
        val = int(val)
        found_node = self.bst.search(val)
        if found_node:
            self.status.config(text=f"{val} found in BST.")
        else:
            self.status.config(text=f"{val} not found in BST.")
        self.redraw(highlight_node=found_node)
        self.entry.delete(0, tk.END)

    # Display the BST values in sorted order
    def print_sorted(self):
        sorted_values = self.bst.inorder()
        messagebox.showinfo("BST Inorder (Sorted)", " ".join(map(str, sorted_values)))

    # Redraw the entire tree visualization.
    def redraw(self, highlight_node=None):
        self.canvas.delete("all")
        if self.bst.root:
            self._draw_tree(self.bst.root, 400, 40, 200, highlight_node)

    # Recursively draw the tree nodes and connections
    def _draw_tree(self, node, x, y, dx, highlight_node=None):
        # Draw left subtree (left child)
        if node.left:
            self.canvas.create_line(x, y, x - dx, y + 60)
            self._draw_tree(node.left, x - dx, y + 60, dx // 2, highlight_node)
        # Draw right subtree (right child)
        if node.right:
            self.canvas.create_line(x, y, x + dx, y + 60)
            self._draw_tree(node.right, x + dx, y + 60, dx // 2, highlight_node)
        # Draw current node (highlighted if it's the search result)
        color = "red" if highlight_node is not None and node is highlight_node else "lightblue"
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color)
        self.canvas.create_text(x, y, text=str(node.key), font=("Arial", 12, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = BSTApp(root)
    root.mainloop() 