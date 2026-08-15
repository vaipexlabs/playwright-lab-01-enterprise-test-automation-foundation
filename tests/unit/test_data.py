from tests.data import ScenarioDataFactory


def test_factory_is_deterministic_for_worker_and_scenario() -> None:
    factory = ScenarioDataFactory(worker_id="gw0")

    first = factory.shipping_address("checkout starter kit")
    second = factory.shipping_address("checkout starter kit")

    assert first == second
    assert first.full_name.startswith("Vaipex Test ")
    assert first.postal_code.isdigit()
    assert len(first.postal_code) == 5


def test_factory_isolates_workers_and_scenarios() -> None:
    first_worker = ScenarioDataFactory(worker_id="gw0")
    second_worker = ScenarioDataFactory(worker_id="gw1")

    values = {
        first_worker.shipping_address("starter kit"),
        first_worker.shipping_address("field guide"),
        second_worker.shipping_address("starter kit"),
    }

    assert len(values) == 3
