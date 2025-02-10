import tkinter as tk
from tkinter import ttk
import math
import re

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("400x500")
        
        self.create_widgets()
        self.setup_layout()
        
        self.root.bind('<Return>', lambda event: self.calculate())
        self.root.bind('<BackSpace>', lambda event: self.delete_last())
        self.root.bind('<Escape>', lambda event: self.clear_all())

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=5)
        
        self.entry = ttk.Entry(self.root, font=('Arial', 20), justify='right')
        self.entry.grid(row=0, column=0, columnspan=5, sticky='nsew', padx=5, pady=5)
        
        buttons = [
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('^', 1, 3), ('!', 1, 4),
            ('(', 2, 0), (')', 2, 1), ('%', 2, 2), ('/', 2, 3), ('C', 2, 4),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('+', 3, 3), ('←', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3), ('AC', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('*', 5, 3), ('=', 5, 4),
            ('0', 6, 0), ('.', 6, 1), ('π', 6, 2), ('√', 6, 3), ('°', 6, 4)
        ]
        
        self.buttons = {}
        for (text, row, col) in buttons:
            cmd = lambda x=text: self.button_click(x)
            btn = ttk.Button(self.root, text=text, command=cmd)
            btn.grid(row=row, column=col, sticky='nsew')
            self.buttons[text] = btn

    def setup_layout(self):
        for i in range(7):
            self.root.rowconfigure(i, weight=1)
        for i in range(5):
            self.root.columnconfigure(i, weight=1)

    def button_click(self, char):
        current = self.entry.get()
        
        if char == '=':
            self.calculate()
        elif char == 'C':
            self.clear_entry()
        elif char == 'AC':
            self.clear_all()
        elif char == '←':
            self.delete_last()
        elif char == 'π':
            self.entry.insert(tk.END, 'π')
        elif char == '√':
            self.entry.insert(tk.END, '√(')
        elif char == '°':
            self.entry.insert(tk.END, '°')
        else:
            self.entry.insert(tk.END, char)

    def calculate(self):
        try:
            expression = self.entry.get().strip()
            
            if not expression:
                raise ValueError("Пустое выражение")
            
            expression = self.process_trig_functions(expression)
            
            expression = expression.replace('^', '**').replace('%', '/100')
            expression = expression.replace('π', 'math.pi')
            expression = expression.replace('√', 'math.sqrt')
            expression = expression.replace('°', '')
            
            if re.search(r'/(0[^.]|0$)', expression):
                raise ZeroDivisionError("Деление на ноль запрещено")
            
            expression = self.process_factorial(expression)
            
            result = eval(expression, {'math': math, '__builtins__': None})
            if isinstance(result, float):
                result = round(result, 10)
                result = f"{result:.10f}".rstrip('0').rstrip('.')
            self.clear_all()
            self.entry.insert(0, str(result))
            
        except Exception as e:
            self.clear_all()
            self.entry.insert(0, f"Ошибка: {str(e)}")

    def process_trig_functions(self, expr):
        patterns = [
            (r'(?i)(?<!math\.)(sin|cos|tan)\s*(\d*\.?\d+)(°?)', 
             lambda m: f'math.{m.group(1).lower()}(math.radians({m.group(2)}))' if m.group(3) 
                       else f'math.{m.group(1).lower()}({m.group(2)})'),
            
            (r'(?i)(?<!math\.)(sin|cos|tan)\s*\(\s*(\d*\.?\d+)(°?)\s*\)', 
             lambda m: f'math.{m.group(1).lower()}(math.radians({m.group(2)}))' if m.group(3) 
                       else f'math.{m.group(1).lower()}({m.group(2)})')
        ]
        
        for pattern, replacement in patterns:
            expr = re.sub(pattern, replacement, expr, flags=re.IGNORECASE)
        
        return expr



    def process_factorial(self, expr):
        matches = re.finditer(r'(\d+\.?\d*)!', expr)
        for match in matches:
            num = match.group(1)
            if '.' in num:
                raise ValueError(f"Факториал не определен для дробных чисел: {num}")
            if int(num) < 0:
                raise ValueError(f"Факториал не определен для отрицательных чисел: {num}")
            expr = expr.replace(match.group(0), str(math.factorial(int(num))))
        return expr

    def clear_entry(self):
        self.entry.delete(0, tk.END)

    def clear_all(self):
        self.entry.delete(0, tk.END)

    def delete_last(self):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current[:-1])

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
