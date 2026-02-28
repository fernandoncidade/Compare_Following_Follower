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
        return "en_US"

    v = lang.strip().replace("-", "_").lower()
    if v in ("en_us", "en"):
        return "en_US"

    if v in ("pt_br", "pt"):
        return "pt_BR"

    return "en_US"


def get_manual_document(lang: str | None = None) -> tuple[ManualSection, ...]:
    lang = normalize_language(lang)
    if lang == "pt_BR":
        try:
            from . import DOC_PT_BR
            return getattr(DOC_PT_BR, "_DOC_PT_BR", tuple())
        except Exception:
            return tuple()

    return _DOC_EN_US


_DOC_EN_US: tuple[ManualSection, ...] = (
    ManualSection(
        id="overview",
        title="Overview",
        paragraphs=(
            "Compare - Following and Follower is an app to analyze the relationship between who you follow and who follows you on GitHub.",
            "It organizes results into objective tabs, shows summary counters, displays cache/rate-limit status, and provides quick actions such as JSON import/export and assisted unfollow.",
        ),
    ),
    ManualSection(
        id="purpose",
        title="What it is for",
        bullets=(
            "Find accounts you follow that do not follow you back.",
            "Find accounts that follow you but you do not follow.",
            "View mutual followers.",
            "Detect who stopped following you between runs.",
            "Track relationship changes without opening profiles one by one.",
        ),
    ),
    ManualSection(
        id="requirements",
        title="Requirements",
        bullets=(
            "Windows 10+ (main UI target).",
            "Python 3.10+ for source execution.",
            "Dependencies installed from requirements.txt (including PySide6 and requests).",
            "Internet access to query the GitHub GraphQL API.",
            "GitHub token in GITHUB_TOKEN for API refresh when there is no valid cache.",
        ),
    ),
    ManualSection(
        id="token-setup",
        title="Token setup (GITHUB_TOKEN)",
        paragraphs=(
            "Without a token, the app can only work with local cached data within TTL.",
            "To force API refresh or fetch data when cache is unavailable, set GITHUB_TOKEN.",
        ),
        bullets=(
            "PowerShell (current session): $env:GITHUB_TOKEN='your_token'",
            "PowerShell (persistent): setx GITHUB_TOKEN \"your_token\"",
            "After setx, open a new terminal/VS Code session so the variable is loaded.",
        ),
    ),
    ManualSection(
        id="how-to-run",
        title="How to run",
        bullets=(
            "GUI: py main.py",
            "CLI: py main.py --cli --user your_username",
            "CLI forcing API refresh: py main.py --cli --user your_username --no-cache",
            "Available arguments: --cli, --user (-u), --no-cache",
        ),
    ),
    ManualSection(
        id="gui-flow",
        title="Main GUI workflow",
        bullets=(
            "Enter the target account in the \"GitHub User\" field.",
            "Click \"▶️ Run\" to load/refresh data.",
            "Read the summary counters at the top.",
            "Inspect each tab to analyze profiles by category.",
            "Use \"Force API refresh (ignore cache for 15 min)\" when you need immediate network data.",
        ),
    ),
    ManualSection(
        id="tabs-and-summary",
        title="Tabs and summary counters",
        paragraphs=(
            "The main header follows: Followers = xx; Following = xx; I do not follow = xx; Mutuals = xx; No longer follow me = xx.",
            "Each tab title also shows its own count.",
        ),
        details=(
            ManualDetails(
                summary="🔵 Followers",
                bullets=("Shows all logins that follow the selected user.",),
            ),
            ManualDetails(
                summary="🟣 Following",
                bullets=("Shows all logins the selected user follows.",),
            ),
            ManualDetails(
                summary="🟢 Mutuals",
                bullets=("Intersection between \"Followers\" and \"Following\".",),
            ),
            ManualDetails(
                summary="🔴 Non-followers",
                bullets=("Accounts you follow that do not follow you back.",),
            ),
            ManualDetails(
                summary="🟡 I do not follow",
                bullets=("Accounts that follow you but you do not follow.",),
            ),
            ManualDetails(
                summary="🟠 No longer follow me",
                bullets=(
                    "Difference between previous and current followers.",
                    "Items in this tab can be checked for assisted unfollow.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="calculations",
        title="How calculations are performed",
        bullets=(
            "Non-followers = following - followers.",
            "I do not follow = followers - following.",
            "Mutuals = followers ∩ following.",
            "No longer follow me = previous_followers - current_followers.",
            "All logins are normalized (trim + lowercase) before comparison.",
        ),
    ),
    ManualSection(
        id="cache-refresh-rate-limit",
        title="Cache, refresh, and rate limit",
        bullets=(
            "Default local cache TTL is 900 seconds (15 minutes).",
            "If cache is valid and force refresh is unchecked, data is loaded from cache.",
            "With force refresh enabled, cache is ignored for the current run.",
            "Force refresh is slower and consumes API rate limit.",
            "The UI shows data source, remaining rate limit, and request usage for the refresh.",
        ),
    ),
    ManualSection(
        id="file-menu",
        title="File menu and shortcuts",
        bullets=(
            "New (Ctrl+N): clears UI data and resets local cache/state files.",
            "Open (Ctrl+O): imports JSON in cache, state, or combined bundle format.",
            "Save (Ctrl+S): exports a JSON bundle with \"atual\" and \"antigo\" payloads.",
            "Help (F1): shows available shortcuts.",
            "Close (Ctrl+Q): closes the application.",
            "Language (Alt+I): switches between pt_BR and en_US in real time.",
            "Manual (Ctrl+Shift+M) and About (Ctrl+Shift+A) are in the Options menu.",
        ),
    ),
    ManualSection(
        id="assisted-unfollow",
        title="Assisted unfollow",
        bullets=(
            "The \"No longer follow me\" tab allows selecting profiles using checkboxes.",
            "The \"🗑️ Unfollow\" button is enabled only when at least one item is checked.",
            "The app asks for confirmation before sending unfollow requests.",
            "After completion, it shows success/failure summary and may trigger automatic refresh.",
        ),
    ),
    ManualSection(
        id="persistent-files",
        title="Persistent files",
        bullets=(
            ".github_follow_compare_atual.json: current snapshot with followers/following and calculated outputs.",
            ".github_follow_compare_antigo.json: previous snapshot used for historical comparison.",
            "Paths can be overridden by environment variables:",
            "FOLLOW_COMPARE_CACHE_FILE (current) and FOLLOW_COMPARE_STATE_FILE (previous).",
            "Base persistent directory comes from source.utils.obter_caminho_persistente().",
        ),
    ),
    ManualSection(
        id="cli-mode",
        title="CLI mode (quick usage)",
        bullets=(
            "Run: py main.py --cli --user your_username",
            "Output includes summary, source (cache/graphql), rate limit, and category lists.",
            "To ignore cache in CLI, add --no-cache.",
        ),
    ),
    ManualSection(
        id="troubleshooting",
        title="Troubleshooting",
        details=(
            ManualDetails(
                summary="Missing token error",
                bullets=(
                    "Typical message: set GITHUB_TOKEN to use GraphQL without cache.",
                    "Set the environment variable and run again.",
                ),
            ),
            ManualDetails(
                summary="Unexpected counters",
                bullets=(
                    "Use force API refresh to avoid stale cached values.",
                    "Confirm the target username is correct.",
                ),
            ),
            ManualDetails(
                summary="Open/save JSON failure",
                bullets=(
                    "Check write permissions for the target directory.",
                    "Ensure file format matches expected cache/state/bundle structure.",
                ),
            ),
            ManualDetails(
                summary="Rate limit unavailable or low",
                bullets=(
                    "Wait for the API rate-limit window to reset.",
                    "Avoid frequent forced refreshes.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="privacy-support",
        title="Privacy and support",
        bullets=(
            "Data is stored locally in the user profile.",
            "The app does not send its own telemetry to third parties.",
            "The token is used only for required API authentication/actions.",
            "Contact: linceu_lighthouse@outlook.com",
        ),
    ),
)


__all__ = ["_DOC_EN_US"]
