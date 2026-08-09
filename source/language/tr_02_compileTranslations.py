import os
import subprocess

import sys

def compilar_traducoes():
    diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    diretorio_traducoes = os.path.join(diretorio_base, "language", "translations")

    lrelease_path = os.path.join(os.path.dirname(sys.executable), "pyside6-lrelease.exe")
    if not os.path.exists(lrelease_path):
        lrelease_path = "pyside6-lrelease"

    for arquivo in os.listdir(diretorio_traducoes):
        if arquivo.endswith('.ts'):
            arquivo_ts = os.path.join(diretorio_traducoes, arquivo)
            arquivo_qm = os.path.join(diretorio_traducoes, arquivo.replace('.ts', '.qm'))

            print(f"Compilando: {arquivo}")
            try:
                resultado = subprocess.run(
                    [lrelease_path, arquivo_ts, "-qm", arquivo_qm],
                    check=True, 
                    capture_output=True, 
                    text=True
                )
                print(f"Sucesso: {resultado.stdout}")

            except subprocess.CalledProcessError as e:
                print(f"Erro ao compilar {arquivo}: {e}")
                print(f"Saída: {e.output}")
            except FileNotFoundError:
                print(f"Erro: O sistema não pode encontrar '{lrelease_path}'. Certifique-se de estar no ambiente virtual.")

if __name__ == "__main__":
    compilar_traducoes()
