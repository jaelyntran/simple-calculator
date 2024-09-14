import tkinter as tk
from simple_calculator_logic import calculate_expression
from simple_calculator_logic import parse_equation


class SimpleCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Simple Calculator')
        self.geometry('450x550')
        self.minsize(300, 400)

        self.equation_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.bind('<Return>', self.on_equals)

        self.create_widgets()

    def create_widgets(self):
        # Configure entry box
        display = tk.Entry(self, textvariable=self.equation_var,
                           font=('Helvetica', 20), bd=4,
                           justify='right',
                           insertwidth=3)
        display.grid(row=0, column=0, columnspan=4,
                     sticky='nsew', padx=10, pady=10)

        # Configure result label
        result_label = tk.Label(self, textvariable=self.result_var,
                                font=('Helvetica', 24), bd=4,
                                justify='right',
                                relief='sunken',
                                anchor='e')
        result_label.grid(row=1, column=0, columnspan=4,
                          sticky='nsew', padx=10, pady=10)

        # Button layout
        buttons = [
            ('C', 2, 0), ('+/-', 2, 1), ('%', 2, 2), ('/', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('*', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
            ('0', 6, 0, 2), ('.', 6, 2), ('=', 6, 3)
        ]

        # Configure button
        for button in buttons:
            text, row, col = button[:3]
            colspan = button[3] if len(button) > 3 else 1

            if text == 'C':
                cur_button = tk.Button(self, text=text,
                                       font=('Arial', 18), command=self.clear)
            elif text == '=':
                cur_button = tk.Button(self, text=text,
                                       font=('Arial', 18), command=self.on_equals)
            elif text == '0':
                cur_button = tk.Button(self, text=text, font=('Arial', 18),
                                       command=lambda t=text: self.button_click(t))
            else:
                cur_button = tk.Button(self, text=text, font=('Arial', 18),
                                       command=lambda t=text: self.button_click(t))

            cur_button.grid(row=row, column=col,
                            columnspan=colspan, sticky='nsew')

        # Configure row and column weights
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.grid_columnconfigure(j, weight=1)

    def button_click(self, text):
        cur_text = self.equation_var.get()
        self.equation_var.set(cur_text + text)

    def on_equals(self, event=None):
        user_input = self.equation_var.get()
        try:
            expression = parse_equation(user_input)
            result = calculate_expression(expression)
            if result.is_integer():
                result = int(result)
            self.result_var.set(f'{user_input}\n= {result}')
        except ZeroDivisionError as e:
            self.show_error(str(e))
        except ValueError as e:
            self.show_error(str(e))

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
        self.equation_var.set('')
        self.result_var.set('')
