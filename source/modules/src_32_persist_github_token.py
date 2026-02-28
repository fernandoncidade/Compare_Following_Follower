from __future__ import annotations
import os
import base64
import ctypes
import shutil
import subprocess
from dataclasses import dataclass
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


@dataclass
class PersistTokenResult:
    user_scope_saved: bool
    system_scope_saved: bool
    user_scope_message: str
    system_scope_message: str


@dataclass
class ResetTokenResult:
    user_scope_removed: bool
    system_scope_removed: bool
    user_scope_message: str
    system_scope_message: str

def _hidden_subprocess_kwargs() -> dict[str, object]:
    if os.name != "nt":
        return {}

    kwargs: dict[str, object] = {}

    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        kwargs["startupinfo"] = startupinfo

    except Exception:
        pass

    try:
        kwargs["creationflags"] = int(getattr(subprocess, "CREATE_NO_WINDOW"))

    except Exception:
        pass

    return kwargs

def _normalize_token(raw_token: str) -> str:
    token = (raw_token or "").strip().strip('"').strip("'")

    if not token:
        raise ValueError("Token do GitHub vazio.")

    return token

def _collect_process_output(completed: subprocess.CompletedProcess[str]) -> str:
    messages: list[str] = []
    stdout_text = (completed.stdout or "").strip()
    stderr_text = (completed.stderr or "").strip()

    if stdout_text:
        messages.append(stdout_text)

    if stderr_text:
        messages.append(stderr_text)

    if messages:
        return "\n".join(messages)

    return "Comando concluído sem saída."

def _is_registry_access_denied(message: str) -> bool:
    normalized = (message or "").strip().lower()

    if not normalized:
        return False

    return (
        ("acesso ao caminho do registro negado" in normalized)
        or ("access to the registry path is denied" in normalized)
        or ("access is denied" in normalized)
        or ("acesso negado" in normalized)
    )

def _read_system_environment_value(name: str) -> str | None:
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            0,
            winreg.KEY_READ,
        ) as key:
            value, _value_type = winreg.QueryValueEx(key, name)

            if isinstance(value, str):
                return value

            return str(value)

    except Exception:
        return None

def _read_user_environment_value(name: str) -> str | None:
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_READ,
        ) as key:
            value, _value_type = winreg.QueryValueEx(key, name)

            if isinstance(value, str):
                return value

            return str(value)

    except Exception:
        return None

def _run_setx(token: str, system_scope: bool) -> tuple[bool, str]:
    args = ["setx", "GITHUB_TOKEN", token]

    if system_scope:
        args.append("/M")

    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,
            **_hidden_subprocess_kwargs(),
        )
        raw_output = _collect_process_output(completed)

        return completed.returncode == 0, raw_output

    except Exception as exc:
        scope_text = "sistema" if system_scope else "usuário"
        logger.error(f"Erro ao executar setx para escopo de {scope_text}: {exc}")
        return False, f"Falha ao executar setx para escopo de {scope_text}."

def _run_setx_system_with_uac(token: str) -> tuple[bool, str]:
    escaped_token = token.replace("'", "''")
    powershell_script = (
        "$ErrorActionPreference='Stop'; "
        f"$token='{escaped_token}'; "
        "$process = Start-Process -FilePath 'setx.exe' "
        "-ArgumentList @('GITHUB_TOKEN', $token, '/M') "
        "-Verb RunAs -WindowStyle Hidden -PassThru -Wait; "
        "exit $process.ExitCode"
    )

    try:
        completed = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-WindowStyle",
                "Hidden",
                "-Command",
                powershell_script,
            ],
            capture_output=True,
            text=True,
            check=False,
            **_hidden_subprocess_kwargs(),
        )

        output_message = _collect_process_output(completed)

        if completed.returncode != 0:
            return False, output_message

        persisted_value = _read_system_environment_value("GITHUB_TOKEN")

        if persisted_value == token:
            return True, "ÒXITO: o valor especificado foi salvo (elevação UAC)."

        return False, (
            "Comando elevado executado, mas não foi possível confirmar o valor em Variáveis do Sistema."
        )

    except Exception as exc:
        logger.error(f"Erro ao executar setx /M com elevação UAC: {exc}")
        return False, "Falha ao solicitar elevação UAC para gravação em Variáveis do Sistema."

def _run_powershell_command(script: str) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-WindowStyle",
                "Hidden",
                "-Command",
                script,
            ],
            capture_output=True,
            text=True,
            check=False,
            **_hidden_subprocess_kwargs(),
        )
        output_message = _collect_process_output(completed)
        return completed.returncode == 0, output_message

    except Exception as exc:
        logger.error(f"Erro ao executar script PowerShell: {exc}")
        return False, "Falha ao executar script PowerShell."

def _encode_powershell_script(script: str) -> str:
    encoded_bytes = script.encode("utf-16le")
    return base64.b64encode(encoded_bytes).decode("ascii")

def _run_elevated_powershell_script(script: str) -> tuple[bool, str]:
    encoded_script = _encode_powershell_script(script)
    wrapper_script = (
        "$ErrorActionPreference='Stop'; "
        f"$encoded='{encoded_script}'; "
        "$process = Start-Process -FilePath 'powershell.exe' "
        "-ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-EncodedCommand', $encoded) "
        "-Verb RunAs -WindowStyle Hidden -PassThru -Wait; "
        "exit $process.ExitCode"
    )
    return _run_powershell_command(wrapper_script)

def _clear_current_process_env(name: str) -> None:
    try:
        os.environ.pop(name, None)

    except Exception:
        pass

    try:
        os.unsetenv(name)

    except Exception:
        pass

    if os.name != "nt":
        return

    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetEnvironmentVariableW(ctypes.c_wchar_p(name), None)

    except Exception:
        pass

def _broadcast_environment_change() -> None:
    if os.name != "nt":
        return

    try:
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.c_ulong()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            "Environment",
            SMTO_ABORTIFHUNG,
            5000,
            ctypes.byref(result),
        )

    except Exception:
        pass

def _run_reset_system_with_uac() -> tuple[bool, str]:
    machine_reset_script = (
        "$ErrorActionPreference='Stop'; "
        "[Environment]::SetEnvironmentVariable('GITHUB_TOKEN', $null, 'Machine'); "
        "Remove-ItemProperty -Path "
        "'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment' "
        "-Name 'GITHUB_TOKEN' -ErrorAction SilentlyContinue; "
        "$machineValue = [Environment]::GetEnvironmentVariable('GITHUB_TOKEN', 'Machine'); "
        "if ([string]::IsNullOrEmpty($machineValue)) { "
        "Write-Output 'MACHINE_TARGET_REMOVED'; "
        "exit 0; "
        "} "
        "Write-Output 'MACHINE_TARGET_STILL_PRESENT'; "
        "exit 9"
    )

    ok, output_message = _run_elevated_powershell_script(machine_reset_script)

    if not ok:
        return False, output_message

    system_value = _read_system_environment_value("GITHUB_TOKEN")

    if system_value is None:
        return True, "Variável removida do escopo de sistema (elevação UAC)."

    return False, "Comando elevado executado, mas a variável ainda existe no escopo de sistema."

def persist_github_token(token: str) -> PersistTokenResult:
    normalized_token = _normalize_token(token)

    if os.name != "nt":
        raise RuntimeError("Persistência automática de token com setx só está disponível no Windows.")

    if shutil.which("setx") is None:
        raise RuntimeError("Comando 'setx' não encontrado neste sistema.")

    system_ok, system_message = _run_setx(normalized_token, system_scope=True)

    if (not system_ok) and _is_registry_access_denied(system_message):
        elevated_ok, elevated_message = _run_setx_system_with_uac(normalized_token)

        if elevated_ok:
            system_ok = True
            system_message = elevated_message

        else:
            system_message = f"{system_message}\nTentativa com elevação UAC: {elevated_message}"

    user_ok, user_message = _run_setx(normalized_token, system_scope=False)

    os.environ["GITHUB_TOKEN"] = normalized_token

    return PersistTokenResult(
        user_scope_saved=user_ok,
        system_scope_saved=system_ok,
        user_scope_message=user_message,
        system_scope_message=system_message,
    )

def reset_github_token() -> ResetTokenResult:
    if os.name != "nt":
        raise RuntimeError("Reset automático de token só está disponível no Windows.")

    if shutil.which("powershell") is None:
        raise RuntimeError("Comando 'powershell' não encontrado neste sistema.")

    reset_script = (
        "$ErrorActionPreference='Stop'; "
        "$isAdmin = ([Security.Principal.WindowsPrincipal] "
        "[Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole("
        "[Security.Principal.WindowsBuiltInRole]::Administrator); "
        "[Environment]::SetEnvironmentVariable('GITHUB_TOKEN', $null, 'User'); "
        "if ($isAdmin) { "
        "[Environment]::SetEnvironmentVariable('GITHUB_TOKEN', $null, 'Machine'); "
        "} else { "
        "Write-Output 'MACHINE_TARGET_NOT_ADMIN'; "
        "} "
        "Remove-Item Env:GITHUB_TOKEN -ErrorAction SilentlyContinue; "
        "Remove-ItemProperty -Path 'HKCU:\\Environment' -Name 'GITHUB_TOKEN' -ErrorAction SilentlyContinue; "
        "if ($isAdmin) { "
        "Remove-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment' "
        "-Name 'GITHUB_TOKEN' -ErrorAction SilentlyContinue; "
        "} "
        "$userValue = [Environment]::GetEnvironmentVariable('GITHUB_TOKEN', 'User'); "
        "$machineValue = [Environment]::GetEnvironmentVariable('GITHUB_TOKEN', 'Machine'); "
        "if ([string]::IsNullOrEmpty($userValue)) { Write-Output 'USER_TARGET_REMOVED'; } "
        "else { Write-Output 'USER_TARGET_STILL_PRESENT'; } "
        "if ($isAdmin) { "
        "if ([string]::IsNullOrEmpty($machineValue)) { Write-Output 'MACHINE_TARGET_REMOVED'; } "
        "else { Write-Output 'MACHINE_TARGET_STILL_PRESENT'; } "
        "}"
    )

    first_ok, first_message = _run_powershell_command(reset_script)
    _clear_current_process_env("GITHUB_TOKEN")
    _broadcast_environment_change()

    user_removed = _read_user_environment_value("GITHUB_TOKEN") is None
    system_removed = _read_system_environment_value("GITHUB_TOKEN") is None
    process_removed = "GITHUB_TOKEN" not in os.environ

    user_message = "Variável removida do escopo de usuário."

    if not user_removed:
        user_message = f"Falha ao remover variável do escopo de usuário.\n{first_message}"

    system_message = "Variável removida do escopo de sistema."

    if not system_removed:
        system_message = first_message

    if not process_removed:
        user_message = f"{user_message}\nFalha ao remover variável da sessão atual do aplicativo."

    if not system_removed:
        elevated_ok, elevated_message = _run_reset_system_with_uac()
        system_removed = _read_system_environment_value("GITHUB_TOKEN") is None
        _broadcast_environment_change()

        if system_removed and elevated_ok:
            system_message = elevated_message

        else:
            system_message = f"{system_message}\nTentativa com elevação UAC: {elevated_message}"

    return ResetTokenResult(
        user_scope_removed=user_removed,
        system_scope_removed=system_removed,
        user_scope_message=user_message,
        system_scope_message=system_message,
    )
