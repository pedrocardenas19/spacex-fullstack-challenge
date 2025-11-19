import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

import boto3
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(
    title="SpaceX Launches API",
    version="1.0.0",
    description="API para consultar lanzamientos de SpaceX desde DynamoDB",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos del frontend (si existe la carpeta)
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")

DYNAMO_TABLE_NAME = os.getenv("LAUNCHES_TABLE_NAME", "spacex-launches-dev")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMO_TABLE_NAME)


class Launch(BaseModel):
    launch_id: str
    mission_name: str
    rocket_id: str
    launch_date_utc: str
    launch_date_unix: int
    status: str
    launchpad_id: Optional[str] = None
    details: Optional[str] = None
    article_link: Optional[str] = None
    wikipedia: Optional[str] = None
    video_link: Optional[str] = None


class LaunchSummary(BaseModel):
    total: int
    by_status: Dict[str, int]
    by_year: Dict[str, int]


@app.get("/health")
def health_check():
    return {"status": "ok", "table": DYNAMO_TABLE_NAME}


@app.get("/launches", response_model=List[Launch])
def list_launches(
    status: Optional[str] = Query(None, description="success | failed | upcoming"),
):
    """
    Lista lanzamientos. Para 205 items podemos usar scan sin problema.
    """
    response = table.scan()
    items = response.get("Items", [])
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response.get("Items", []))

    if status:
        items = [i for i in items if i.get("status") == status]

    # Orden sencillo por fecha
    items.sort(key=lambda x: x.get("launch_date_unix", 0), reverse=True)

    return items


@app.get("/launches/{launch_id}", response_model=Launch)
def get_launch(launch_id: str):
    response = table.get_item(Key={"launch_id": launch_id})
    item = response.get("Item")

    if not item:
        raise HTTPException(status_code=404, detail="Launch not found")

    return item


@app.get("/stats/summary", response_model=LaunchSummary)
def stats_summary():
    """
    Devuelve conteos por status y por año (para gráficos).
    """
    response = table.scan()
    items = response.get("Items", [])

    total = len(items)
    by_status: Dict[str, int] = {}
    by_year: Dict[str, int] = {}

    for item in items:
        status = item.get("status", "unknown")
        by_status[status] = by_status.get(status, 0) + 1

        # Derivar año desde launch_date_utc o unix
        date_utc = item.get("launch_date_utc")
        year = None
        if date_utc:
            try:
                year = datetime.fromisoformat(
                    date_utc.replace("Z", "+00:00")
                ).year
            except Exception:
                pass

        if year is None and item.get("launch_date_unix"):
            try:
                year = datetime.utcfromtimestamp(
                    int(item["launch_date_unix"])
                ).year
            except Exception:
                pass

        if year:
            by_year[str(year)] = by_year.get(str(year), 0) + 1

    return LaunchSummary(total=total, by_status=by_status, by_year=by_year)


# Servir el frontend en la raíz (debe ir al final)
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """
    Sirve el frontend React. Cualquier ruta no manejada por la API
    devuelve el index.html para que React Router maneje la navegación.
    """
    if STATIC_DIR.exists():
        # Si es un archivo estático específico, servirlo
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Si no, devolver index.html para SPA routing
        index_path = STATIC_DIR / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
    
    raise HTTPException(status_code=404, detail="Not found")
