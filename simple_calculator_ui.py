import tkinter as tk
from simple_calculator_logic import calculate_expression
from simple_calculator_logic import parse_equation


class SimpleCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Simple Calculator')
        self.geometry('450x550')
        self.minsize(300, 400)

        self.result_var = tk.StringVar()
        self.equation_var = tk.StringVar()
        self.bind('<Return>', self.on_equals)

        self.create_widgets()

    def create_widgets(self):
        # Configure entry box
        display = tk.Entry(self, textvariable=self.result_var,
                           font=('Helvetica', 20), bd=3,
                           justify='right',
                           insertwidth=2)
        display.grid(row=0, column=0, columnspan=4,
                     sticky='nsew', padx=10, pady=(5, 0))

        # Configure label for equation display
        equation_label = tk.Label(self, textvariable=self.equation_var,
                                  font=('Helvetica', 16),
                                  bg=self.cget('bg'),
                                  anchor='e')
        equation_label.grid(row=1, column=0, columnspan=4,
                            sticky='nsew', padx=10, pady=(0, 5))

        # Button layout
        buttons = [
            ('C', '#d3ffc7', 2, 0), ('+/-', '#d3ffc7', 2, 1),
            ('%', '#d3ffc7', 2, 2), ('/', '#f9f9f9', 2, 3),
            ('7', '#ffffff', 3, 0), ('8', '#ffffff', 3, 1),
            ('9', '#ffffff', 3, 2), ('*', '#f9f9f9', 3, 3),
            ('4', '#ffffff', 4, 0), ('5', '#ffffff', 4, 1),
            ('6', '#ffffff', 4, 2), ('-', '#f9f9f9', 4, 3),
            ('1', '#ffffff', 5, 0), ('2', '#ffffff', 5, 1),
            ('3', '#ffffff', 5, 2), ('+', '#f9f9f9', 5, 3),
            ('0', '#ffffff', 6, 0, 2),
            ('.', '#ffffff', 6, 2), ('=', '#f9f9f9', 6, 3)
        ]

        # Configure button
        for button in buttons:
            text, color, row, col = button[:4]
            colspan = button[4] if len(button) > 4 else 1

            if text == 'C':
                cur_button = tk.Button(self, text=text, bg=color,
                                       font=('Arial', 18), command=self.clear)
            elif text == '+/-':
                cur_button = tk.Button(self, text=text, bg=color,
                                       font=('Arial', 18), command=self.sign_inverse)
            elif text == '=':
                cur_button = tk.Button(self, text=text, bg=color,
                                       font=('Arial', 18), command=self.on_equals)
            else:
                cur_button = tk.Button(self, text=text, bg=color,
                                       font=('Arial', 18),
                                       command=lambda t=text: self.button_click(t))

            cur_button.grid(row=row, column=col,
                            columnspan=colspan, sticky='nsew')

        # Configure row and column weights
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.grid_columnconfigure(j, weight=1)
        self.grid_rowconfigure(1, weight=0)

    def sign_inverse(self):
        cur_text = self.result_var.get()
        if cur_text == '':
            # If entry is empty, add a minus sign
            self.result_var.set('-')
        elif cur_text.startswith('-'):
            # If entry starts with a
            # minus sign, remove it
            self.result_var.set(cur_text[:1])
        elif cur_text[len(cur_text) - 1] in '+-*/%':
            self.result_var.set(cur_text + '-')
        else:
            # Inverse current number
            try:
                val = float(cur_text)
                val = round(val * -1, 8)
                if val.is_integer():
                    val = int(val)
                self.result_var.set(str(val))
            except ValueError as e:
                self.show_error(str(e))

        self.after(0, lambda: self.focus_to_end())

    def button_click(self, text):
        cur_text = self.result_var.get()

        if cur_text == '' and text in '+*/%':
            return
        elif cur_text == '-' and text in '+-*/%':
            self.result_var.set('')
            self.equation_var.set('')
        else:
            # Update the equation with new entry
            self.result_var.set(cur_text + text)

        self.after(0, lambda: self.focus_to_end())

    def on_equals(self, event=None):
        user_input = self.result_var.get()
        try:
            expression = parse_equation(user_input)
            result = calculate_expression(expression)
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)
            self.result_var.set(result)
            self.equation_var.set(user_input)
        except ZeroDivisionError as e:
            self.show_error(str(e))
        except ValueError as e:
            self.show_error(str(e))

        self.after(0, lambda: self.focus_to_end())

    def focus_to_end(self):
        display = self.focus_get()
        if isinstance(display, tk.Entry):
            display.icursor(tk.END)

    def show_error(self, msg):
        # Create a new Toplevel window
        msg_window = tk.Toplevel(self)
        msg_window.title('Error')
        msg_window.geometry('400x300')
        msg_window.minsize(350, 250)

        # Create a Label widget to display the error message
        error_label = tk.Label(msg_window, text=msg, padx=20, pady=20)
        error_label.pack()

        # Create an OK button to close the window
        ok_button = tk.Button(msg_window, text='OK', command=msg_window.destroy)
        ok_button.pack(pady=10)

    def clear(self):
        self.result_var.set('')
        self.equation_var.set('')
