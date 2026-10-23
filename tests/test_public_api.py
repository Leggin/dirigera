from src import dirigera


def test_all_exported_names_exist() -> None:
    for name in dirigera.__all__:
        assert hasattr(dirigera, name), name
