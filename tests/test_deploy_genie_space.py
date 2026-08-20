import pytest

from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location(
    "deploy_genie_space",
    "C:/WORK/REPO/retail-analytics_new/scripts/deploy_genie_space.py",
)
module = module_from_spec(spec)
spec.loader.exec_module(module)


def test_normalize_workspace_url_accepts_base_url():
    assert module.normalize_workspace_url("https://dbc-123.cloud.databricks.com/") == "https://dbc-123.cloud.databricks.com"


def test_normalize_workspace_url_rejects_api_path():
    with pytest.raises(ValueError):
        module.normalize_workspace_url("https://dbc-123.cloud.databricks.com/api/2.0")
