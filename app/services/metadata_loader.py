def load_modules_with_quality():
	"""
	Carga los módulos y les agrega el campo quality_state desde el reporte de calidad si existe.
	"""
	data_file = os.path.join("data", "modules_index.json")
	if not os.path.exists(data_file):
		return []
	with open(data_file, "r") as f:
		modules = json.load(f)
	quality = load_quality_states()
	for m in modules:
		m["quality_state"] = quality.get(m["id"], m.get("quality_state", "UNKNOWN"))
	return modules
import os
import json

def load_quality_states():
	"""
	Lee el archivo .evidence/iac-quality-report.json si existe y retorna un dict {module_id: result}.
	Si no existe, retorna un dict vacío.
	"""
	path = ".evidence/iac-quality-report.json"
	if not os.path.exists(path):
		return {}
	with open(path) as f:
		data = json.load(f)
	return {m["id"]: m["result"] for m in data.get("modules", [])}
