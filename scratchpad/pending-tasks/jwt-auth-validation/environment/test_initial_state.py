import shutil

def test_zuplo_cli_available():
    assert shutil.which("zuplo") is not None or shutil.which("npx") is not None, "zuplo or npx binary not found in PATH."
