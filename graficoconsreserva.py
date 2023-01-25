import tkinter
from tkinter import Label, PhotoImage, Button, Entry, ttk, messagebox
from tkinter.ttk import Treeview

from graficoreserva import GraficoReserva
from sistema.centraliza_janelas import center
from reserva import Reserva

class GraficoConsultaReserva(Reserva):
    def __init__(self):
        self.principal = tkinter.Toplevel()
        self.principal.geometry("692x360")
        self.principal.title('Consultas - Reservas')
        self.principal.resizable(height=False, width=False)
        center(self.principal)

        ## Icones
        self.icon_cadastrar = PhotoImage(file="assets/icones/icon_cadastrar.png")
        self.icon_editar = PhotoImage(file="assets/icones/icon_editar.png")
        self.icon_remover = PhotoImage(file="assets/icones/icon_remove.png")
        self.icon_saida = PhotoImage(file="assets/icones/icon_saida.png")
        self.icon_pesquisar = PhotoImage(file="assets/icones/icon_pesquisar.png")
        self.icon_limpar = PhotoImage(file="assets/icones/icon_limpar.png")
        self.icon_atualizar = PhotoImage(file="assets/icones/icon_atualizar.png")

        ## Labels
        self.lb_busca = Label(self.principal, text="Buscar Reservas: ")
        self.lb_lista = Label(self.principal, text="Lista de Reservas: ")

        ## Caixas de texto
        self.cx_busca = Entry(self.principal, width=35, font='32')
        self.cx_opcoes = ttk.Combobox(self.principal, width=10, state="readonly")
        self.cx_opcoes['values'] = ("Técnico", "Ferramenta")
        self.cx_opcoes.current(0)

        ## Botões
        self.bt_atualizar = Button(self.principal, text="Atualizar", image=self.icon_atualizar, compound='left', padx=5,height=22, command=self.consulta_reserva)
        self.bt_pesquisa = Button(self.principal, text="Pesquisar", image=self.icon_pesquisar, compound='left', padx=5,height=22, command=self.pesquisa_reserva)
        self.bt_limpar = Button(self.principal, text="Limpar", image=self.icon_limpar, compound='left', padx=5,height=22, command=self.limpar_pesquisa)
        self.bt_cadastrar = Button(self.principal, text="Cadastrar", image=self.icon_cadastrar, compound='left', padx=5,height=22, command=GraficoReserva)
        self.bt_visul_edit = Button(self.principal, text="Visualizar/Editar", image=self.icon_editar, compound='left',padx=5, height=22, command=self.editar_reserva)
        self.bt_remover = Button(self.principal, text="Remover", image=self.icon_remover, compound='left', padx=5,height=22, command=self.remover_reserva)
        self.bt_fechar = Button(self.principal, text="Fechar", image=self.icon_saida, compound='left', padx=5,height=22, command=self.principal.destroy)

        ## Inicio da Lista de Reservas
        self.nomes_colunas = ('col1', 'col2', 'col3', 'col4', 'col5')
        self.lista_reservas = Treeview(self.principal, columns=self.nomes_colunas, show='headings', height=10)
        self.lista_reservas.column('col1', width=55, stretch=False)
        self.lista_reservas.column('col2', width=175, stretch=False)
        self.lista_reservas.column('col3', width=164, stretch=False)
        self.lista_reservas.column('col4', width=138, stretch=False)
        self.lista_reservas.column('col5', width=138, stretch=False)

        self.lista_reservas.heading('col1', text='Código')
        self.lista_reservas.heading('col2', text='Técnico')
        self.lista_reservas.heading('col3', text='Ferramenta')
        self.lista_reservas.heading('col4', text="Data e Hora/Retirada")
        self.lista_reservas.heading('col5', text="Data e Hora/Devolução")

        ## Fim da lista de reserva

        ## Alinhamento dos componentes
        self.lb_busca.place(x=10, y=10)
        self.lb_lista.place(x=10, y=80)

        self.cx_busca.place(x=10, y=40)
        self.cx_opcoes.place(x=335, y=41)

        self.bt_pesquisa.place(x=425, y=35)
        self.bt_atualizar.place(x=518, y=35)
        self.bt_limpar.place(x=608, y=35)

        self.lista_reservas.place(x=10, y=80)

        self.bt_cadastrar.place(x=10, y=320)
        self.bt_visul_edit.place(x=105, y=320)
        self.bt_remover.place(x=235, y=320)
        self.bt_fechar.place(x=610, y=320)

        self.consulta_reserva()

        self.principal.mainloop() ## Abre a janela no momento que a classe é chamada ou estanciada!

    def consulta_reserva(self):
        if self.cx_busca.get() != '':
            self.pesquisa_reserva()
        else:
            self.lista_reservas.delete(*self.lista_reservas.get_children())
            consulta = self.listar_reservas_cadastradas()

            for valor in consulta:
                self.lista_reservas.insert('', tkinter.END, values=(valor[9], valor[1], valor[3],
                                                                    f'{valor[4]} - {valor[5]}', f'{valor[6]} - {valor[7]}'))

    def pesquisa_reserva(self):
        var_busca = 'nome_tecnico'

        if self.cx_opcoes.get() == "Técnico":
            var_busca = 'nome_tecnico'
        elif self.cx_opcoes.get() == "Ferramenta":
            var_busca = 'nome_ferramenta'

        self.lista_reservas.delete(*self.lista_reservas.get_children())
        consulta = self.pesquisar_banco(campo=var_busca, pesquisa=self.cx_busca.get())

        for valor in consulta:
            self.lista_reservas.insert('', tkinter.END, values=(valor[9], valor[1], valor[3],
                                                                f'{valor[4]} - {valor[5]}', f'{valor[6]} - {valor[7]}'))

    def limpar_pesquisa(self):
        self.cx_busca.delete(0, 'end')

    def remover_reserva(self):
        self.codigo_selecionado = False

        for item_selecionado in self.lista_reservas.selection():
            self.codigo_selecionado = \
                self.lista_reservas.item(item_selecionado)['values'][0]

        if self.codigo_selecionado:
            banco = self.remover_banco(self.codigo_selecionado)

            if banco:
                tkinter.messagebox.showinfo('Reserva removida', 'A reserva selecionada foi removida com sucesso!', parent=self.principal)
                self.consulta_reserva()
        else:
            tkinter.messagebox.showerror('Erro ao remover reserva', 'Por favor, selecione uma reserva na lista para realizar sua remoção', parent=self.principal)
            self.principal.lift()

    def editar_reserva(self):
        self.codigo_selecionado = False

        for item_selecionado in self.lista_reservas.selection():
            self.codigo_selecionado = \
                self.lista_reservas.item(item_selecionado)['values'][0]

        if self.codigo_selecionado == False:
            tkinter.messagebox.showerror("Erro ao abrir reserva",
                                         "Por favor, selecione uma reserva na lista para realizar sua Visualização/Edição.",
                                         parent=self.principal)
        else:
            GraficoReserva(self.codigo_selecionado)