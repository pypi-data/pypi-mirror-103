from ehelply_microservice_library.service_bootstrap import ServiceBootstrap

from fastapi.testclient import TestClient

from typing import Type


def make_test_client(service: Type[ServiceBootstrap]) -> TestClient:
    class ServiceTest(service):
        def if_dev_launch_dev_server(self) -> bool:
            return False

    service = ServiceTest()

    app = service.fastapi_driver.instance

    client = TestClient(app)

    return client
