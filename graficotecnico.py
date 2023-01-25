import tkinter
from tkinter import Label, ttk, Button, Entry, PhotoImage, messagebox

from sistema.centraliza_janelas import center
from tecnico import Tecnico
from sistema.banco import Banco

# class Validadores:
#    def validadores_entry2(self, text):
#        if text == "": return True
#        try:
#            value = int(text)
#        except ValueError:
#            return False
#        return 0 >= 100
#    def ValidarEntradas(self):
#     self.vcmd2 = (self.reserva(self.validadores_entry2), "%P")

class GraficoTecnico :
    def __init__(self, cpf=False):
        self.principal = tkinter.Toplevel()
        self.cpf = cpf

        self.principal.geometry("400x140")
        self.principal.title('Técnicos')
        self.principal.resizable(height=False, width=False)
        center(self.principal)

        ## Labels
        self.lb_nome = Label(self.principal, text="Nome: ")
        self.lb_cpf = Label(self.principal, text="CPF: ")
        self.lb_tel = Label(self.principal, text="Telefone: ")
        self.lb_equipe = Label(self.principal, text="Equipe: ")
        self.lb_turno = Label(self.principal, text="Turno: ")

        ## Icones
        self.icon_salvar = PhotoImage(file="assets/icones/icon_salvar.png")
        self.icon_fechar = PhotoImage(file="assets/icones/icon_saida.png")

        ## Caixas de Texto
        self.cx_nome = Entry(self.principal, width=54)
        self.cx_cpf = Entry(self.principal, width=22)

        self.cx_cpf.bind("<KeyRelease>", self.format_cpf)

        self.cx_tel = Entry(self.principal, width=20)

        self.cx_tel.bind("<KeyRelease>", self.format_telefone)

        self.cx_equipe = Entry(self.principal, width=22)
        self.cx_turno = ttk.Combobox(self.principal, width=17)
        self.cx_turno['values'] = ("Manhã", "Tarde", "Noite")

        ## Botoes
        self.bt_salvar = Button(self.principal, text="Salvar", image=self.icon_salvar, compound='left', padx=5,
                                height=22, command=self.salvar)
        self.bt_fechar = Button(self.principal, text="Fechar", image=self.icon_fechar, compound='left', padx=5,
                                height=22, command=self.principal.destroy)

        ## Alinhamento dos componentes
        self.lb_nome.place(x=10, y=10)
        self.lb_cpf.place(x=10, y=40)
        self.lb_tel.place(x=205, y=40)
        self.lb_equipe.place(x=10, y=70)
        self.lb_turno.place(x=205, y=70)

        self.cx_nome.place(x=60, y=10)
        self.cx_cpf.place(x=60, y=40)
        self.cx_tel.place(x=265, y=40)
        self.cx_equipe.place(x=60, y=70)
        self.cx_turno.place(x=265, y=70)

        self.bt_salvar.place(x=245, y=100)
        self.bt_fechar.place(x=320, y=100)

        self.principal.focus_force()  # Mantem o focus na janela ativa
        self.principal.grab_set()  # Matem no top até ser fechada

        ## Se estiver CPF, preenche os campos ativando o modo Edição
        if self.cpf:
            self.preencher_campos()

        self.principal.mainloop()  ## Abre a janela no momento em que a classe é estanciada

    ## Função para verificar se está no modo edição para salvar ou atualizar no banco
    def salvar(self):
        if self.cpf == False:
            self.cadastrar()
        else:
            self.editar()

    def cadastrar(self):
        if(self.cx_nome.get() and self.cx_cpf.get() and self.cx_tel.get() and self.cx_turno.get() and self.cx_equipe.get()) == '':
            tkinter.messagebox.showerror("Validação de campos", "Um ou mais campos estão em branco. Verifique os campos e tente novamente.", parent=self.principal)
        else:
            self.novo_tecnico = Tecnico(self.cx_nome.get(),
                                        self.cx_cpf.get(),
                                        self.cx_tel.get(),
                                        self.cx_turno.get(),
                                        self.cx_equipe.get())

            if self.novo_tecnico.cadastra_banco():
                tkinter.messagebox.showinfo("Cadastro de Tecnico", "Cadastro realizado com sucesso!", parent=self.principal)
                self.principal.destroy()
            else:
                tkinter.messagebox.showerror("Falha ao cadastrar",
                                             "Não foi possível cadastrar os dados. Por favor verifique os campos novamente!",
                                             parent=self.principal)
                self.principal.lift()

    def preencher_campos(self):
        self.dados = Tecnico().consulta_banco(self.cpf)

        self.cx_nome.insert(0, self.dados[0][0])
        self.cx_cpf.insert(0, self.dados[0][1])
        self.cx_cpf.config(state='disabled')
        self.cx_tel.insert(0, self.dados[0][2])
        self.cx_equipe.insert(0, self.dados[0][4])
        self.cx_turno.insert(0, self.dados[0][3])

    def editar(self):
        if (
                self.cx_nome.get() and self.cx_cpf.get() and self.cx_tel.get() and self.cx_turno.get() and self.cx_equipe.get()) == '':
            tkinter.messagebox.showerror("Validação de campos",
                                         "Um ou mais campos estão em branco. Verifique os campos e tente novamente",
                                         parent=self.principal)
        else:
            self.atualiza = Tecnico().atualiza_banco(set=(f"nome = '{self.cx_nome.get()}',"
                                                          f"telefone = '{self.cx_tel.get()}',"
                                                          f"turno = '{self.cx_turno.get()}',"
                                                          f"nome_equipe = '{self.cx_equipe.get()}'"),
                                                     where=f"cpf = '{self.cx_cpf.get()}'")
            if self.atualiza:
                tkinter.messagebox.showinfo("Editar técnico", "Técnico editado com sucesso!", parent=self.principal)
                self.principal.destroy()
            else:
                tkinter.messagebox.showerror("Falha ao editar",
                                             "Não foi possível editar o técnico. Por favor, tente novamente.",
                                             parent=self.principal)
                self.principal.lift()

    def format_cpf(self, event=None):
        texto = self.cx_cpf.get().replace(".", "").replace("-", "")[:11]
        novo_texto = ""

        if event.keysym.lower() == "backspace": return

        for index in range(len(texto)):
            if not texto[index] in "0123456789": continue
            if index in [2, 5]:
                novo_texto += texto[index] + "."
            elif index == 8:
                novo_texto += texto[index] + "-"
            else:
                novo_texto += texto[index]

        self.cx_cpf.delete(0, "end")
        self.cx_cpf.insert(0, novo_texto)

    def format_telefone(self, event=None):
        texto = self.cx_tel.get().replace(".", "").replace("-", "")[:13]
        novo_texto = "("

        if event.keysym.lower() == "backspace": return

        for index in range(len(texto)):
            if not texto[index] in "0123456789": continue
            if index in [2]:
                novo_texto += texto[index] + ")"
            elif index == 8:
                novo_texto += texto[index] + "-"
            else:
                novo_texto += texto[index]

        self.cx_tel.delete(0, "end")
        self.cx_tel.insert(0, novo_texto)