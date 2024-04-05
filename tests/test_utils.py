from src.dirigera.hub.utils import camelize_dict


def test_camelize_dict():
    data = {
        "key_a": "data_b",
        "key_b": {
            "key_b_a": "data_b_a",
            "key_b_b": {"key_b_b_a": "data_b_a", "key_b_b_b": ["a_b_c"]},
        },
    }
    result = camelize_dict(data)
    assert "keyA" in result
    assert result["keyA"] == data["key_a"]
    assert "keyB" in result
    assert "keyBA" in result["keyB"]
    assert result["keyB"]["keyBA"] == data["key_b"]["key_b_a"]
    assert "keyBBA" in result["keyB"]["keyBB"]
    assert result["keyB"]["keyBB"]["keyBBA"] == data["key_b"]["key_b_b"]["key_b_b_a"]
    assert "keyBBB" in result["keyB"]["keyBB"]
    assert result["keyB"]["keyBB"]["keyBBB"] == data["key_b"]["key_b_b"]["key_b_b_b"]
