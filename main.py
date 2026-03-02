import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from datetime import datetime, timedelta
import json
import os
from functools import partial

# Configurar tamanho da janela
Window.size = (360, 640)

# Estruturas de dados
class Cliente:
    def __init__(self, nome, telefone, aniversario, email=""):
        self.nome = nome
        self.telefone = telefone
        self.aniversario = aniversario
        self.email = email
        self.historico = []
        self.total_gasto = 0.0

class Agendamento:
    def __init__(self, cliente, servico, data, hora, duracao=60):
        self.cliente = cliente
        self.servico = servico
        self.data = data
        self.hora = hora
        self.duracao = duracao
        self.status = "agendado"

class Servico:
    def __init__(self, nome, preco, duracao=60):
        self.nome = nome
        self.preco = preco
        self.duracao = duracao

class Transacao:
    def __init__(self, cliente, valor, tipo, data, descricao=""):
        self.cliente = cliente
        self.valor = valor
        self.tipo = tipo
        self.data = data
        self.descricao = descricao

# Tela Principal
class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.clientes = []
        self.agendamentos = []
        self.servicos = []
        self.transacoes = []
        self.carregar_dados()
        self.setup_ui()
    
    def setup_ui(self):
        # CabeÃ§alho com estilo moderno
        header = BoxLayout(size_hint_y=0.12, padding=[15, 10], spacing=10)
        with header.canvas.before:
            Color(0.4, 0.2, 0.8, 1)
            Rectangle(size=header.size, pos=header.pos)
        
        title_label = Label(
            text="Bianca Beauty",
            font_size='24sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        header.add_widget(title_label)
        self.add_widget(header)
        
        # Tabs principais
        self.tabs = TabbedPanel(do_default_tab=False)
        
        agenda_tab = TabbedPanelItem(text="Agenda")
        agenda_tab.add_widget(self.criar_agenda_view())
        self.tabs.add_widget(agenda_tab)
        
        clientes_tab = TabbedPanelItem(text="Clientes")
        clientes_tab.add_widget(self.criar_clientes_view())
        self.tabs.add_widget(clientes_tab)
        
        relatorios_tab = TabbedPanelItem(text="Relatorios")
        relatorios_tab.add_widget(self.criar_relatorios_view())
        self.tabs.add_widget(relatorios_tab)
        
        financeiro_tab = TabbedPanelItem(text="Financeiro")
        financeiro_tab.add_widget(self.criar_financeiro_view())
        self.tabs.add_widget(financeiro_tab)
        
        servicos_tab = TabbedPanelItem(text="Servicos")
        servicos_tab.add_widget(self.criar_servicos_view())
        self.tabs.add_widget(servicos_tab)
        
        self.add_widget(self.tabs)
    
    def criar_agenda_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        data_atual = datetime.now().strftime("%d/%m/%Y")
        cabecalho = BoxLayout(size_hint_y=0.12, spacing=10)
        cabecalho.add_widget(Label(text="Hoje: " + data_atual, font_size='16sp', bold=True))
        
        btn_novo = Button(text="+ Novo", size_hint_x=0.3, background_color=(0.4, 0.2, 0.8, 1))
        btn_novo.bind(on_press=self.novo_agendamento)
        cabecalho.add_widget(btn_novo)
        layout.add_widget(cabecalho)
        
        scroll = ScrollView()
        self.agenda_lista = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.agenda_lista.bind(minimum_height=self.agenda_lista.setter('height'))
        
        self.atualizar_agenda_view()
        
        scroll.add_widget(self.agenda_lista)
        layout.add_widget(scroll)
        
        return layout
    
    def criar_clientes_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        barra = BoxLayout(size_hint_y=0.12, spacing=5)
        self.busca_input = TextInput(hint_text="Buscar cliente...", multiline=False)
        btn_busca = Button(text="Buscar", size_hint_x=0.2, background_color=(0.4, 0.2, 0.8, 1))
        btn_busca.bind(on_press=self.buscar_clientes)
        
        btn_novo = Button(text="+ Novo", size_hint_x=0.25, background_color=(0.4, 0.2, 0.8, 1))
        btn_novo.bind(on_press=self.novo_cliente)
        
        barra.add_widget(self.busca_input)
        barra.add_widget(btn_busca)
        barra.add_widget(btn_novo)
        layout.add_widget(barra)
        
        scroll = ScrollView()
        self.clientes_lista = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.clientes_lista.bind(minimum_height=self.clientes_lista.setter('height'))
        
        self.atualizar_clientes_view()
        
        scroll.add_widget(self.clientes_lista)
        layout.add_widget(scroll)
        
        aniversariantes = self.get_aniversariantes()
        if aniversariantes:
            aniv_box = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
            aniv_label = Label(
                text="Aniversariantes (proximos 14 dias):",
                size_hint_y=0.3,
                font_size='12sp',
                bold=True
            )
            aniv_box.add_widget(aniv_label)
            
            for cliente in aniversariantes[:3]:
                aniv_box.add_widget(Label(
                    text=cliente.nome + " - " + cliente.aniversario,
                    size_hint_y=0.23,
                    font_size='11sp'
                ))
            layout.add_widget(aniv_box)
        
        return layout
    
    def criar_relatorios_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        cards_layout = GridLayout(cols=2, size_hint_y=0.5, spacing=10)
        
        card1 = BoxLayout(orientation='vertical', padding=10)
        with card1.canvas.before:
            Color(0.2, 0.6, 0.8, 0.8)
            Rectangle(size=card1.size, pos=card1.pos)
        card1.add_widget(Label(text="Total Clientes", font_size='12sp', color=(1,1,1,1)))
        card1.add_widget(Label(text=str(len(self.clientes)), font_size='22sp', bold=True, color=(1,1,1,1)))
        cards_layout.add_widget(card1)
        
        card2 = BoxLayout(orientation='vertical', padding=10)
        with card2.canvas.before:
            Color(0.2, 0.8, 0.4, 0.8)
            Rectangle(size=card2.size, pos=card2.pos)
        card2.add_widget(Label(text="Receita Mes", font_size='12sp', color=(1,1,1,1)))
        receita_mes = sum(t.valor for t in self.transacoes if t.data.month == datetime.now().month)
        card2.add_widget(Label(text="R$ " + str(round(receita_mes, 2)), font_size='22sp', bold=True, color=(1,1,1,1)))
        cards_layout.add_widget(card2)
        
        card3 = BoxLayout(orientation='vertical', padding=10)
        with card3.canvas.before:
            Color(0.8, 0.4, 0.2, 0.8)
            Rectangle(size=card3.size, pos=card3.pos)
        card3.add_widget(Label(text="Melhor Cliente", font_size='12sp', color=(1,1,1,1)))
        if self.clientes:
            melhor = max(self.clientes, key=lambda c: c.total_gasto)
            card3.add_widget(Label(text=melhor.nome, font_size='14sp', color=(1,1,1,1)))
            card3.add_widget(Label(text="R$ " + str(round(melhor.total_gasto, 2)), font_size='16sp', bold=True, color=(1,1,1,1)))
        cards_layout.add_widget(card3)
        
        card4 = BoxLayout(orientation='vertical', padding=10)
        with card4.canvas.before:
            Color(0.8, 0.2, 0.6, 0.8)
            Rectangle(size=card4.size, pos=card4.pos)
        card4.add_widget(Label(text="Servicos Top", font_size='12sp', color=(1,1,1,1)))
        servicos_count = {}
        for a in self.agendamentos:
            servicos_count[a.servico] = servicos_count.get(a.servico, 0) + 1
        
        top_servicos = sorted(servicos_count.items(), key=lambda x: x[1], reverse=True)[:1]
        for servico, count in top_servicos:
            card4.add_widget(Label(text=servico + ": " + str(count) + "x", font_size='14sp', color=(1,1,1,1)))
        cards_layout.add_widget(card4)
        
        layout.add_widget(cards_layout)
        
        scroll = ScrollView()
        info_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        info_layout.bind(minimum_height=info_layout.setter('height'))
        
        info_layout.add_widget(Label(text="Estatisticas:", size_hint_y=None, height=30, bold=True))
        total_agendamentos = len(self.agendamentos)
        info_layout.add_widget(Label(text="Total Agendamentos: " + str(total_agendamentos), size_hint_y=None, height=30))
        
        scroll.add_widget(info_layout)
        layout.add_widget(scroll)
        
        return layout
    
    def criar_financeiro_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        resumo = GridLayout(cols=2, size_hint_y=0.35, spacing=10, padding=10)
        
        receita = sum(t.valor for t in self.transacoes)
        despesas = 750.93
        lucro = receita - despesas
        
        card_receita = BoxLayout(orientation='vertical', padding=10)
        with card_receita.canvas.before:
            Color(0.2, 0.8, 0.4, 0.8)
            Rectangle(size=card_receita.size, pos=card_receita.pos)
        card_receita.add_widget(Label(text="Receita:", color=(1,1,1,1)))
        card_receita.add_widget(Label(text="R$ " + str(round(receita, 2)), font_size='18sp', bold=True, color=(1,1,1,1)))
        resumo.add_widget(card_receita)
        
        card_despesas = BoxLayout(orientation='vertical', padding=10)
        with card_despesas.canvas.before:
            Color(0.8, 0.2, 0.2, 0.8)
            Rectangle(size=card_despesas.size, pos=card_despesas.pos)
        card_despesas.add_widget(Label(text="Despesas:", color=(1,1,1,1)))
        card_despesas.add_widget(Label(text="R$ " + str(round(despesas, 2)), font_size='18sp', bold=True, color=(1,1,1,1)))
        resumo.add_widget(card_despesas)
        
        card_lucro = BoxLayout(orientation='vertical', padding=10)
        with card_lucro.canvas.before:
            Color(0.4, 0.2, 0.8, 0.8)
            Rectangle(size=card_lucro.size, pos=card_lucro.pos)
        card_lucro.add_widget(Label(text="Lucro:", color=(1,1,1,1)))
        card_lucro.add_widget(Label(text="R$ " + str(round(lucro, 2)), font_size='18sp', bold=True, color=(1,1,1,1)))
        resumo.add_widget(card_lucro)
        
        layout.add_widget(resumo)
        
        formas = GridLayout(cols=2, size_hint_y=0.4, spacing=5, padding=10)
        formas.add_widget(Label(text="Dinheiro:", bold=True))
        valor_dinheiro = sum(t.valor for t in self.transacoes if t.tipo == "dinheiro")
        formas.add_widget(Label(text="R$ " + str(round(valor_dinheiro, 2))))
        
        formas.add_widget(Label(text="Credito:", bold=True))
        valor_credito = sum(t.valor for t in self.transacoes if t.tipo == "credito")
        formas.add_widget(Label(text="R$ " + str(round(valor_credito, 2))))
        
        formas.add_widget(Label(text="Debito:", bold=True))
        valor_debito = sum(t.valor for t in self.transacoes if t.tipo == "debito")
        formas.add_widget(Label(text="R$ " + str(round(valor_debito, 2))))
        
        layout.add_widget(formas)
        
        btn_nova = Button(text="+ Nova Transacao", size_hint_y=0.1, background_color=(0.4, 0.2, 0.8, 1))
        btn_nova.bind(on_press=self.nova_transacao)
        layout.add_widget(btn_nova)
        
        return layout
    
    def criar_servicos_view(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        scroll = ScrollView()
        servicos_lista = GridLayout(cols=1, spacing=5, size_hint_y=None)
        servicos_lista.bind(minimum_height=servicos_lista.setter('height'))
        
        for servico in self.servicos:
            item = BoxLayout(size_hint_y=None, height=50, padding=5, spacing=10)
            with item.canvas.before:
                Color(0.9, 0.9, 0.9, 1)
                Rectangle(size=item.size, pos=item.pos)
            
            item.add_widget(Label(text=servico.nome, bold=True))
            item.add_widget(Label(text="R$ " + str(round(servico.preco, 2)), halign='right'))
            item.add_widget(Label(text=str(servico.duracao) + "min", size_hint_x=0.2))
            servicos_lista.add_widget(item)
        
        scroll.add_widget(servicos_lista)
        layout.add_widget(scroll)
        
        btn_novo = Button(text="+ Novo Servico", size_hint_y=0.1, background_color=(0.4, 0.2, 0.8, 1))
        btn_novo.bind(on_press=self.novo_servico)
        layout.add_widget(btn_novo)
        
        return layout
    
    def atualizar_agenda_view(self):
        self.agenda_lista.clear_widgets()
        hoje = datetime.now().date()
        agendamentos_hoje = [a for a in self.agendamentos if a.data.date() == hoje]
        
        if not agendamentos_hoje:
            self.agenda_lista.add_widget(Label(text="Nenhum agendamento para hoje", size_hint_y=None, height=40))
            return
        
        for ag in sorted(agendamentos_hoje, key=lambda x: x.hora):
            item = BoxLayout(orientation='vertical', size_hint_y=None, height=90, padding=[5])
            with item.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                Rectangle(size=item.size, pos=item.pos)
            
            item.add_widget(Label(text=ag.hora + " - " + ag.cliente, bold=True, halign='left', size_hint_y=0.3))
            item.add_widget(Label(text=ag.servico, halign='left', size_hint_y=0.3))
            
            botoes = BoxLayout(size_hint_y=0.4, spacing=3)
            btn_whats = Button(text="WhatsApp", size_hint_x=0.33, background_color=(0.2, 0.8, 0.4, 1))
            btn_whats.bind(on_press=lambda x, a=ag: self.enviar_whats(a))
            
            btn_confirmar = Button(text="Confirmar", size_hint_x=0.33, background_color=(0.4, 0.2, 0.8, 1))
            btn_confirmar.bind(on_press=lambda x, a=ag: self.confirmar_agendamento(a))
            
            btn_cancelar = Button(text="Cancelar", size_hint_x=0.33, background_color=(0.8, 0.2, 0.2, 1))
            btn_cancelar.bind(on_press=lambda x, a=ag: self.cancelar_agendamento(a))
            
            botoes.add_widget(btn_whats)
            botoes.add_widget(btn_confirmar)
            botoes.add_widget(btn_cancelar)
            
            item.add_widget(botoes)
            self.agenda_lista.add_widget(item)
    
    def atualizar_clientes_view(self, filtro=""):
        self.clientes_lista.clear_widgets()
        for cliente in self.clientes:
            if filtro.lower() in cliente.nome.lower() or filtro == "":
                item = BoxLayout(orientation='vertical', size_hint_y=None, height=70, padding=[5], spacing=3)
                with item.canvas.before:
                    Color(0.95, 0.95, 0.95, 1)
                    Rectangle(size=item.size, pos=item.pos)
                
                linha1 = BoxLayout(size_hint_y=0.4, spacing=5)
                linha1.add_widget(Label(text=cliente.nome, bold=True, halign='left'))
                linha1.add_widget(Label(text="R$ " + str(round(cliente.total_gasto, 2)), halign='right'))
                
                linha2 = BoxLayout(size_hint_y=0.6, spacing=2)
                btn_editar = Button(text="Editar", size_hint_x=0.25, background_color=(0.4, 0.2, 0.8, 1))
                btn_editar.bind(on_press=lambda x, c=cliente: self.editar_cliente(c))
                
                btn_agendar = Button(text="Agendar", size_hint_x=0.25, background_color=(0.2, 0.6, 0.8, 1))
                btn_agendar.bind(on_press=lambda x, c=cliente: self.agendar_cliente(c))
                
                btn_historico = Button(text="Historico", size_hint_x=0.25, background_color=(0.8, 0.6, 0.2, 1))
                btn_historico.bind(on_press=lambda x, c=cliente: self.ver_historico(c))
                
                btn_whats = Button(text="WhatsApp", size_hint_x=0.25, background_color=(0.2, 0.8, 0.4, 1))
                btn_whats.bind(on_press=lambda x, c=cliente: self.enviar_whats_cliente(c))
                
                linha2.add_widget(btn_editar)
                linha2.add_widget(btn_agendar)
                linha2.add_widget(btn_historico)
                linha2.add_widget(btn_whats)
                
                item.add_widget(linha1)
                item.add_widget(linha2)
                self.clientes_lista.add_widget(item)
    
    def get_aniversariantes(self):
        hoje = datetime.now()
        aniversariantes = []
        for cliente in self.clientes:
            if cliente.aniversario:
                try:
                    dia, mes = map(int, cliente.aniversario.split('/'))
                    data_aniv = datetime(hoje.year, mes, dia)
                    if data_aniv < hoje:
                        data_aniv = datetime(hoje.year + 1, mes, dia)
                    dias = (data_aniv - hoje).days
                    if dias <= 14:
                        aniversariantes.append(cliente)
                except:
                    pass
        return sorted(aniversariantes, key=lambda c: c.aniversario)
    
    def novo_agendamento(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        cliente_input = TextInput(hint_text="Nome do cliente", multiline=False)
        servico_input = TextInput(hint_text="Servico", multiline=False)
        data_input = TextInput(hint_text="Data (DD/MM/AAAA)", multiline=False)
        hora_input = TextInput(hint_text="Hora (HH:MM)", multiline=False)
        
        content.add_widget(cliente_input)
        content.add_widget(servico_input)
        content.add_widget(data_input)
        content.add_widget(hora_input)
        
        botoes = BoxLayout(size_hint_y=0.3, spacing=10)
        btn_salvar = Button(text="Salvar", background_color=(0.4, 0.2, 0.8, 1))
        btn_cancelar = Button(text="Cancelar", background_color=(0.8, 0.2, 0.2, 1))
        botoes.add_widget(btn_salvar)
        botoes.add_widget(btn_cancelar)
        content.add_widget(botoes)
        
        popup = Popup(title="Novo Agendamento", content=content, size_hint=(0.9, 0.7))
        
        def salvar(instance):
            try:
                novo = Agendamento(
                    cliente_input.text,
                    servico_input.text,
                    datetime.strptime(data_input.text, "%d/%m/%Y"),
                    hora_input.text
                )
                self.agendamentos.append(novo)
                self.salvar_dados()
                self.atualizar_agenda_view()
                popup.dismiss()
            except Exception as e:
                print("Erro ao salvar agendamento: " + str(e))
        
        btn_salvar.bind(on_press=salvar)
        btn_cancelar.bind(on_press=popup.dismiss)
        popup.open()
    
    def novo_cliente(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        nome_input = TextInput(hint_text="Nome completo", multiline=False)
        tel_input = TextInput(hint_text="Telefone", multiline=False)
        aniv_input = TextInput(hint_text="Aniversario (DD/MM)", multiline=False)
        email_input = TextInput(hint_text="E-mail (opcional)", multiline=False)
        
        content.add_widget(nome_input)
        content.add_widget(tel_input)
        content.add_widget(aniv_input)
        content.add_widget(email_input)
        
        botoes = BoxLayout(size_hint_y=0.3, spacing=10)
        btn_salvar = Button(text="Salvar", background_color=(0.4, 0.2, 0.8, 1))
        btn_cancelar = Button(text="Cancelar", background_color=(0.8, 0.2, 0.2, 1))
        botoes.add_widget(btn_salvar)
        botoes.add_widget(btn_cancelar)
        content.add_widget(botoes)
        
        popup = Popup(title="Novo Cliente", content=content, size_hint=(0.9, 0.7))
        
        def salvar(instance):
            try:
                novo = Cliente(
                    nome_input.text,
                    tel_input.text,
                    aniv_input.text,
                    email_input.text
                )
                self.clientes.append(novo)
                self.salvar_dados()
                self.atualizar_clientes_view()
                popup.dismiss()
            except Exception as e:
                print("Erro ao salvar cliente: " + str(e))
        
        btn_salvar.bind(on_press=salvar)
        btn_cancelar.bind(on_press=popup.dismiss)
        popup.open()
    
    def novo_servico(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        nome_input = TextInput(hint_text="Nome do servico", multiline=False)
        preco_input = TextInput(hint_text="Preco (R$)", multiline=False)
        duracao_input = TextInput(hint_text="Duracao (minutos)", multiline=False)
        
        content.add_widget(nome_input)
        content.add_widget(preco_input)
        content.add_widget(duracao_input)
        
        botoes = BoxLayout(size_hint_y=0.3, spacing=10)
        btn_salvar = Button(text="Salvar", background_color=(0.4, 0.2, 0.8, 1))
        btn_cancelar = Button(text="Cancelar", background_color=(0.8, 0.2, 0.2, 1))
        botoes.add_widget(btn_salvar)
        botoes.add_widget(btn_cancelar)
        content.add_widget(botoes)
        
        popup = Popup(title="Novo Servico", content=content, size_hint=(0.9, 0.6))
        
        def salvar(instance):
            try:
                novo = Servico(
                    nome_input.text,
                    float(preco_input.text.replace(',', '.')),
                    int(duracao_input.text)
                )
                self.servicos.append(novo)
                self.salvar_dados()
                popup.dismiss()
            except Exception as e:
                print("Erro ao salvar servico: " + str(e))
        
        btn_salvar.bind(on_press=salvar)
        btn_cancelar.bind(on_press=popup.dismiss)
        popup.open()
    
    def nova_transacao(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        cliente_input = TextInput(hint_text="Cliente", multiline=False)
        valor_input = TextInput(hint_text="Valor (R$)", multiline=False)
        tipo_input = TextInput(hint_text="Tipo (dinheiro/credito/debito)", multiline=False)
        
        content.add_widget(cliente_input)
        content.add_widget(valor_input)
        content.add_widget(tipo_input)
        
        botoes = BoxLayout(size_hint_y=0.3, spacing=10)
        btn_salvar = Button(text="Salvar", background_color=(0.4, 0.2, 0.8, 1))
        btn_cancelar = Button(text="Cancelar", background_color=(0.8, 0.2, 0.2, 1))
        botoes.add_widget(btn_salvar)
        botoes.add_widget(btn_cancelar)
        content.add_widget(botoes)
        
        popup = Popup(title="Nova Transacao", content=content, size_hint=(0.9, 0.6))
        
        def salvar(instance):
            try:
                nova = Transacao(
                    cliente_input.text,
                    float(valor_input.text.replace(',', '.')),
                    tipo_input.text.lower(),
                    datetime.now()
                )
                self.transacoes.append(nova)
                
                for c in self.clientes:
                    if c.nome == cliente_input.text:
                        c.total_gasto += nova.valor
                        c.historico.append("Pagamento: R$ " + str(round(nova.valor, 2)))
                
                self.salvar_dados()
                popup.dismiss()
            except Exception as e:
                print("Erro ao salvar transacao: " + str(e))
        
        btn_salvar.bind(on_press=salvar)
        btn_cancelar.bind(on_press=popup.dismiss)
        popup.open()
    
    def buscar_clientes(self, instance):
        self.atualizar_clientes_view(self.busca_input.text)
    
    def editar_cliente(self, cliente):
        pass
    
    def agendar_cliente(self, cliente):
        self.novo_agendamento(None)
    
    def ver_historico(self, cliente):
        content = BoxLayout(orientation='vertical')
        scroll = ScrollView()
        lista = GridLayout(cols=1, spacing=5, size_hint_y=None)
        lista.bind(minimum_height=lista.setter('height'))
        
        if cliente.historico:
            for item in cliente.historico:
                lista.add_widget(Label(text=item, size_hint_y=None, height=30))
        else:
            lista.add_widget(Label(text="Sem historico", size_hint_y=None, height=30))
        
        scroll.add_widget(lista)
        content.add_widget(scroll)
        
        btn_fechar = Button(text="Fechar", size_hint_y=0.1, background_color=(0.8, 0.2, 0.2, 1))
        content.add_widget(btn_fechar)
        
        popup = Popup(title="Historico de " + cliente.nome, content=content, size_hint=(0.9, 0.7))
        btn_fechar.bind(on_press=popup.dismiss)
        popup.open()
    
    def enviar_whats_cliente(self, cliente):
        mensagem = "Ola " + cliente.nome + "! Bem-vindo ao Mychelle Beauty!"
        popup = Popup(
            title="WhatsApp",
            content=Label(text="Mensagem para " + cliente.telefone + ":\n\n" + mensagem),
            size_hint=(0.8, 0.4)
        )
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
        popup.open()
    
    def enviar_whats(self, agendamento):
        mensagem = "Ola " + agendamento.cliente + "! Voce tem um agendamento em Mychelle Beauty as " + agendamento.hora + " para " + agendamento.servico
        for c in self.clientes:
            if c.nome == agendamento.cliente:
                popup = Popup(
                    title="WhatsApp",
                    content=Label(text="Mensagem para " + c.telefone + ":\n\n" + mensagem),
                    size_hint=(0.8, 0.4)
                )
                Clock.schedule_once(lambda dt: popup.dismiss(), 2)
                popup.open()
                break
    
    def confirmar_agendamento(self, agendamento):
        agendamento.status = "confirmado"
        self.salvar_dados()
        self.atualizar_agenda_view()
    
    def cancelar_agendamento(self, agendamento):
        self.agendamentos.remove(agendamento)
        self.salvar_dados()
        self.atualizar_agenda_view()
    
    def salvar_dados(self):
        dados = {
            'clientes': [],
            'agendamentos': [],
            'servicos': [],
            'transacoes': []
        }
        
        for c in self.clientes:
            dados['clientes'].append({
                'nome': c.nome,
                'telefone': c.telefone,
                'aniversario': c.aniversario,
                'email': c.email,
                'total_gasto': c.total_gasto,
                'historico': c.historico
            })
        
        for a in self.agendamentos:
            dados['agendamentos'].append({
                'cliente': a.cliente,
                'servico': a.servico,
                'data': a.data.isoformat() if a.data else None,
                'hora': a.hora,
                'status': a.status
            })
        
        for s in self.servicos:
            dados['servicos'].append({
                'nome': s.nome,
                'preco': s.preco,
                'duracao': s.duracao
            })
        
        for t in self.transacoes:
            dados['transacoes'].append({
                'cliente': t.cliente,
                'valor': t.valor,
                'tipo': t.tipo,
                'data': t.data.isoformat() if t.data else None,
                'descricao': t.descricao
            })
        
        with open('dados_app.json', 'w') as f:
            json.dump(dados, f, indent=2)
    
    def carregar_dados(self):
        if not os.path.exists('dados_app.json'):
            self.carregar_dados_exemplo()
            return
        
        try:
            with open('dados_app.json', 'r') as f:
                dados = json.load(f)
            
            self.clientes = []
            for c in dados.get('clientes', []):
                cliente = Cliente(
                    c.get('nome', ''),
                    c.get('telefone', ''),
                    c.get('aniversario', ''),
                    c.get('email', '')
                )
                cliente.total_gasto = c.get('total_gasto', 0.0)
                cliente.historico = c.get('historico', [])
                self.clientes.append(cliente)
            
            self.agendamentos = []
            for a in dados.get('agendamentos', []):
                ag = Agendamento(
                    a.get('cliente', ''),
                    a.get('servico', ''),
                    datetime.fromisoformat(a['data']) if a.get('data') else datetime.now(),
                    a.get('hora', '')
                )
                ag.status = a.get('status', 'agendado')
                self.agendamentos.append(ag)
            
            self.servicos = []
            for s in dados.get('servicos', []):
                serv = Servico(
                    s.get('nome', ''),
                    s.get('preco', 0.0),
                    s.get('duracao', 60)
                )
                self.servicos.append(serv)
            
            self.transacoes = []
            for t in dados.get('transacoes', []):
                trans = Transacao(
                    t.get('cliente', ''),
                    t.get('valor', 0.0),
                    t.get('tipo', 'dinheiro'),
                    datetime.fromisoformat(t['data']) if t.get('data') else datetime.now(),
                    t.get('descricao', '')
                )
                self.transacoes.append(trans)
        
        except Exception as e:
            print("Erro ao carregar dados: " + str(e))
            self.carregar_dados_exemplo()
    
    def carregar_dados_exemplo(self):
        self.clientes = [
            Cliente("Juliana", "1199999999", "29/05", "juliana@email.com"),
            Cliente("Flavia", "1198888888", "05/06", "flavia@email.com"),
            Cliente("Mariana", "1197777777", "10/06", "mariana@email.com"),
            Cliente("Adriana", "1196666666", "11/06", "adriana@email.com"),
            Cliente("Carolina", "1195555555", "15/03", "carolina@email.com"),
            Cliente("Cassiana", "1194444444", "20/04", "cassiana@email.com"),
            Cliente("Dayana", "1193333333", "25/07", "dayana@email.com"),
        ]
        
        totais = [1324.00, 1226.00, 1217.00, 1205.00, 1193.00, 1090.00, 1028.00]
        for i, c in enumerate(self.clientes[:7]):
            c.total_gasto = totais[i]
            c.historico.append("Total gasto: R$ " + str(round(c.total_gasto, 2)))
        
        self.servicos = [
            Servico("Micropigmentacao", 250.00, 120),
            Servico("Pe e mao", 60.00, 60),
            Servico("Sobrancelha", 45.00, 30),
            Servico("Massagem", 80.00, 60),
            Servico("Corte Cabelo", 50.00, 45),
            Servico("Maquiagem", 120.00, 90),
        ]
        
        hoje = datetime.now()
        self.agendamentos = [
            Agendamento("Juliana", "Pe e mao", hoje, "10:00"),
            Agendamento("Carla Camargo", "Sobrancelha", hoje, "09:00"),
            Agendamento("Carla Camargo", "Corte Cabelo", hoje, "09:30"),
            Agendamento("Gabriela", "Micropigmentacao", hoje, "11:00"),
            Agendamento("Bruno", "Maquiagem", hoje, "08:00"),
            Agendamento("Flavia", "Sobrancelha", hoje + timedelta(days=4), "08:30"),
        ]
        
        self.transacoes = [
            Transacao("Carolina", 250.00, "credito", datetime.now()),
            Transacao("Cassiana", 180.00, "dinheiro", datetime.now()),
            Transacao("Dayana", 320.00, "debito", datetime.now()),
        ]

class BeautyApp(App):
    def build(self):
        self.title = "Bianca Beauty"
        return MainScreen()

if __name__ == '__main__':
    BeautyApp().run()
