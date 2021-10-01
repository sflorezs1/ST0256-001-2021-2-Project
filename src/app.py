import ast
import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable, Optional
import math  # will be used for user defined lambdas at runtime


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title('Métodos Numéricos')

        self.geometry('800x600')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage,):
            frame: tk.Frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        self.frames[cont].tkraise()

    @staticmethod
    def parse_lambda(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            body = value_if_allowed.replace('^', '**')
            f = ast.Lambda('x', body)
            return f
        else:
            return None

    @staticmethod
    def validate_num(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False


class StartPage(tk.Frame):
    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Menu principal")
        label.pack()

        button_is = ttk.Button(self, text="Búsquedas incrementales",
                               command=lambda _: controller.show_frame(IncrementalSearches))
        button_is.pack()
        button_b = ttk.Button(self, text="Bisección",
                              command=lambda _: controller.show_frame(Bisection))
        button_b.pack()
        button_fr = ttk.Button(self, text="Regla falsa",
                               command=lambda _: controller.show_frame(FakeRule))
        button_fr.pack()
        button_fp = ttk.Button(self, text="Punto Fijo",
                               command=lambda _: controller.show_frame(FixedPoint))
        button_fp.pack()
        button_n = ttk.Button(self, text="Newton",
                              command=lambda _: controller.show_frame(Newton))
        button_n.pack()
        button_s = ttk.Button(self, text="Secante",
                               command=lambda _: controller.show_frame(Secant))
        button_s.pack()
        button_mr = ttk.Button(self, text="Raíces múltiples",
                               command=lambda _: controller.show_frame(FakeRule))
        button_mr.pack()


class IncrementalSearches(tk.Frame):
    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)

        label = ttk.Label(text="Método de búsquedas incrementales")
        label.grid(row=0, column=4, padx=10, pady=10)
        func_entry = ttk.Entry(self, validate='key', validatecomand=controller.validate_num)
        f: Optional[Callable] = None

        ttk.Entry(self, validate='key', validatecomand=controller.validate_num)



class Bisection(tk.Frame):
    pass


class FakeRule(tk.Frame):
    pass


class FixedPoint(tk.Frame):
    pass


class Newton(tk.Frame):
    pass


class Secant(tk.Frame):
    pass


class MultipleRoots(tk.Frame):
    pass
