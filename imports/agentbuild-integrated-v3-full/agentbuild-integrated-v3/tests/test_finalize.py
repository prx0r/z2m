import io
from pathlib import Path
import zipfile
import pytest

from agentbuild.finalize import _safe_extract_zip, find_app_root


def test_find_app_root_current_layout(tmp_path):
    app = tmp_path / "workspace" / "app"
    app.mkdir(parents=True)
    (app / "package.json").write_text("{}")
    assert find_app_root(tmp_path) == app


def test_safe_extract_rejects_zip_slip(tmp_path):
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("../escape.txt", "bad")
    with pytest.raises(ValueError):
        _safe_extract_zip(archive, tmp_path / "out")
    assert not (tmp_path / "escape.txt").exists()
