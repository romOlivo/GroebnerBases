from application.window import Window
from model.parse import Parse
from model.groebner import Groebner
from tkinter import font


class Application:
    def __init__(self):
        self.principal_window = None
        self.find_window = None
        self.test_window = None
        self.create_principal_window()

    def create_principal_window(self):
        def open_find_window():
            self.create_find_window()
            self.principal_window.open_window(self.find_window)

        def open_test_window():
            self.create_test_window()
            self.principal_window.open_window(self.test_window)

        self.principal_window = Window(title="Groebner Bases")
        self.principal_window.add_label(text="Bienvenido a Groebner Bases", font=font.BOLD, column=0, row=0,
                                        columnspan=2)
        self.principal_window.add_label(text="Calcula y comprueba Bases de Groebner de un ideal polinomial",
                                        side=None, px=4, py=20, column=0, row=1, columnspan=2)
        self.principal_window.add_button(text="Comprobar", command=open_test_window, column=0, row=2)
        self.principal_window.add_button(text="Encontrar", command=open_find_window, column=1, row=2)

    def create_find_window(self):
        def open_principal_window():
            self.create_principal_window()
            self.find_window.open_window(self.principal_window)

        def act_var():
            inp = self.find_window.get_input(id_input)
            current = self.find_window.get_text_component(id_label)
            new_text = "{0}\n{1}".format(current, inp)
            if current == "":
                new_text = inp
            self.find_window.change_label_properties(id_label, text=new_text)
            self.find_window.delete_text(id=id_input)

        def clean():
            self.find_window.change_label_properties(id_label, text="")
            self.find_window.change_label_properties(id_solution, text="")

        def find():
            base_text = self.find_window.get_text_component(id_label)
            variables = Parse.get_ordered_var(f="", base=base_text, sep="\n")
            generators = Parse.convert_poly_base(base=base_text, var=variables, sep="\n")
            self.find_window.change_label_properties(id_title, text="Base de Groebner")
            base = Groebner.make_groebner_base(base=generators)
            text = Parse.base_to_string(base=base, var=variables, sep="\n")
            self.find_window.change_label_properties(id_solution, text=text)

        self.find_window = Window(title="Groebner Bases", width=500, height=400)
        self.find_window.add_label(text="Buscador de Bases de Groebner", font=font.BOLD, column=0, row=0,
                                        columnspan=3, py=5)
        self.find_window.add_label(text="Introduzca un nuevo generador", column=0, row=1, px=4, py=2)
        id_input = self.find_window.add_input(width=30, column=1, row=1)
        self.find_window.add_button(text="Añadir", command=act_var, column=2, row=1, px=15)
        self.find_window.add_label(text="Orden", column=0, row=2, py=7)
        self.find_window.add_label(text="Lexicográfico", column=1, row=2, py=7)
        self.find_window.add_label(text="Generadores", column=0, row=3, columnspan=3, font=font.ITALIC, py=10)
        id_label = self.find_window.add_label(column=0, row=4, columnspan=3)
        self.find_window.add_button(text="Comprobar", command=find, column=0, row=6)
        self.find_window.add_button(text="Limpiar", command=clean, column=2, row=6, px=20)
        id_title = self.find_window.add_label(column=0, row=7, px=4, py=2, columnspan=3, font=font.BOLD)
        id_solution = self.find_window.add_label(column=0, row=8, px=4, py=10, columnspan=3)
        self.find_window.add_linear_separator(column=0, row=9, columnspan=3, px=10, py=10)
        self.find_window.add_button(text="Volver", command=open_principal_window, column=0, row=10)
        self.find_window.add_button(text="Cerrar", command=self.find_window.close, column=2, row=10, px=20)

    def create_test_window(self):
        def open_principal_window():
            self.create_principal_window()
            self.test_window.open_window(self.principal_window)

        def act_var():
            inp = self.test_window.get_input(id_input)
            current = self.test_window.get_text_component(id_label)
            new_text = "{0}\n{1}".format(current, inp)
            if current == "":
                new_text = inp
            self.test_window.change_label_properties(id_label, text=new_text)

        def clean():
            self.test_window.change_label_properties(id_label, text="")
            self.test_window.change_label_properties(id_title, text="")
            self.test_window.change_label_properties(id_solution, text="")

        def test():
            f_text = self.test_window.get_input(id_input_pol)
            base_text = self.test_window.get_text_component(id_label)
            variables = Parse.get_ordered_var(f=f_text, base=base_text, sep="\n")
            f = Parse.convert_poly(p=f_text, var=variables)
            generators = Parse.convert_poly_base(base=base_text, var=variables, sep="\n")
            is_member = Groebner.pol_in_ideal(f=f, base=generators)
            add_text = ""
            if not is_member:
                add_text = "no "
            self.test_window.change_label_properties(id_title, text="Resultado")
            self.test_window.change_label_properties(id_solution, text="El polinomio {0} {1}pertenece al ideal"
                                                     .format(f_text, add_text))

        self.test_window = Window(title="Groebner Bases", width=550, height=350)
        self.test_window.add_label(text="Comprobador Pertenecia Ideal", font=font.BOLD, column=0, row=0,
                                        columnspan=3, py=15)
        self.test_window.add_label(text="Introduzca un polinomio", column=0, row=1, px=4, py=2)
        id_input_pol = self.test_window.add_input(width=30, column=1, row=1)
        self.test_window.add_label(text="Introduzca elemento Base de Groebner", column=0, row=2, px=4, py=2)
        id_input = self.test_window.add_input(width=30, column=1, row=2)
        self.test_window.add_button(text="Añadir", command=act_var, column=2, row=2, px=15)
        self.test_window.add_label(text="Generadores", column=0, row=3, px=4, py=15, columnspan=3)
        id_label = self.test_window.add_label(column=0, row=4, columnspan=3, py=5)
        self.test_window.add_button(text="Comprobar", command=test, column=0, row=6)
        self.test_window.add_button(text="Limpiar", command=clean, column=2, row=6, px=20)
        id_title = self.test_window.add_label(column=0, row=7, px=4, py=2, columnspan=3, font=font.BOLD)
        id_solution = self.test_window.add_label(column=0, row=8, px=4, py=10, columnspan=3)
        self.test_window.add_linear_separator(column=0, row=9, columnspan=3, px=10, py=10)
        self.test_window.add_button(text="Volver", command=open_principal_window, column=0, row=10)
        self.test_window.add_button(text="Cerrar", command=self.test_window.close, column=2, row=10, px=20)

    def run(self):
        # Show principal window
        self.principal_window.show()


def main():
    Application().run()


if __name__ == '__main__':
    main()