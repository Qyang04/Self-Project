class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key  # Use 'key' for clarity and consistency

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Insert a key into the BST."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        """Helper method to insert recursively and return the new subtree root."""
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        # If key == node.key, do not insert duplicates (can be changed if duplicates allowed)
        return node

    def inorder(self):
        """Return the inorder traversal as a list."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def search(self, key):
        """Search for a key in the BST. Returns True if found, else False."""
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

# User input and demo
if __name__ == "__main__":
    bst = BST()
    try:
        nums = list(map(int, input("Enter numbers to insert into BST (space-separated): ").split()))
    except ValueError:
        print("Invalid input. Please enter integers only.")
        exit(1)
    for num in nums:
        bst.insert(num)
    inorder_result = bst.inorder()
    print("Inorder traversal:", ' '.join(map(str, inorder_result)))
    # Optional: Demonstrate search
    search_key = input("Enter a number to search in BST (or press Enter to skip): ").strip()
    if search_key:
        try:
            search_key = int(search_key)
            found = bst.search(search_key)
            print(f"{search_key} {'found' if found else 'not found'} in BST.")
        except ValueError:
            print("Invalid input for search key.")