# Keylogger Miniprojeto – Criptografia e Segurança

**Autores**: Paulo Vinícius & André Nicolas  
**Disciplina**: Criptografia e Segurança nas Comunicações  
**Instituição**: Escola Superior de Tecnologia e Gestão, IPVC (Portugal)

---

## 🔎 Descrição

Este é um **keylogger completo para Windows**, desenvolvido como um miniprojeto académico.
Registra teclado, mouse e janelas ativadas, além de gerar persistência, criptografar os logs com PGP e enviar remotamente via HTTP POST.

---

## ⚠️ Aviso Legal

Uso **exclusivamente educativo**.
O uso não consentido é ilegal em muitos países.
Proteja a privacidade e cumpra com a legislação local.

---

## ✅ Pré-requisitos

- Windows (7+)

---

## 📁 Estrutura do Projeto

```
.
├── keylogger.py   # Script principal python
├── post.php       # Receptor de dados no servidor
└── README.MD      # Esse arquivo
```

---

## 🛠 Funcionalidades (keylogger.py)

- **Persistência**
  - `copiar_para_caminho()`: copia o executável para um diretório oculto.
  - `adicionar_persistencia()`: cria tarefa agendada para iniciamento automático e adiciona o arquivo nos programas de inicialização.

- **Identificação do sistema**
  - `pegar_uuid()`: obtém UUID via `wmic` ou `Get-ItemProperty`.
  - `pegar_dados_do_sistema()`: recolhe info de SO, hardware, antivírus, etc.

- **Captura de eventos**
  - `thread_teclado()`: regista todas as teclas.
  - `thread_mouse()`: regista cliques e posição.
  - `thread_janelas()`: regista alteração de janela ativa.

- **Logs e envio**
  - `salvar_em_cache()`: armazena logs em cache.
  - `encriptar_log(dados)`: criptografa usando PGP.
  - `thread_encriptar_e_enviar()`: encripta + envia logs via HTTP POST.
  - `enviar_post()`: envia os dados para o servidor remoto.

- **Interface**
  - `janela_aviso()`: exibe aviso de que o keylogger está em execução.

---

## 🌐 Receptor (post.php)

- Recebe dados POST.
- Grava as informações recebidas no banco de dados.

---

## 🛡 Segurança e Criptografia

- Todos os dados são encriptados com uma chave pública **PGP** de 4096 bytes, criada especificamente para o projeto.
- URL do servidor está ofuscada (Base64).
- Logs incluem `UUID`, timestamp e eventos.

---

## 🤝 Contribuições

Este projeto é **fechado** para fins acadêmicos. Mas pode ser estendido com:

- Suporte a múltiplos formatos de criptografia
- Envio via email/FTP
- Interface gráfica opcional

---

## 📜 Licença & Ética

Uso exclusivo para esta disciplina.
Qualquer utilização fora do contexto **é da responsabilidade do utilizador**.

---

## 👤 Autores

- Paulo Vinícius Kuss 
- André Nicolas Silva Alves

---

## 📞 Contacto

- Email Paulo: [pviniks@gmail.com](pviniks@gmail.com)
- GitHub Paulo: [PViniKs](https://github.com/PViniKs)
- LinkedIn Paulo: [/in/paulovkuss](https://www.linkedin.com/in/paulovkuss/)

- Email André: [xby75010@gmail.com](xby75010@gmail.com)
- GitHub André: [Nickolas-007](https://github.com/Nickolas-007)
- LinkedIn André: [/in/andre-nicolas-silva-alves](https://www.linkedin.com/in/andre-nicolas-silva-alves-46872b215/)
