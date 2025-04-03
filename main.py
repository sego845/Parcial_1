from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Sego - Panadería API")
FILENAME = "sego.json"

class Pan(BaseModel):
    id: int
    nombre: str
    precio: float
    peso: float  # en gramos


def load_data():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

@app.get("/panes", response_model=list[Pan])
def lista_panes():
    return load_data()

@app.get("/panes/{pan_id}", response_model=Pan)
def obtener_pan(pan_id: int):
    panes = load_data()
    for pan in panes:
        if pan["id"] == pan_id:
            return pan
    raise HTTPException(status_code=404, detail="Pan no encontrado")

@app.post("/panes", response_model=Pan)
def crear_pan(pan: Pan):
    panes = load_data()
    if any(p["id"] == pan.id for p in panes):
        raise HTTPException(status_code=400, detail="El pan con este ID ya existe")
    panes.append(pan.dict())
    save_data(panes)
    return pan

@app.put("/panes/{pan_id}", response_model=Pan)
def actualizar_pan(pan_id: int, updated_pan: Pan):
    panes = load_data()
    for index, pan in enumerate(panes):
        if pan["id"] == pan_id:
            panes[index] = updated_pan.dict()
            save_data(panes)
            return updated_pan
    raise HTTPException(status_code=404, detail="Pan no encontrado")

@app.delete("/panes/{pan_id}")
def eliminar_pan(pan_id: int):
    panes = load_data()
    panes = [pan for pan in panes if pan["id"] != pan_id]
    save_data(panes)
    return {"message": "Pan eliminado exitosamente"}
