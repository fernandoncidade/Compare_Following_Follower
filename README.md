<!-- Multilanguage README.md for Compare - Following and Follower -->

<p align="center">
  <b>Selecione o idioma / Select language:</b><br>
  <a href="#ptbr">🇧🇷 Português (BR)</a> |
  <a href="#enus">🇺🇸 English (US)</a>
</p>

---

## <a id="ptbr"></a>🇧🇷 Português (BR)

<details>
<summary>Clique para expandir o README em português</summary>

# Compare - Following and Follower

Versão: 2026.3.1.0
Autor: Fernando Nillsson Cidade

## Resumo
Compare - Following and Follower é um aplicativo desktop para comparar, de forma prática, quem você segue e quem te segue no GitHub.

## Descrição curta
Uma ferramenta para transformar listas grandes de seguidores em decisões claras, sem abrir perfil por perfil.

## Funcionalidades principais
- Consulta seguidores e seguindo via GitHub GraphQL API.
- Exibe resultados em abas objetivas:
  - Seguidores
  - Sigo
  - Não seguidores (você segue, mas não te seguem)
  - Não sigo (te seguem, mas você não segue)
  - Mútuos
  - Não me seguem mais
- Cache local com TTL padrão de 15 minutos para reduzir chamadas desnecessárias.
- Opção de forçar atualização da API (ignora cache).
- Indicadores de origem de dados, rate limit e requisições usadas.
- Importação/exportação em JSON no formato do aplicativo.
- Menu de idioma com alternância entre Português (Brasil) e Inglês (Estados Unidos).

## Novidades e melhorias recentes
- Configuração de token pela interface em **Configurações > Definir token GitHub** (`Ctrl+Shift+T`), com prompt para colar o token.
- Persistência do token no Windows com `setx` em dois escopos:
  - Usuário: `setx GITHUB_TOKEN "seu_token"`
  - Sistema: `setx GITHUB_TOKEN "seu_token" /M` (com elevação/UAC quando necessário)
- Reset completo do token em **Configurações > Resetar Token/Variáveis de Ambiente** (`Ctrl+Shift+R`):
  - remove escopo de usuário, escopo de sistema, sessão atual e chaves de Registro relacionadas;
  - remove arquivos locais de cache/estado;
  - reinicia o aplicativo ao final da operação.
- Exclusão do banco local em **Arquivo > Excluir** (`Ctrl+Shift+D`):
  - lista apenas arquivos que realmente existem;
  - informa quando nenhum arquivo existe;
  - exibe mensagens claras de sucesso/erro.
- Leitura de token mais robusta: quando `GITHUB_TOKEN` não está na sessão, o app tenta ler token persistido no Registro (usuário/sistema) e sincroniza a sessão atual.
- Fluxo automático quando o token está ausente: em operações de atualização/unfollow, o app pode solicitar o token em janela de diálogo e continuar a execução atual com o valor informado.
- Atalhos de menu e idioma refinados, incluindo atalho para submenu de idioma (`Alt+I`).

## Requisitos
- Windows 10 ou superior.
- Python 3.10+ para executar por código-fonte.
- Dependências Python (arquivo `requirements.txt`):
  - requests
  - PySide6 / shiboken6
  - certifi, charset-normalizer, idna, urllib3
- Token do GitHub para consultas autenticadas na API.

## Instalação (código-fonte no Windows)
1. Criar e ativar ambiente virtual:
   - PowerShell:
     - `py -m venv .venv`
     - `.\.venv\Scripts\Activate.ps1`
   - CMD:
     - `py -m venv .venv`
     - `.venv\Scripts\activate`
2. Instalar dependências:
   - `pip install -r requirements.txt`
3. Definir token do GitHub:
   - PowerShell (sessão atual): `$env:GITHUB_TOKEN='seu_token'`
   - PowerShell (persistente - usuário): `setx GITHUB_TOKEN "seu_token"`
   - PowerShell (persistente - sistema): `setx GITHUB_TOKEN "seu_token" /M`
   - Alternativa pela GUI: **Configurações > Definir token GitHub** (`Ctrl+Shift+T`)
4. Executar:
   - GUI: `py main.py`
   - CLI: `py main.py --cli --user seu_usuario`

## Uso rápido
1. Informe seu usuário GitHub.
2. Clique em **Executar** (GUI) ou use `--cli`.
3. Analise as abas de resultado.
4. Opcionalmente exporte/salve os dados para comparações futuras.

## Parâmetros de linha de comando
- `--cli`: executa sem interface gráfica.
- `--user` ou `-u`: define o usuário GitHub alvo.
- `--no-cache`: força atualização da API (ignora cache local).

Exemplos:
- `py main.py --cli --user fernandoncidade`
- `py main.py --cli --user fernandoncidade --no-cache`

## Persistência de dados
Os dados são salvos no diretório persistente do usuário:
- `.github_follow_compare_atual.json`: estado atual (followers, following e resultados calculados).
- `.github_follow_compare_antigo.json`: snapshot anterior usado para detectar mudanças.

Campo de comparação histórica:
- `Não me seguem mais`: perfis que estavam no snapshot anterior e não aparecem mais nos seguidores atuais.

# 1) Como obter o Token no GitHub (Personal Access Token – PAT)

## 📌 Conceito técnico

Um **Personal Access Token (PAT)** é um mecanismo de autenticação baseado em *Bearer Token* que substitui o uso de senha para chamadas à **GitHub REST API** ou **GraphQL API**.

Ele é utilizado via header HTTP:

```http
Authorization: Bearer SEU_TOKEN
```

Sem token:

* Limite: **60 requisições/hora**
* Baseado no IP

Com token:

* Limite: **5.000 requisições/hora**
* Baseado na conta autenticada

---

## 📌 Tipos de Token no GitHub

Atualmente existem dois modelos:

| Tipo                      | Indicado para                     | Observação                          |
| ------------------------- | --------------------------------- | ----------------------------------- |
| **Classic (PAT Classic)** | Scripts simples e testes locais   | Mais direto                         |
| **Fine-grained token**    | Controle granular por repositório | Mais seguro, porém mais burocrático |

Para seu script de followers, use **PAT Classic**.

---

## 📌 Passo-a-passo detalhado (Web Interface)

### 1️⃣ Acesse o GitHub

Entre em:

```
https://github.com
```

---

### 2️⃣ Acesse configurações da conta

* Clique no seu avatar (canto superior direito)
* Clique em **Settings**

---

### 3️⃣ Navegue até as configurações de desenvolvedor

Menu lateral esquerdo:

```
Developer settings
```

---

### 4️⃣ Acesse a área de Tokens

```
Personal access tokens
→ Tokens (classic)
```

---

### 5️⃣ Gere um novo token

Clique em:

```
Generate new token
→ Generate new token (classic)
```

O GitHub pode solicitar confirmação de senha ou 2FA.

---

## 📌 Configuração correta do Token

### 🔹 Note (Descrição)

Coloque algo identificável:

```
followers-following-script
```

Isso é apenas um rótulo interno.

---

### 🔹 Expiration (Validade)

Recomendação técnica:

| Uso                  | Expiração recomendada |
| -------------------- | --------------------- |
| Teste local          | 30 dias               |
| Uso contínuo pessoal | 90 dias               |
| Produção             | Rotação periódica     |

Nunca utilize “No expiration” em ambiente profissional.

---

### 🔹 Scopes (Permissões)

Para seu caso específico:

✔ **Nenhum scope é necessário** para ler seguidores públicos.

Se quiser garantir compatibilidade:

✔ Marque apenas:

```
read:user
```

⚠️ Evite marcar permissões como:

* repo
* admin
* delete
* workflow

Princípio aplicado: **Least Privilege (Princípio do menor privilégio)**

---

### 6️⃣ Gere o Token

Clique em:

```
Generate token
```

---

## ⚠️ Atenção crítica

O GitHub exibirá o token **apenas uma vez**.

Formato típico:

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Se perder, será necessário gerar outro.

---

## 🔐 Boas práticas de segurança

Nunca:

* Colocar token diretamente no código
* Fazer commit do token no Git
* Compartilhar token em prints
* Enviar token por e-mail

Ideal:

* Armazenar como variável de ambiente
* Usar `.env` ignorado pelo `.gitignore` (alternativa)
* Rotacionar periodicamente

---

# 2) Armazenar o Token com Segurança no Windows (Variável de Ambiente)

## 📌 Conceito

Variáveis de ambiente são armazenadas no sistema operacional e podem ser lidas pelo Python via:

```python
os.getenv("GITHUB_TOKEN")
```

Isso evita hardcode no código-fonte.

---

# ✅ Opção A — Variável persistente (Recomendada)

## ✔ Características

* Fica salva no perfil do usuário
* Sobrevive a reinicializações
* Não aparece no código

---

## 🔹 Comando no PowerShell

```powershell
setx GITHUB_TOKEN "COLE_AQUI_SEU_TOKEN"
```

Exemplo real:

```powershell
setx GITHUB_TOKEN "ghp_abc123XYZ..."
```

---

## 🔹 O que acontece internamente?

O Windows grava a variável em:

```
HKEY_CURRENT_USER\Environment
```

Ela será carregada automaticamente em novas sessões.

---

## 🔹 Passo obrigatório

Após usar `setx`:

* Feche o VS Code
* Reabra o VS Code
* Ou feche o terminal e abra novamente

Sem isso, a variável não estará disponível.

---

## 🔹 Teste se funcionou

No novo terminal:

```powershell
$env:GITHUB_TOKEN
```

Se aparecer o token → está correto.

Se retornar vazio → sessão antiga ainda ativa.

---

# ⚠️ Observação importante sobre `setx`

`setx` não altera a sessão atual.

Ele grava para sessões futuras.

Se quiser usar imediatamente na mesma sessão:

```powershell
$env:GITHUB_TOKEN="ghp_abc123XYZ..."
```

---

# ✅ Opção B — Variável temporária (Sessão atual apenas)

```powershell
$env:GITHUB_TOKEN="COLE_AQUI_SEU_TOKEN"
```

## ✔ Características

* Funciona imediatamente
* Some ao fechar o terminal
* Não altera o sistema

---

## 📌 Quando usar?

| Situação                      | Melhor opção |
| ----------------------------- | ------------ |
| Teste rápido                  | Temporária   |
| Projeto contínuo              | Persistente  |
| Ambiente corporativo restrito | Temporária   |

---

# 🔎 Como o Python lê a variável

No seu script:

```python
import os

TOKEN = os.getenv("GITHUB_TOKEN")
```

Se `TOKEN` for `None`, o script roda sem autenticação.

---

# 🧪 Teste técnico completo

No PowerShell:

```powershell
python -c "import os; print(os.getenv('GITHUB_TOKEN'))"
```

Se imprimir o token → integração correta.

---

# 🔐 Segurança avançada (Opcional)

Se quiser elevar o nível:

## ✔ Usar Windows Credential Manager

## ✔ Usar arquivo `.env` + python-dotenv

## ✔ Usar GitHub CLI (`gh auth login`)

## ✔ Rotacionar token automaticamente

Mas para seu cenário local, variável de ambiente é suficiente.

---

# 📌 Resumo Técnico Final

| Item          | Recomendação                     |
| ------------- | -------------------------------- |
| Tipo de Token | PAT Classic                      |
| Expiração     | 30–90 dias                       |
| Scopes        | Nenhum ou apenas `read:user`     |
| Armazenamento | Variável de ambiente persistente |
| Segurança     | Nunca hardcode                   |

---

Se quiser, posso agora explicar:

* 🔎 Como monitorar seu rate limit em tempo real
* 🚀 Como migrar para GraphQL (menos requisições)
* 🖥️ Como integrar isso de forma segura no seu projeto PySide6

## Privacidade e dados
- Dados persistidos localmente no perfil do usuário.
- O aplicativo não envia telemetria própria para terceiros.
- O token do GitHub é usado somente para autenticar consultas e ações necessárias.

## Idiomas suportados
- `pt_BR`: Português (Brasil)
- `en_US`: English (United States)

## Suporte e contato
- Autor: Fernando Nillsson Cidade
- E-mail: linceu_lighthouse@outlook.com
- Relato de problemas: abra uma issue no repositório e, se possível, anexe logs.

## Licença e avisos
Consulte os arquivos de licença, avisos legais, EULA e política de privacidade na pasta `source/assets`.

---

</details>

## <a id="enus"></a>🇺🇸 English (US)

<details>
<summary>Click to expand the README in English</summary>

# Compare - Following and Follower

Version: 2026.3.1.0
Author: Fernando Nillsson Cidade

## Summary
Compare - Following and Follower is a desktop app to compare, in a practical way, who you follow and who follows you on GitHub.

## Short description
A tool to turn large follower lists into clear decisions without opening profile by profile.

## Key features
- Fetches followers and following through the GitHub GraphQL API.
- Displays results in objective tabs:
  - Followers
  - Following
  - Non-followers (you follow them, they do not follow you back)
  - I do not follow (they follow you, you do not follow them)
  - Mutuals
  - No longer follow me
- Local cache with a default TTL of 15 minutes to reduce unnecessary requests.
- Option to force API refresh (ignores cache).
- Data source, rate limit, and request usage indicators.
- JSON import/export using the app data format.
- Language menu with Portuguese (Brazil) and English (United States).

## Recent updates and improvements
- Token setup via UI in **Settings > Set GitHub token** (`Ctrl+Shift+T`), with a dialog to paste the token.
- Windows token persistence using `setx` in both scopes:
  - User: `setx GITHUB_TOKEN "your_token"`
  - System: `setx GITHUB_TOKEN "your_token" /M` (with UAC elevation when required)
- Full token reset in **Settings > Reset Token/Environment Variables** (`Ctrl+Shift+R`):
  - removes user scope, system scope, current session value, and related Registry entries;
  - removes local cache/state files;
  - restarts the application after the operation.
- Local database deletion in **File > Delete** (`Ctrl+Shift+D`):
  - lists only files that actually exist;
  - informs when no database files exist;
  - shows clear success/error feedback.
- More robust token loading: when `GITHUB_TOKEN` is missing from the current session, the app attempts to read persisted token values from Registry (user/system) and syncs the current process environment.
- Automatic missing-token flow: during refresh/unfollow operations, the app can request the token via dialog and continue the current run using the informed value.
- Refined menu/language shortcuts, including the language submenu shortcut (`Alt+I`).

## Requirements
- Windows 10 or later.
- Python 3.10+ to run from source.
- Python dependencies (`requirements.txt`):
  - requests
  - PySide6 / shiboken6
  - certifi, charset-normalizer, idna, urllib3
- GitHub token for authenticated API queries.

## Installation (from source on Windows)
1. Create and activate a virtual environment:
   - PowerShell:
     - `py -m venv .venv`
     - `.\.venv\Scripts\Activate.ps1`
   - CMD:
     - `py -m venv .venv`
     - `.venv\Scripts\activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Set GitHub token:
   - PowerShell (current session): `$env:GITHUB_TOKEN='your_token'`
   - PowerShell (persistent - user): `setx GITHUB_TOKEN "your_token"`
   - PowerShell (persistent - system): `setx GITHUB_TOKEN "your_token" /M`
   - GUI alternative: **Settings > Set GitHub token** (`Ctrl+Shift+T`)
4. Run:
   - GUI: `py main.py`
   - CLI: `py main.py --cli --user your_username`

## Quick use
1. Enter your GitHub username.
2. Click **Run** (GUI) or use `--cli`.
3. Review the result tabs.
4. Optionally export/save data for future comparisons.

## Command-line arguments
- `--cli`: run without the graphical interface.
- `--user` or `-u`: set target GitHub username.
- `--no-cache`: force API refresh (ignore local cache).

Examples:
- `py main.py --cli --user fernandoncidade`
- `py main.py --cli --user fernandoncidade --no-cache`

## Data persistence
Data is saved in the user persistent directory:
- `.github_follow_compare_atual.json`: current snapshot (followers, following, and calculated outputs).
- `.github_follow_compare_antigo.json`: previous snapshot used to detect changes.

Historical comparison field:
- `No longer follow me`: users present in the previous snapshot that are absent from current followers.

# 1) How to Get a GitHub Token (Personal Access Token - PAT)

## 📌 Technical Concept

A **Personal Access Token (PAT)** is an authentication mechanism based on a *Bearer Token* that replaces password usage for calls to the **GitHub REST API** or **GraphQL API**.

It is sent through the HTTP header:

```http
Authorization: Bearer YOUR_TOKEN
```

Without token:

* Limit: **60 requests/hour**
* IP-based

With token:

* Limit: **5,000 requests/hour**
* Based on the authenticated account

---

## 📌 GitHub Token Types

There are currently two models:

| Type                      | Recommended for                    | Notes                                |
| ------------------------- | ---------------------------------- | ------------------------------------ |
| **Classic (PAT Classic)** | Simple scripts and local tests     | More straightforward                 |
| **Fine-grained token**    | Granular repository-level controls | More secure, but more bureaucratic   |

For your followers script, use **PAT Classic**.

---

## 📌 Detailed Step-by-Step (Web Interface)

### 1️⃣ Open GitHub

Go to:

```
https://github.com
```

---

### 2️⃣ Open account settings

* Click your avatar (top-right corner)
* Click **Settings**

---

### 3️⃣ Navigate to developer settings

Left sidebar menu:

```
Developer settings
```

---

### 4️⃣ Open the Tokens area

```
Personal access tokens
→ Tokens (classic)
```

---

### 5️⃣ Generate a new token

Click:

```
Generate new token
→ Generate new token (classic)
```

GitHub may ask for password confirmation or 2FA.

---

## 📌 Correct Token Configuration

### 🔹 Note (Description)

Use something identifiable:

```
followers-following-script
```

This is only an internal label.

---

### 🔹 Expiration (Validity)

Technical recommendation:

| Use case                | Recommended expiration |
| ----------------------- | ---------------------- |
| Local testing           | 30 days                |
| Ongoing personal use    | 90 days                |
| Production              | Periodic rotation      |

Never use "No expiration" in a professional environment.

---

### 🔹 Scopes (Permissions)

For your specific case:

✔ **No scope is required** to read public followers.

If you want compatibility:

✔ Check only:

```
read:user
```

⚠️ Avoid permissions such as:

* repo
* admin
* delete
* workflow

Applied principle: **Least Privilege**

---

### 6️⃣ Generate the Token

Click:

```
Generate token
```

---

## ⚠️ Critical Warning

GitHub will display the token **only once**.

Typical format:

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

If you lose it, you must generate a new one.

---

## 🔐 Security Best Practices

Never:

* Put the token directly in the code
* Commit the token to Git
* Share the token in screenshots
* Send the token by email

Ideal:

* Store it as an environment variable
* Use a `.env` file ignored by `.gitignore` (alternative)
* Rotate it periodically

---

# 2) Store the Token Securely on Windows (Environment Variable)

## 📌 Concept

Environment variables are stored in the operating system and can be read by Python via:

```python
os.getenv("GITHUB_TOKEN")
```

This avoids hardcoding in source code.

---

# ✅ Option A - Persistent variable (Recommended)

## ✔ Characteristics

* Saved in the user profile
* Survives system restarts
* Does not appear in code

---

## 🔹 PowerShell command

```powershell
setx GITHUB_TOKEN "PASTE_YOUR_TOKEN_HERE"
```

Real example:

```powershell
setx GITHUB_TOKEN "ghp_abc123XYZ..."
```

---

## 🔹 What happens internally?

Windows stores the variable at:

```
HKEY_CURRENT_USER\Environment
```

It is automatically loaded in new sessions.

---

## 🔹 Mandatory step

After using `setx`:

* Close VS Code
* Reopen VS Code
* Or close the terminal and open it again

Without this, the variable will not be available.

---

## 🔹 Verify it worked

In a new terminal:

```powershell
$env:GITHUB_TOKEN
```

If the token appears -> it is correct.

If it returns empty -> an old session is still active.

---

# ⚠️ Important note about `setx`

`setx` does not change the current session.

It writes for future sessions.

If you want to use it immediately in the same session:

```powershell
$env:GITHUB_TOKEN="ghp_abc123XYZ..."
```

---

# ✅ Option B - Temporary variable (Current session only)

```powershell
$env:GITHUB_TOKEN="PASTE_YOUR_TOKEN_HERE"
```

## ✔ Characteristics

* Works immediately
* Disappears when terminal closes
* Does not change the system

---

## 📌 When should you use each option?

| Scenario                      | Best option |
| ----------------------------- | ----------- |
| Quick test                    | Temporary   |
| Ongoing project               | Persistent  |
| Restricted corporate setup    | Temporary   |

---

# 🔎 How Python reads the variable

In your script:

```python
import os

TOKEN = os.getenv("GITHUB_TOKEN")
```

If `TOKEN` is `None`, the script runs without authentication.

---

# 🧪 Full technical test

In PowerShell:

```powershell
python -c "import os; print(os.getenv('GITHUB_TOKEN'))"
```

If it prints the token -> integration is correct.

---

# 🔐 Advanced security (Optional)

If you want to raise the security level:

## ✔ Use Windows Credential Manager

## ✔ Use a `.env` file + python-dotenv

## ✔ Use GitHub CLI (`gh auth login`)

## ✔ Rotate token automatically

But for your local scenario, an environment variable is enough.

---

# 📌 Final Technical Summary

| Item          | Recommendation                    |
| ------------- | --------------------------------- |
| Token type    | PAT Classic                       |
| Expiration    | 30-90 days                        |
| Scopes        | None or only `read:user`          |
| Storage       | Persistent environment variable   |
| Security      | Never hardcode                    |

---

If you want, I can now explain:

* 🔎 How to monitor your rate limit in real time
* 🚀 How to migrate to GraphQL (fewer requests)
* 🖥️ How to integrate this securely into your PySide6 project

## Privacy and data
- Data is stored locally in the user profile.
- The app does not send its own telemetry to third parties.
- The GitHub token is used only to authenticate required queries/actions.

## Supported languages
- `pt_BR`: Portuguese (Brazil)
- `en_US`: English (United States)

## Support and contact
- Author: Fernando Nillsson Cidade
- E-mail: linceu_lighthouse@outlook.com
- Report issues: open a repository issue and include logs when possible.

## License and notices
Check license files, legal notices, EULA, and privacy policy under `source/assets`.

---

</details>
