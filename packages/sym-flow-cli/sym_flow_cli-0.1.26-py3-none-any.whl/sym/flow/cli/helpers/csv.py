import json
from typing import Dict, List


def set_connectors(path: str, integrations: List[Dict[str, str]]):
    try:
        import xattr
    except:
        return

    connectors = json.dumps({i["name"]: i["type"] for i in integrations}).encode("utf-8")
    xattr.xattr(path).update({"user.sym.connectors": connectors})
