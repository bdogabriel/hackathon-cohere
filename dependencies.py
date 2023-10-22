import os
import subprocess

def install_dependencies():

    # Obtém a lista de dependências do projeto
    with open("requirements.txt", "r") as f:
        requirements = f.read().splitlines()

    # Instala as dependências
    for dependency in requirements:
        subprocess.call(["pip", "install", dependency])


if __name__ == "__main__":
    install_dependencies()
