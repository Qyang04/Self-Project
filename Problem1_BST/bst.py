class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key  # Use 'key' for clarity and consistency

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, verbose=True):
        """Insert a key into the BST, showing steps if verbose."""
        if verbose:
            print(f"Inserting {key}:")
        self.root = self._insert(self.root, key, verbose)

    def _insert(self, node, key, verbose, depth=0):
        indent = '  ' * depth
        if node is None:
            if verbose:
                print(f"{indent}Node is None, inserting {key} here.")
            return Node(key)
        if verbose:
            print(f"{indent}At node {node.key}.")
        if key < node.key:
            if verbose:
                print(f"{indent}{key} < {node.key}: go left.")
            node.left = self._insert(node.left, key, verbose, depth+1)
        elif key > node.key:
            if verbose:
                print(f"{indent}{key} > {node.key}: go right.")
            node.right = self._insert(node.right, key, verbose, depth+1)
        else:
            if verbose:
                print(f"{indent}{key} == {node.key}: already exists, not inserting.")
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

    def search(self, key, verbose=True):
        """Search for a key in the BST. Returns True if found, else False. Shows steps if verbose."""
        if verbose:
            print(f"Searching for {key}:")
        return self._search(self.root, key, verbose)

    def _search(self, node, key, verbose, depth=0):
        indent = '  ' * depth
        if node is None:
            if verbose:
                print(f"{indent}Node is None. {key} not found.")
            return False
        if verbose:
            print(f"{indent}At node {node.key}.")
        if key == node.key:
            if verbose:
                print(f"{indent}Found {key}!")
            return True
        elif key < node.key:
            if verbose:
                print(f"{indent}{key} < {node.key}: go left.")
            return self._search(node.left, key, verbose, depth+1)
        else:
            if verbose:
                print(f"{indent}{key} > {node.key}: go right.")
            return self._search(node.right, key, verbose, depth+1)

    def delete(self, key, verbose=True):
        """Delete a key from the BST, showing steps if verbose."""
        if verbose:
            print(f"Deleting {key}:")
        self.root, deleted = self._delete(self.root, key, verbose)
        if verbose:
            if deleted:
                print(f"{key} deleted from BST.")
            else:
                print(f"{key} not found in BST.")

    def _delete(self, node, key, verbose, depth=0):
        indent = '  ' * depth
        if node is None:
            if verbose:
                print(f"{indent}Node is None. {key} not found.")
            return node, False
        if verbose:
            print(f"{indent}At node {node.key}.")
        if key < node.key:
            if verbose:
                print(f"{indent}{key} < {node.key}: go left.")
            node.left, deleted = self._delete(node.left, key, verbose, depth+1)
            return node, deleted
        elif key > node.key:
            if verbose:
                print(f"{indent}{key} > {node.key}: go right.")
            node.right, deleted = self._delete(node.right, key, verbose, depth+1)
            return node, deleted
        else:
            if verbose:
                print(f"{indent}Found {key}, deleting...")
            # Node with only one child or no child
            if node.left is None:
                if verbose:
                    print(f"{indent}Node has no left child. Replace with right child.")
                return node.right, True
            elif node.right is None:
                if verbose:
                    print(f"{indent}Node has no right child. Replace with left child.")
                return node.left, True
            # Node with two children: Get the inorder successor
            succ = self._min_value_node(node.right)
            if verbose:
                print(f"{indent}Node has two children. Inorder successor is {succ.key}.")
            node.key = succ.key
            node.right, _ = self._delete(node.right, succ.key, verbose, depth+1)
            return node, True

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

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
    while True:
        print("\nCurrent inorder traversal:", ' '.join(map(str, bst.inorder())))
        print("Choose operation: [i]nsert, [s]earch, [d]elete, [q]uit")
        op = input("Operation: ").strip().lower()
        if op == 'i':
            val = input("Enter number to insert: ").strip()
            try:
                val = int(val)
                bst.insert(val)
            except ValueError:
                print("Invalid input.")
        elif op == 's':
            val = input("Enter number to search: ").strip()
            try:
                val = int(val)
                found = bst.search(val)
                print(f"Result: {val} {'found' if found else 'not found'} in BST.")
            except ValueError:
                print("Invalid input.")
        elif op == 'd':
            val = input("Enter number to delete: ").strip()
            try:
                val = int(val)
                bst.delete(val)
            except ValueError:
                print("Invalid input.")
        elif op == 'q':
            print("Exiting.")
            break
        else:
            print("Unknown operation. Please choose i, s, d, or q.")