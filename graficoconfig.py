import tkinter
from tkinter import Label, Button, Entry, messagebox, PhotoImage

from config import Config
from sistema.centraliza_janelas import center


class GraficoConfig(Config):
    def __init__(self):
        super().__init__()
        self.principal = tkinter.Toplevel() #Top Level pois ela é filha de graficomain.py

        ## Ajustar tamanho da janela e não permitir maximizar.
        self.principal.geometry("260x310")
        self.principal.resizable(width=False, height=False)

        self.principal.title('Config Email')
        center(self.principal)

        ## Labels.
        self.lb_banco = Label(self.principal, font='Helvetica 12 bold', text="Acesso ao Banco de Dados")
        self.lb_host = Label(self.principal, text="Host: ")
        self.lb_usuario = Label(self.principal, text="Usuário: ")
        self.lb_senha = Label(self.principal, text="Senha: ")
        self.lb_porta = Label(self.principal, text="Porta: ")
        self.lb_remetente = Label(self.principal, text="Remetente: ")
        self.lb_reserva = Label(self.principal, font='Helvetica 12 bold', text="Envio de Reservas")
        self.lb_email = Label(self.principal, text="Email: ")

        ## Icones.
        self.icon_salvar = PhotoImage(file="assets/icones/icon_salvar.png")
        self.icon_sair = PhotoImage(file="assets/icones/icon_saida.png")

        ## Caixas de texto.
        self.cx_host = Entry(self.principal, width=27)
        self.cx_usuario = Entry(self.principal, width=27)
        self.cx_senha = Entry(self.principal, width=27)
        self.cx_porta = Entry(self.principal, width=15)
        self.cx_remetente = Entry(self.principal, width=27)
        self.cx_email = Entry(self.principal, width=27)

        ## Botões.
        self.bt_salvar = Button(self.principal, image=self.icon_salvar, compound='left', height=22, padx=5,
                               text="Salvar", command=self._salvar)
        self.bt_fechar = Button(self.principal, image=self.icon_sair, compound='left', height=22, padx=5, text="Fechar",
                               command=self.principal.destroy)

        ## Alinhamento dos componentes
        self.lb_banco.place(x=20, y=10)
        self.lb_host.place(x=10, y=40)
        self.lb_usuario.place(x=10, y=70)
        self.lb_senha.place(x=10, y=100)
        self.lb_porta.place(x=10, y=130)
        self.lb_remetente.place(x=10, y=160)
        self.lb_reserva.place(x=60, y=210)
        self.lb_email.place(x=10, y=240)

        self.cx_host.place(x=80, y=40)
        self.cx_usuario.place(x=80, y=70)
        self.cx_senha.place(x=80, y=100)
        self.cx_porta.place(x=80, y=130)
        self.cx_remetente.place(x=80, y=160)
        self.cx_email.place(x=80, y=240)

        self.bt_salvar.place(x=105, y=270)
        self.bt_fechar.place(x=180, y=270)

        self._preenche_campos() ## Função para preencher os campos no momento que a classe é estanciada.

        self.principal.focus_force()  # Mantem o focus na janela ativa
        self.principal.grab_set()  # Matem no top até ser fechada

        self.principal.mainloop() ## Abre a janela no momento que a classe é chamada ou estanciada.

    ## Preenche os campos
    def _preenche_campos(self):
        dados = self._carregar_configuracao()[0]

        # Havendo dados ele completa os campos do formulário.
        if dados != False:
            self.cx_host.insert(0, dados[0])
            self.cx_usuario.insert(0, dados[1])
            self.cx_senha.insert(0, dados[2])
            self.cx_porta.insert(0, dados[3])
            self.cx_remetente.insert(0, dados[5])
            self.cx_email.insert(0, dados[6])

    ## Salva dados no banco.
    def _salvar(self):
        resposta = self._salvar_configuracao(dados=(self.cx_host.get(),
                                                    self.cx_usuario.get(),
                                                    self.cx_senha.get(),
                                                    self.cx_porta.get(),
                                                    self.cx_remetente.get(),
                                                    self.cx_email.get()))

        ## Mostra alert de sucesso ou erro dependendo da resposta do banco.
        if resposta:
            tkinter.messagebox.showinfo('Salvar Configuração', 'Dados salvos com sucesso!')
            self.principal.destroy()
        else:
            tkinter.messagebox.showerror('Erro ao Salvar',
                                         "Erro ao salvar as informações. Por favor, verifique os campos.")
            self.principal.lift()  # Puxa a janela novamente para frente após exibir o aviso.