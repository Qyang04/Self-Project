import math
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import List, Tuple, Optional

def coin_change_min_coins_dp(coins, amount):
    """
    Dynamic programming solution for minimum coins problem
    Returns minimum number of coins needed and the combination
    """
    if amount == 0:
        return 0, []
    
    if amount < 0:
        return -1, []
    
    print(f"\nDYNAMIC PROGRAMMING SOLUTION FOR MINIMUM COINS:")
    print("=" * 60)
    print(f"Coins: {coins}, Amount: {amount}")
    print()
    
    # Initialize DP table for minimum coins
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # Track which coin was used for each amount
    coin_used = [-1] * (amount + 1)
    
    print("STEP-BY-STEP DP FILLING:")
    print("-" * 40)
    
    # Fill DP table
    for current_amount in range(1, amount + 1):
        print(f"\nProcessing amount {current_amount}:")
        print(f"  Initial dp[{current_amount}] = ∞")
        
        for coin in coins:
            if coin <= current_amount:
                print(f"  → Try coin {coin}: dp[{current_amount - coin}] + 1 = {dp[current_amount - coin]} + 1 = {dp[current_amount - coin] + 1}")
                if dp[current_amount - coin] + 1 < dp[current_amount]:
                    dp[current_amount] = dp[current_amount - coin] + 1
                    coin_used[current_amount] = coin
                    print(f"  → Update dp[{current_amount}] = {dp[current_amount]} (using coin {coin})")
                else:
                    print(f"  → Keep current value {dp[current_amount]} (better than {dp[current_amount - coin] + 1})")
            else:
                print(f"  → Skip coin {coin} (too large for amount {current_amount})")
        
        if dp[current_amount] == float('inf'):
            print(f"  Final: dp[{current_amount}] = ∞ (no solution)")
        else:
            print(f"  Final: dp[{current_amount}] = {dp[current_amount]} coins")
    
    # Check if solution exists
    if dp[amount] == float('inf'):
        print(f"\nRESULT: Impossible to make amount {amount}")
        return -1, []
    
    # Reconstruct the solution
    print(f"\nRECONSTRUCTING OPTIMAL SOLUTION:")
    print("-" * 40)
    combination = []
    remaining = amount
    step = 1
    
    while remaining > 0:
        coin = coin_used[remaining]
        combination.append(coin)
        print(f"Step {step}: Use coin {coin}, remaining = {remaining} - {coin} = {remaining - coin}")
        remaining -= coin
        step += 1
    
    print(f"Final combination: {combination}")
    print(f"Total coins: {dp[amount]}")
    
    return dp[amount], combination, dp

def coin_change_count_ways_dp(coins, amount):
    """
    Dynamic programming solution for counting all ways
    Returns the total number of different ways to make the amount
    """
    if amount == 0:
        return 1
    
    if amount < 0:
        return 0
    
    print(f"\nDYNAMIC PROGRAMMING SOLUTION FOR COUNTING WAYS:")
    print("=" * 60)
    print(f"Coins: {coins}, Amount: {amount}")
    print()
    
    # Initialize DP table for counting ways
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make amount 0 (use no coins)
    
    print("STEP-BY-STEP DP FILLING:")
    print("-" * 40)
    print(f"Initialize: dp[0] = 1 (base case)")
    
    # Fill DP table - this counts all possible sequences
    for coin in coins:
        print(f"\nProcessing coin {coin}:")
        for current_amount in range(coin, amount + 1):
            old_value = dp[current_amount]
            dp[current_amount] += dp[current_amount - coin]
            print(f"  → dp[{current_amount}] += dp[{current_amount - coin}] = {old_value} + {dp[current_amount - coin]} = {dp[current_amount]}")
    
    print(f"\nRESULT: Total ways to make {amount}: {dp[amount]}")
    
    return dp[amount], dp

class PrettyTable:
    """A class to create pretty formatted tables in tkinter"""
    
    def __init__(self, parent, headers, data, title="", max_rows=20):
        self.parent = parent
        self.headers = headers
        self.data = data
        self.title = title
        self.max_rows = max_rows
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        
        # Title
        if title:
            title_label = ttk.Label(self.frame, text=title, font=('Arial', 12, 'bold'))
            title_label.pack(pady=(0, 10))
        
        # Create Treeview
        self.tree = ttk.Treeview(self.frame, columns=headers, show='headings', height=min(len(data), max_rows))
        
        # Configure columns
        for header in headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, width=150, anchor='center')
        
        # Add data
        for i, row in enumerate(data):
            tags = ()
            if i == 0:  # Header row
                tags = ('header',)
            elif i % 2 == 0:  # Even rows
                tags = ('even',)
            else:  # Odd rows
                tags = ('odd',)
            
            self.tree.insert('', 'end', values=row, tags=tags)
        
        # Configure tags for styling
        self.tree.tag_configure('header', background='#4CAF50', foreground='white', font=('Arial', 10, 'bold'))
        self.tree.tag_configure('even', background='#f9f9f9')
        self.tree.tag_configure('odd', background='#ffffff')
        
        # Add scrollbar if needed
        if len(data) > max_rows:
            scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side='right', fill='y')
        
        self.tree.pack(fill='both', expand=True)
    
    def pack(self, **kwargs):
        return self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        return self.frame.grid(**kwargs)

class CoinChangeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Coin Change Problem - Dynamic Programming")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title with better styling
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="🪙 Coin Change Problem", 
                               font=('Arial', 18, 'bold'), foreground='#2E86AB')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Dynamic Programming Solution", 
                                  font=('Arial', 12), foreground='#666666')
        subtitle_label.pack()
        
        # Input section with better styling
        input_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding="15")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Coins input
        ttk.Label(input_frame, text="Coins (space-separated):", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.coins_entry = ttk.Entry(input_frame, width=35, font=('Arial', 10))
        self.coins_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        self.coins_entry.insert(0, "1 3 4 5")
        
        # Amount input
        ttk.Label(input_frame, text="Target Amount:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(15, 0))
        self.amount_entry = ttk.Entry(input_frame, width=35, font=('Arial', 10))
        self.amount_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 20), pady=(15, 0))
        self.amount_entry.insert(0, "7")
        
        # Solve button with better styling
        solve_button = ttk.Button(input_frame, text="Solve Problem", command=self.solve_problem, 
                                 style='Accent.TButton')
        solve_button.grid(row=0, column=2, rowspan=2, padx=(20, 0))
        
        # Results section with better styling
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="15")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Results labels with better styling
        self.total_ways_label = ttk.Label(results_frame, text="Total ways: -", font=('Arial', 11, 'bold'), foreground='#2E86AB')
        self.total_ways_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 30))
        
        self.min_coins_label = ttk.Label(results_frame, text="Minimum coins: -", font=('Arial', 11, 'bold'), foreground='#A23B72')
        self.min_coins_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        self.combination_label = ttk.Label(results_frame, text="Optimal combination: -", font=('Arial', 11, 'bold'), foreground='#F18F01')
        self.combination_label.grid(row=0, column=2, sticky=tk.W)
        
        # DP Tables section
        tables_frame = ttk.LabelFrame(main_frame, text="Dynamic Programming Tables", padding="15")
        tables_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        tables_frame.columnconfigure(0, weight=1)
        tables_frame.columnconfigure(1, weight=1)
        tables_frame.rowconfigure(0, weight=1)
        
        # Notebook for tabs with better styling
        notebook = ttk.Notebook(tables_frame)
        notebook.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Minimum coins tab
        min_coins_frame = ttk.Frame(notebook)
        notebook.add(min_coins_frame, text="Minimum Coins")
        
        self.min_coins_container = ttk.Frame(min_coins_frame)
        self.min_coins_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Count ways tab
        count_ways_frame = ttk.Frame(notebook)
        notebook.add(count_ways_frame, text="Count Ways")
        
        self.count_ways_container = ttk.Frame(count_ways_frame)
        self.count_ways_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Steps tab
        steps_frame = ttk.Frame(notebook)
        notebook.add(steps_frame, text="Step-by-Step Process")
        
        self.steps_text = scrolledtext.ScrolledText(steps_frame, height=20, width=100, 
                                                   font=('Consolas', 10), wrap=tk.WORD)
        self.steps_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar with better styling
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to solve!")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, 
                              font=('Arial', 9), foreground='#666666')
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 0))

    def solve_problem(self):
        """Solve the coin change problem and display results"""
        try:
            # Get input values
            coins_input = self.coins_entry.get().strip()
            amount_input = self.amount_entry.get().strip()
            
            if not coins_input or not amount_input:
                messagebox.showerror("Error", "Please enter both coins and target amount")
                return
            
            # Parse coins
            coins = []
            for coin_str in coins_input.split():
                coin = int(coin_str)
                if coin <= 0:
                    messagebox.showerror("Error", f"Invalid coin value: {coin}. Coins must be positive integers!")
                    return
                coins.append(coin)
            
            if not coins:
                messagebox.showerror("Error", "No valid coins entered!")
                return
            
            # Parse amount
            amount = int(amount_input)
            if amount < 0:
                messagebox.showerror("Error", "Target amount cannot be negative!")
                return
            
            self.status_var.set("Solving...")
            self.root.update()
        
        # Solve using dynamic programming
            min_coins, min_combination, min_dp = coin_change_min_coins_dp(coins, amount)
            total_ways, ways_dp = coin_change_count_ways_dp(coins, amount)
            
            # Update results with emojis
            self.total_ways_label.config(text=f"Total ways: {total_ways}")
            
            if min_coins != -1:
                self.min_coins_label.config(text=f"Minimum coins: {min_coins}")
                self.combination_label.config(text=f"Optimal combination: {min_combination}")
            else:
                self.min_coins_label.config(text="Minimum coins: Impossible")
                self.combination_label.config(text="Optimal combination: None")
            
            # Display pretty DP tables
            self.display_pretty_min_coins_table(coins, amount, min_dp)
            self.display_pretty_count_ways_table(coins, amount, ways_dp)
            self.display_steps(coins, amount, min_coins, min_combination, total_ways, min_dp, ways_dp)
            
            self.status_var.set("Solved successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            self.status_var.set("Error occurred")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error occurred")

    def display_pretty_min_coins_table(self, coins, amount, dp_table):
        """Display minimum coins DP table in a pretty format"""
        # Clear previous table
        for widget in self.min_coins_container.winfo_children():
            widget.destroy()
        
        # Prepare data for table
        headers = ["Amount", "DP Value", "Explanation"]
        data = []
        
        for i in range(amount + 1):
            result = dp_table[i]
            if result == float('inf'):
                result_str = '∞'
                explanation = "No solution possible"
            else:
                result_str = str(result)
                if i == 0:
                    explanation = "Base case: 0 coins needed for amount 0"
                else:
                    if result == 0:
                        explanation = "Base case: 0 coins needed for amount 0"
                    else:
                        # Find the coin that gives minimum
                        min_coin = None
                        for coin in coins:
                            if coin <= i and dp_table[i - coin] + 1 == result:
                                min_coin = coin
                                break
                        explanation = f"Use coin {min_coin}: dp[{i - min_coin}] + 1 = {dp_table[i - min_coin]} + 1 = {result}"
            
            data.append([f"Amount {i}", result_str, explanation])
        
        # Create pretty table
        table = PrettyTable(self.min_coins_container, headers, data, 
                           title="Minimum Coins Dynamic Programming Table")
        table.pack(fill=tk.BOTH, expand=True)

    def display_pretty_count_ways_table(self, coins, amount, dp_table):
        """Display count ways DP table in a pretty format"""
        # Clear previous table
        for widget in self.count_ways_container.winfo_children():
            widget.destroy()
        
        # Prepare data for table
        headers = ["Amount", "DP Value", "Explanation"]
        data = []
        
        for i in range(amount + 1):
            result = dp_table[i]
            result_str = str(result)
            
            if i == 0:
                explanation = "Base case: 1 way to make amount 0"
            else:
                if result == 0:
                    explanation = "No ways to make this amount"
                else:
                    ways = []
                    for coin in coins:
                        if coin <= i and dp_table[i - coin] > 0:
                            ways.append(f"dp[{i - coin}]={dp_table[i - coin]}")
                    if ways:
                        explanation = f"Sum of ways: {' + '.join(ways)} = {result}"
                    else:
                        explanation = f"Base case: {result} way(s)"
            
            data.append([f"Amount {i}", result_str, explanation])
        
        # Create pretty table
        table = PrettyTable(self.count_ways_container, headers, data, 
                           title="Count Ways Dynamic Programming Table")
        table.pack(fill=tk.BOTH, expand=True)

    def display_steps(self, coins, amount, min_coins, min_combination, total_ways, min_dp, ways_dp):
        """Display step-by-step process with better formatting"""
        self.steps_text.delete(1.0, tk.END)
        
        output = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    STEP-BY-STEP DYNAMIC PROGRAMMING PROCESS                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

INPUT PARAMETERS:
   • Coins available: {coins}
   • Target amount: {amount}

RESULTS:
   • Total ways to obtain {amount}: {total_ways}
"""
        
        if min_coins != -1:
            output += f"   • Optimal way (minimum coins): {min_coins} coins\n"
            output += f"   • Optimal combination: {min_combination}\n"
        else:
            output += f"   • Optimal way: Impossible to make the amount\n"
        
        output += f"""
ALGORITHM EXPLANATION:

MINIMUM COINS ALGORITHM:
   • For each amount from 1 to target, try each coin
   • If coin value <= current amount, check if using this coin gives fewer total coins
   • Formula: dp[amount] = min(dp[amount - coin] + 1) for all valid coins
   • Time Complexity: O(amount × number of coins)
   • Space Complexity: O(amount)

COUNT WAYS ALGORITHM:
   • For each coin, update all amounts that can be reached using this coin
   • Formula: dp[amount] += dp[amount - coin] for each coin
   • This counts all possible sequences of coins that sum to the target
   • Time Complexity: O(amount × number of coins)
   • Space Complexity: O(amount)

KEY INSIGHTS:
   • Dynamic programming avoids recalculating subproblems
   • Each cell in the DP table represents the solution to a subproblem
   • The final answer is found in dp[target_amount]
"""
        
        self.steps_text.insert(tk.END, output)

def run_coin_change_program():
    """Main function to run the coin change program"""
    # Create GUI
    root = tk.Tk()
    app = CoinChangeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_coin_change_program()