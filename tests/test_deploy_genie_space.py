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


def test_create_space_payload_includes_warehouse_id(monkeypatch):
    captured = {}

    def fake_post(url, headers, json):
        captured['url'] = url
        captured['json'] = json

        class FakeResponse:
            status_code = 200
            text = "{}"

            @staticmethod
            def json():
                return {"space_id": "abc123"}

        return FakeResponse()

    monkeypatch.setattr(module.requests, "post", fake_post)

    deployer = module.GenieSpaceDeployer(
        "https://dbc-123.cloud.databricks.com",
        "dapi123456",
        "retail_ai3_dev",
        warehouse_id="warehouse-123",
    )

    result = deployer.create_space({
        "space": {"display_name": "Test Space", "description": "desc"},
        "tables": ["retail_ai3.gold.product_wise_revenue"],
    })

    assert result == "abc123"
    assert captured["json"]["warehouse_id"] == "warehouse-123"
