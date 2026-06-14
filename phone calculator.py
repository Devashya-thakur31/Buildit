import tkinter as tk
import ast
import operator

class PhoneCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("360x520")
        self.root.configure(bg="#17171c") # Modern dark background
        self.root.resizable(False, False)

        self.expression = ""

        # Safe AST operators map
        self.allowed_operators = {
            ast.Add: operator.add, ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv,
            ast.Mod: operator.mod, ast.Pow: operator.pow,
            ast.USub: operator.neg, ast.UAdd: operator.pos
        }

        # 1. Digital Display Screen
        self.display_label = tk.Label(
            root, text="0", anchor="e", font=("Arial", 36),
            bg="#17171c", fg="#ffffff", padx=20, pady=20
        )
        self.display_label.pack(expand=True, fill="both")

        # 2. Square Button Grid Layout Configuration
        self.button_frame = tk.Frame(root, bg="#17171c")
        self.button_frame.pack(fill="both", expand=True)

        # Configure 4 columns equally
        for i in range(4):
            self.button_frame.columnconfigure(i, weight=1)
        # Configure 5 rows equally  
        for i in range(5):
            self.button_frame.rowconfigure(i, weight=1)

        self.create_buttons()

    def create_buttons(self):
        # Grid layout blueprint matrix: (Text, Row, Column, BG Color, Text Color)
        buttons = [
            ('C', 0, 0, '#a5a5a5', '#000000'), ('(', 0, 1, '#a5a5a5', '#000000'), (')', 0, 2, '#a5a5a5', '#000000'), ('/', 0, 3, '#ff9f0a', '#ffffff'),
            ('7', 1, 0, '#333333', '#ffffff'), ('8', 1, 1, '#333333', '#ffffff'), ('9', 1, 2, '#333333', '#ffffff'), ('*', 1, 3, '#ff9f0a', '#ffffff'),
            ('4', 2, 0, '#333333', '#ffffff'), ('5', 2, 1, '#333333', '#ffffff'), ('6', 2, 2, '#333333', '#ffffff'), ('-', 2, 3, '#ff9f0a', '#ffffff'),
            ('1', 3, 0, '#333333', '#ffffff'), ('2', 3, 1, '#333333', '#ffffff'), ('3', 3, 2, '#333333', '#ffffff'), ('+', 3, 3, '#ff9f0a', '#ffffff'),
            ('0', 4, 0, '#333333', '#ffffff'), ('.', 4, 1, '#333333', '#ffffff'), ('%', 4, 2, '#333333', '#ffffff'), ('=', 4, 3, '#ff9f0a', '#ffffff'),
        ]

        for text, row, col, bg, fg in buttons:
            # Lambda keeps click tracking tied directly to the unique character
            btn = tk.Button(
                self.button_frame, text=text, bg=bg, fg=fg, 
                font=("Arial", 20, "bold"), borderwidth=0, relief="flat",
                command=lambda t=text: self.on_button_click(t)
            )
            # Sticky "nsew" stretches the button to form perfectly square cells
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display_label.config(text="0")
        elif char == '=':
            self.calculate_result()
        else:
            # Append characters smoothly to build the arithmetic string
            if self.display_label.cget("text") == "0" and char not in ['+', '-', '*', '/', '%']:
                self.expression = char
            else:
                self.expression += char
            self.display_label.config(text=self.expression)

    def calculate_result(self):
        if not self.expression:
            return
        try:
            node = ast.parse(self.expression.strip(), mode='eval')
            result = self._eval_node(node.body)
            
            # Format float answers nicely to remove ugly trailing zeros
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            self.display_label.config(text=str(result))
            self.expression = str(result) # Store string result to continue calculating
        except ZeroDivisionError:
            self.display_label.config(text="Error")
            self.expression = ""
        except Exception:
            self.display_label.config(text="Error")
            self.expression = ""

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left_val = self._eval_node(node.left)
            right_val = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in self.allowed_operators:
                return self.allowed_operators[op_type](left_val, right_val)
        elif isinstance(node, ast.UnaryOp):
            operand_val = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in self.allowed_operators:
                return self.allowed_operators[op_type](operand_val)
        raise ValueError("Invalid operation")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneCalculator(root)
    root.mainloop()
