# 💈 BarberStyle – Site Institucional para Barbearia Local

> Projeto desenvolvido para a disciplina de **Padrões Web para No Code e Low Code** – UniFECAF  
> Ferramenta principal: **Webflow** | Integração: **Airtable API**

---

## 📌 Visão Geral

O **BarberStyle** é um site institucional criado para uma barbearia local fictícia chamada "Barbearia Estilo Certo", localizada em São Paulo – SP. O objetivo é oferecer presença digital profissional sem custo elevado de desenvolvimento, utilizando a plataforma no-code **Webflow** com customizações manuais em HTML, CSS e JavaScript.

O site permite que clientes:
- Conheçam os serviços e preços da barbearia
- Façam agendamentos via formulário integrado ao **Airtable**
- Visualizem a galeria de cortes realizados
- Entrem em contato pelo WhatsApp diretamente pelo site

---

## 🚀 Como Acessar

| Recurso | Link |
|---|---|
| 🌐 Site publicado (Webflow) | `https://barberstyle-estilo-certo.webflow.io` *(simulado)* |
| 📋 Base de dados (Airtable) | `https://airtable.com/...` *(privado)* |
| 🎬 Vídeo Pitch | `https://loom.com/...` *(link do vídeo)* |

---

## 🗂️ Estrutura do Projeto

```
barberstyle/
│
├── README.md                    ← Este arquivo
├── index.html                   ← Código HTML exportado do Webflow (simulado)
├── custom-styles.css            ← CSS customizado injetado no Webflow
├── custom-scripts.js            ← JavaScript personalizado (interações)
├── airtable_integration.py      ← Script Python para consulta à API do Airtable
├── relatorio_tecnico.pdf        ← Relatório técnico completo (Parte Teórica)
└── assets/
    └── prints/                  ← Capturas de tela da aplicação
```

---

## 🛠️ Tecnologias e Ferramentas

| Camada | Ferramenta |
|---|---|
| Construção visual | Webflow (no-code) |
| Banco de dados / formulários | Airtable |
| Customização de estilo | CSS manual (embed no Webflow) |
| Interatividade | JavaScript vanilla (embed) |
| Integração via API | Airtable REST API (Python) |
| Hospedagem | Webflow Hosting (CDN global) |

---

## ⚙️ Funcionalidades

### 1. Página Principal (Home)
- Hero section com CTA para agendamento
- Seção "Nossos Serviços" com cards responsivos
- Depoimentos de clientes
- Botão flutuante de WhatsApp

### 2. Formulário de Agendamento
- Campos: Nome, Telefone, Serviço desejado, Data/Hora preferida
- Dados enviados automaticamente para o **Airtable**
- Validação de campos com JavaScript
- Feedback visual ao usuário após envio

### 3. Galeria
- Grid responsivo de fotos dos cortes
- Efeito de hover com CSS customizado
- Lazy loading implementado via atributo `loading="lazy"`

### 4. Acessibilidade
- Atributos `alt` em todas as imagens
- Contraste de cores conforme WCAG AA (mínimo 4.5:1)
- Navegação por teclado habilitada
- Uso semântico de tags HTML5 (`<header>`, `<main>`, `<section>`, `<footer>`)

---

## 📦 Como Rodar o Script Python (Integração Airtable)

### Pré-requisitos
```bash
pip install requests python-dotenv
```

### Configuração
Crie um arquivo `.env` na raiz do projeto:
```env
AIRTABLE_API_KEY=sua_chave_aqui
AIRTABLE_BASE_ID=seu_base_id_aqui
AIRTABLE_TABLE_NAME=Agendamentos
```

### Execução
```bash
python airtable_integration.py
```

O script irá:
1. Listar todos os agendamentos cadastrados
2. Exibir nome, serviço e data/hora de cada registro
3. Permitir filtrar agendamentos por data

---

## 📱 Responsividade

O layout foi construído com breakpoints para:
- **Desktop** → ≥ 992px
- **Tablet** → 768px – 991px
- **Mobile** → ≤ 767px

O Webflow aplica as classes de breakpoint automaticamente; os ajustes finos de espaçamento e tipografia foram feitos via CSS customizado injetado no `<head>` do projeto.

---

## ♿ Acessibilidade

Práticas aplicadas:
- `lang="pt-BR"` no elemento `<html>`
- `aria-label` nos botões sem texto visível (ex: botão WhatsApp)
- `role="navigation"` no menu de navegação
- Fontes legíveis (mínimo 16px no corpo do texto)
- Sem uso de cores como único indicador de informação

---

## ⚠️ Limitações Conhecidas

- O plano gratuito do Webflow limita o site a 2 páginas estáticas
- O Airtable API tem limite de 5 requisições/segundo no plano free
- Não é possível adicionar autenticação de usuário sem upgrade de plano
- Animações complexas requerem plano pago do Webflow (Interactions 2.0)

---

## 👨‍💻 Autores

Desenvolvido como parte do trabalho avaliativo da disciplina **Padrões Web para No Code e Low Code** – UniFECAF, 2025.

---

## 📄 Licença

Este projeto é de uso acadêmico. Todos os dados de clientes utilizados são fictícios.
