from dataclasses import dataclass


@dataclass(frozen=True)
class ManualDetails:
    summary: str
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()


@dataclass(frozen=True)
class ManualSection:
    id: str
    title: str
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()
    details: tuple[ManualDetails, ...] = ()


def normalize_language(lang: str | None) -> str:
    if not lang:
        return "pt_BR"

    v = lang.strip().replace("-", "_").lower()
    if v in ("pt_br", "pt"):
        return "pt_BR"

    if v in ("en_us", "en"):
        return "en_US"

    return "pt_BR"


def get_manual_document(lang: str | None = None) -> tuple[ManualSection, ...]:
    lang = normalize_language(lang)
    if lang == "en_US":
        try:
            from . import DOC_EN_US
            return getattr(DOC_EN_US, "_DOC_EN_US", tuple())
        except Exception:
            return tuple()

    return _DOC_PT_BR


_DOC_PT_BR: tuple[ManualSection, ...] = (
    ManualSection(
        id="visao-geral",
        title="Visão geral",
        paragraphs=(
            "Compare - Following and Follower é um aplicativo para analisar o relacionamento entre quem você segue e quem te segue no GitHub.",
            "Ele organiza os resultados em abas objetivas, mostra contagens resumidas, exibe status de cache/rate limit e permite ações rápidas como exportar/importar dados e executar unfollow assistido.",
        ),
    ),
    ManualSection(
        id="para-que-serve",
        title="Para que serve",
        bullets=(
            "Identificar perfis que você segue, mas não te seguem de volta.",
            "Identificar quem te segue e você ainda não segue.",
            "Verificar seguidores mútuos.",
            "Detectar quem deixou de te seguir entre duas execuções.",
            "Acompanhar mudanças sem precisar abrir perfil por perfil.",
        ),
    ),
    ManualSection(
        id="requisitos",
        title="Requisitos",
        bullets=(
            "Windows 10+ (foco principal da interface).",
            "Python 3.10+ para execução por código-fonte.",
            "Dependências instaladas via requirements.txt (inclui PySide6 e requests).",
            "Internet para consultar a GitHub GraphQL API.",
            "Token do GitHub em GITHUB_TOKEN para atualização via API (quando não houver cache válido).",
        ),
    ),
    ManualSection(
        id="configuracao-token",
        title="Configuração do token (GITHUB_TOKEN)",
        paragraphs=(
            "Sem token, o aplicativo só consegue operar com dados já existentes em cache local dentro do TTL.",
            "Para forçar atualização da API ou carregar dados sem cache, defina GITHUB_TOKEN no ambiente.",
        ),
        bullets=(
            "PowerShell (sessão atual): $env:GITHUB_TOKEN='seu_token'",
            "PowerShell (persistente - usuário): setx GITHUB_TOKEN \"seu_token\"",
            "PowerShell (persistente - sistema): setx GITHUB_TOKEN \"seu_token\" /M",
            "Após usar setx, abra um novo terminal/VS Code para a variável ser carregada.",
        ),
    ),
    ManualSection(
        id="token-pela-interface",
        title="Definir token pela interface (recomendado)",
        bullets=(
            "Abra Configurações > Definir token GitHub (Ctrl+Shift+T).",
            "Cole o token e confirme em OK.",
            "No Windows, o aplicativo tenta gravar o token em Variáveis de Usuário e Variáveis de Sistema.",
            "A gravação em Variáveis de Sistema pode solicitar confirmação de administrador (UAC).",
            "Se apenas uma parte da gravação funcionar, o app informa os detalhes e continua a execução atual com o token informado.",
        ),
    ),
    ManualSection(
        id="reset-token-variaveis",
        title="Resetar token e variáveis de ambiente",
        bullets=(
            "Abra Configurações > Resetar Token/Variáveis de Ambiente (Ctrl+Shift+R).",
            "O app solicita confirmação e mostra os arquivos locais que também serão removidos.",
            "A ação remove token de usuário, token de sistema, sessão atual e chaves de Registro relacionadas.",
            "Também remove os arquivos locais .github_follow_compare_antigo.json e .github_follow_compare_atual.json.",
            "Ao final, o aplicativo reinicia automaticamente para aplicar as mudanças.",
        ),
    ),
    ManualSection(
        id="como-executar",
        title="Como executar",
        bullets=(
            "GUI: py main.py",
            "CLI: py main.py --cli --user seu_usuario",
            "CLI forçando API: py main.py --cli --user seu_usuario --no-cache",
            "Parâmetros disponíveis: --cli, --user (-u), --no-cache",
        ),
    ),
    ManualSection(
        id="fluxo-gui",
        title="Fluxo principal na interface",
        bullets=(
            "Informe o usuário GitHub no campo \"Usuário GitHub\".",
            "Clique em \"▶️ Executar\" para carregar/atualizar dados.",
            "Se o token estiver ausente e não houver cache utilizável, o app pode solicitar o token em janela de diálogo.",
            "Leia o resumo de contagens no topo.",
            "Navegue pelas abas para analisar os perfis por categoria.",
            "Use a opção \"Forçar atualização da API (ignorar cache por 15 min)\" quando quiser dados de rede imediatos.",
        ),
    ),
    ManualSection(
        id="abas-e-resumo",
        title="Abas e resumo de contagens",
        paragraphs=(
            "O cabeçalho principal usa o formato: Seguidores = xx; Sigo = xx; Não sigo = xx; Mútuos = xx; Não me seguem mais = xx.",
            "Cada aba também mostra sua contagem no título.",
        ),
        details=(
            ManualDetails(
                summary="🔵 Seguidores",
                bullets=("Mostra todos os logins que seguem o usuário informado.",),
            ),
            ManualDetails(
                summary="🟣 Sigo",
                bullets=("Mostra todos os logins que o usuário informado segue.",),
            ),
            ManualDetails(
                summary="🟢 Mútuos",
                bullets=("Interseção entre \"Seguidores\" e \"Sigo\".",),
            ),
            ManualDetails(
                summary="🔴 Não seguidores",
                bullets=("Perfis que você segue, mas que não te seguem de volta.",),
            ),
            ManualDetails(
                summary="🟡 Não sigo",
                bullets=("Perfis que te seguem, mas que você não segue.",),
            ),
            ManualDetails(
                summary="🟠 Não me seguem mais",
                bullets=(
                    "Diferença entre seguidores antigos e atuais.",
                    "Itens dessa aba podem ser marcados para unfollow assistido.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="calculos",
        title="Como os cálculos são feitos",
        bullets=(
            "Não seguidores = seguindo - seguidores.",
            "Não sigo = seguidores - seguindo.",
            "Mútuos = seguidores ∩ seguindo.",
            "Não me seguem mais = seguidores_antigos - seguidores_atuais.",
            "Todos os logins são normalizados (trim + lowercase) antes de comparar.",
        ),
    ),
    ManualSection(
        id="cache-e-atualizacao",
        title="Cache, atualização e rate limit",
        bullets=(
            "O cache local padrão tem TTL de 900 segundos (15 minutos).",
            "Se existir cache válido e a opção de forçar atualização estiver desmarcada, o app lê do cache.",
            "Com \"Forçar atualização da API\", o app ignora cache no ciclo atual.",
            "A opção de forçar atualização é mais lenta e consome rate limit da API.",
            "A interface exibe origem dos dados, rate limit restante e requisições da atualização.",
        ),
    ),
    ManualSection(
        id="menu-arquivo",
        title="Menu Arquivo e atalhos",
        bullets=(
            "Novo (Ctrl+N): limpa interface e reseta arquivos locais de cache/estado.",
            "Abrir (Ctrl+O): importa JSON de cache, estado ou pacote combinado.",
            "Salvar (Ctrl+S): exporta um pacote JSON com \"atual\" e \"antigo\".",
            "Excluir (Ctrl+Shift+D): mostra os arquivos de banco existentes e pede confirmação para excluir.",
            "Se não existir nenhum arquivo de banco local, o aplicativo informa isso na janela de diálogo.",
            "Ajuda (F1): mostra atalhos disponíveis.",
            "Fechar (Ctrl+Q): fecha a aplicação.",
        ),
    ),
    ManualSection(
        id="menu-configuracoes-opcoes",
        title="Menu Configurações, Idioma e Opções",
        bullets=(
            "Definir token GitHub (Ctrl+Shift+T): abre diálogo para colar token e salvar no ambiente.",
            "Resetar Token/Variáveis de Ambiente (Ctrl+Shift+R): remove token, arquivos locais e reinicia o app.",
            "Idioma (Alt+I): submenu em Configurações para alternar pt_BR/en_US em tempo real.",
            "Manual (Ctrl+Shift+M) e Sobre (Ctrl+Shift+A) ficam no menu Opções.",
        ),
    ),
    ManualSection(
        id="unfollow-assistido",
        title="Unfollow assistido",
        bullets=(
            "A aba \"Não me seguem mais\" permite marcar perfis com checkbox.",
            "O botão \"🗑️ Unfollow\" habilita apenas quando há itens marcados.",
            "Antes de executar, o app pede confirmação.",
            "Ao concluir, exibe resumo de sucesso/falha e pode atualizar os dados automaticamente.",
        ),
    ),
    ManualSection(
        id="arquivos-persistentes",
        title="Arquivos persistentes",
        bullets=(
            ".github_follow_compare_atual.json: snapshot atual com followers/following e resultados calculados.",
            ".github_follow_compare_antigo.json: snapshot anterior para histórico de mudanças.",
            "Esses arquivos podem ser removidos por Arquivo > Excluir ou durante o reset de token em Configurações.",
            "Os caminhos podem ser customizados por variável de ambiente:",
            "FOLLOW_COMPARE_CACHE_FILE (arquivo atual) e FOLLOW_COMPARE_STATE_FILE (arquivo antigo).",
            "O diretório base persistente vem de source.utils.obter_caminho_persistente().",
        ),
    ),
    ManualSection(
        id="modo-cli",
        title="Modo CLI (uso rápido)",
        bullets=(
            "Execute: py main.py --cli --user seu_usuario",
            "A saída mostra resumo, origem (cache/graphql), rate limit e listas por categoria.",
            "Para ignorar cache no CLI: adicione --no-cache.",
        ),
    ),
    ManualSection(
        id="solucao-problemas",
        title="Solução de problemas",
        details=(
            ManualDetails(
                summary="Erro de token ausente",
                bullets=(
                    "Mensagem típica: Defina GITHUB_TOKEN para usar GraphQL sem cache.",
                    "Defina a variável de ambiente e execute novamente.",
                    "Você também pode usar Configurações > Definir token GitHub para configurar pelo próprio aplicativo.",
                ),
            ),
            ManualDetails(
                summary="Token salvo parcialmente (Windows)",
                bullets=(
                    "Pode ocorrer quando o escopo de usuário salva, mas o escopo de sistema exige permissão de administrador.",
                    "Confirme o prompt UAC quando solicitado ou execute o app/terminal com privilégios administrativos.",
                    "Mesmo com salvamento parcial, a execução atual pode continuar usando o token informado.",
                ),
            ),
            ManualDetails(
                summary="Contagens inesperadas",
                bullets=(
                    "Forçe atualização da API para evitar leitura de cache antigo.",
                    "Confira se o usuário informado está correto.",
                ),
            ),
            ManualDetails(
                summary="Falha ao abrir/salvar JSON",
                bullets=(
                    "Verifique permissões de escrita na pasta alvo.",
                    "Confirme se o arquivo segue o formato esperado (cache/estado/pacote).",
                ),
            ),
            ManualDetails(
                summary="Excluir banco local não removeu tudo",
                bullets=(
                    "O menu Excluir remove os arquivos que existem no momento da confirmação.",
                    "Se não houver arquivos, a janela informa que não há banco local para excluir.",
                    "Se apenas um arquivo existir, apenas ele será listado/removido.",
                ),
            ),
            ManualDetails(
                summary="Rate limit indisponível ou baixo",
                bullets=(
                    "Aguarde reset da janela de rate limit da API.",
                    "Evite uso contínuo com atualização forçada.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="privacidade-suporte",
        title="Privacidade e suporte",
        bullets=(
            "Os dados ficam armazenados localmente no perfil do usuário.",
            "O aplicativo não envia telemetria própria para terceiros.",
            "O token é usado apenas para autenticar consultas/ações necessárias.",
            "Contato: linceu_lighthouse@outlook.com",
        ),
    ),
)


__all__ = ["_DOC_PT_BR"]
