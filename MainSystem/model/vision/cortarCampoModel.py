import numpy as np
from model import ModelContext

class CortarCampoModel(ModelContext):
  """Mantém as variáveis como pontos clicados para a view de cortar campo"""
  
  def __init__(self):
    ModelContext.__init__(self, {
      "clicked_points_homography": ("clicked_points_homography", []),
      "clicked_points_crop": ("clicked_points_crop", [])
    })
    """Variáveis armazenadas no modelo"""
