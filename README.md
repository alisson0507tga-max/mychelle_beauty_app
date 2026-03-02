# Mychelle Beauty - Aplicativo de Gestão para Salão de Beleza

Um aplicativo profissional desenvolvido em **Kivy** para gerenciar agendamentos, clientes, serviços e finanças de um salão de beleza.

## Características Principais

### 📅 Agenda
- Visualizar agendamentos do dia
- Criar novos agendamentos
- Confirmar ou cancelar agendamentos
- Enviar lembretes via WhatsApp

### 👥 Clientes
- Cadastro completo de clientes
- Busca rápida por nome
- Histórico de atendimentos
- Visualizar total gasto
- Notificações de aniversário
- Enviar mensagens via WhatsApp

### 💰 Financeiro
- Dashboard com receita, despesas e lucro
- Controle por forma de pagamento (dinheiro, crédito, débito)
- Histórico de transações
- Registrar novas transações

### 📊 Relatórios
- Total de clientes
- Receita do mês
- Melhor cliente
- Serviços mais vendidos
- Estatísticas gerais

### ✂️ Serviços
- Cadastro de serviços
- Preço e duração
- Listagem completa

## Design e Interface

O aplicativo possui:
- **Design moderno** com cores vibrantes (roxo, verde, azul, laranja)
- **Cards coloridos** para melhor visualização de dados
- **Interface responsiva** adaptada para mobile
- **Abas de navegação** intuitivas
- **Botões de ação rápida** em todas as telas

## Tecnologias Utilizadas

- **Python 3.11+**
- **Kivy 2.1.0** - Framework para interface gráfica
- **Buildozer** - Ferramenta para compilar APK
- **Cython** - Para otimização de performance

## Requisitos para Compilar

### No Linux/Mac:
```bash
# Instalar dependências
sudo apt-get install openjdk-11-jdk  # Linux
brew install openjdk@11              # Mac

# Instalar Python packages
pip3 install kivy buildozer cython

# Instalar dependências do Buildozer
pip3 install python-for-android
```

### No Windows:
- Instalar Java JDK 11+
- Instalar Python 3.11+
- Instalar as dependências via pip

## Como Compilar o APK

### Passo 1: Preparar o Ambiente

```bash
# Navegar para o diretório do projeto
cd mychelle_beauty_app

# Inicializar buildozer (se ainda não feito)
buildozer init
```

### Passo 2: Configurar buildozer.spec

O arquivo `buildozer.spec` já está configurado com:
- Nome do app: Mychelle Beauty
- Package name: mychellebeauty
- Package domain: com.mychelle.beauty
- Versão: 0.1

### Passo 3: Compilar o APK

```bash
# Compilar para Android (debug)
buildozer android debug

# Ou compilar para Android (release)
buildozer android release
```

O processo pode levar de 15 a 45 minutos dependendo da velocidade do computador.

### Passo 4: Localizar o APK

Após a compilação bem-sucedida, o APK estará em:
```
bin/mychellebeauty-0.1-debug.apk  # Para debug
bin/mychellebeauty-0.1-release.apk # Para release
```

## Instalação no Dispositivo

### Via ADB (Android Debug Bridge):
```bash
adb install bin/mychellebeauty-0.1-debug.apk
```

### Via Arquivo:
1. Copie o arquivo `.apk` para seu dispositivo Android
2. Abra o gerenciador de arquivos
3. Localize e toque no arquivo `.apk`
4. Siga as instruções de instalação

## Estrutura do Projeto

```
mychelle_beauty_app/
├── main.py                 # Código principal do aplicativo
├── buildozer.spec         # Configuração do Buildozer
├── dados_app.json         # Arquivo de dados (criado automaticamente)
├── app_reference.md       # Referência do app Minha Agenda
└── README.md              # Este arquivo
```

## Funcionalidades de Dados

O aplicativo armazena dados em `dados_app.json` com:
- **Clientes**: Nome, telefone, aniversário, email, histórico
- **Agendamentos**: Cliente, serviço, data, hora, status
- **Serviços**: Nome, preço, duração
- **Transações**: Cliente, valor, tipo, data

## Integração com WhatsApp

O aplicativo está preparado para integração com WhatsApp via Intent do Android. Para usar:

1. Certifique-se de que o WhatsApp está instalado no dispositivo
2. Clique no botão "WhatsApp" em qualquer cliente ou agendamento
3. A mensagem será enviada automaticamente

## Próximas Melhorias

- [ ] Ícone personalizado para o app
- [ ] Gráficos interativos com matplotlib
- [ ] Notificações push para aniversários
- [ ] Backup na nuvem (Google Drive, Firebase)
- [ ] Sistema de fidelidade com cartões de desconto
- [ ] Integração real com WhatsApp API
- [ ] Modo escuro
- [ ] Suporte a múltiplos idiomas

## Solução de Problemas

### Erro: "Java compiler (javac) not found"
```bash
# Instale o JDK
sudo apt-get install openjdk-11-jdk  # Linux
brew install openjdk@11              # Mac
```

### Erro: "Android SDK not found"
O Buildozer baixará automaticamente o SDK na primeira execução. Certifique-se de ter espaço em disco (>10GB).

### Build muito lento
- Isso é normal na primeira compilação
- Compilações subsequentes serão mais rápidas
- Use `buildozer android debug` para debug (mais rápido)

### APK não instala
- Verifique se o dispositivo permite instalação de apps desconhecidos
- Tente desinstalar versões anteriores primeiro
- Verifique se o arquivo `.apk` não está corrompido

## Contato e Suporte

Para dúvidas ou sugestões sobre o desenvolvimento do app, entre em contato com o desenvolvedor.

## Licença

Este projeto é fornecido como está para uso pessoal e comercial.

---

**Versão**: 0.1  
**Última atualização**: Março 2026  
**Desenvolvido com**: Kivy + Python
# Teste para rodar workflow
# Teste workflow
