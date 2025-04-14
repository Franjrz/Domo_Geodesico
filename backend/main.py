from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from typing import Dict, List, Optional, Any

app = FastAPI(title="API Domo Geodésico")

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para los parámetros de entrada
class DomoParams(BaseModel):
    tipo_solido: str  # tetraedro, cubo, octaedro, dodecaedro, icosaedro
    # Aquí se pueden añadir más parámetros según sea necesario
    escala: Optional[float] = 1.0
    # Otros parámetros opcionales

# Función para cargar los datos de un sólido platónico
def cargar_solido(tipo_solido: str) -> Dict[str, List[float]]:
    ruta_archivo = os.path.join("semillas", f"{tipo_solido}.json")
    try:
        with open(ruta_archivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail=f"Sólido platónico '{tipo_solido}' no encontrado. Opciones disponibles: tetraedro, cubo, octaedro, dodecaedro, icosaedro"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al decodificar el archivo JSON para '{tipo_solido}'"
        )

@app.post("/api/generar-domo")
async def generar_domo(params: DomoParams):
    """
    Genera un domo geodésico basado en un sólido platónico.
    
    Parámetros:
    - tipo_solido: Tipo de sólido platónico (tetraedro, cubo, octaedro, dodecaedro, icosaedro)
    - escala: Factor de escala para el domo (por defecto: 1.0)
    
    Retorna:
    - Un diccionario con los puntos del domo geodésico
    """
    # Cargar los puntos del sólido platónico
    puntos = cargar_solido(params.tipo_solido)
    
    # Aplicar escala si es diferente de 1.0
    if params.escala != 1.0:
        for punto_id, coordenadas in puntos.items():
            puntos[punto_id] = [coord * params.escala for coord in coordenadas]
    
    # Aquí se podrían aplicar más transformaciones o cálculos según los parámetros
    
    return {
        "tipo_solido": params.tipo_solido,
        "escala": params.escala,
        "puntos": puntos
    }

@app.get("/")
async def root():
    return {"mensaje": "API de Domo Geodésico funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
