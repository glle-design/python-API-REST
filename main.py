#API REST: Interfaz de programación denaplicaciones para compartir recursos
from typing import Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Es un framework: Inicializamos una variable dónde tendra todas las caracteristicas de una API REST
app = FastAPI()

# CREAR CRUD: ALTA-BAJA-MODIFICACIÓN
# Crear clase: Es para hacer un modelo para las variables y los tipos de datos
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int
        
# Simularemos una base de datos
cursos_db = []
# CRUD: READ: (lectura) ALL: Leeremos todos los cursos que allá en la base de datos
@app.get("/cursos/", response_model=list[Curso])
def obtener_cursos():
    return cursos_db

# CRUD: CREATE (escribir) POST: Agregaremos un nuevo recurso a nuestra base de datos
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) # Usamos uuid para generar un id random e irrepetible
    cursos_db.append(curso) # Agrega un curso a la lista de cursos
    return curso

# CRUD: READ: (lectura) get(individual): Leeremos el curso que coincida con el que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db  if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# CRUD: APDATE (actualizar o modificar): PUT: Modificaremos un recurso que coincida con el id que mandamos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db  if curso.id == curso_id), None) 
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) #Buscamos el indice exacto dónde está el curso en nuestra lista de BASE DE DATOS
    cursos_db[index] = curso_actualizado
    return curso_actualizado

#  CRUD: DELETE: (borrado/baja): Eliminaremos un recurso que coincida con el id que mandemos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db  if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso

 







