import importlib
from pathlib import Path

modulo = importlib.import_module("app.core.database.connection")
motor = getattr(modulo, "engine", None)

if motor is None:
    print("No encontré 'engine'. Nombres disponibles:")
    print([n for n in dir(modulo) if not n.startswith("_")])
    raise SystemExit(1)

sql = Path("actualizar_base.sql").read_text(encoding="utf-8")

with motor.begin() as conexion:
    conexion.exec_driver_sql(sql)

print("Base de datos actualizada.")