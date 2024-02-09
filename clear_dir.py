from pathlib import Path

[f.unlink() for f in Path("/y/people/ajc677/Masters_project/xhpi_run/hudson_output").glob("*") if f.is_file()] 
