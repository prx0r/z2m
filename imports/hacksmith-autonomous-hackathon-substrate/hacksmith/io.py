import json
from pathlib import Path

def load_spec(path='ENTRY_SPEC.json'):
    return json.loads(Path(path).read_text(encoding='utf-8'))
