#!/usr/bin/env python3

"""Arquivo com a função principal do sistema"""

from view import View
from controller import Controller
from model import Model

def main():
  """Função principal que instancia os componentes base, abre a interface gráfica e faz o flush dos dados em memória permanente ao terminar"""
  controller = Controller()
  view = View(controller)
  
  view.run()
  
  Model().flush()

if __name__ == "__main__":
  main()
