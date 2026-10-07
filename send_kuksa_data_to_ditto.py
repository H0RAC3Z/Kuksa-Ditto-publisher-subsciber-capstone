"""Read vehicle signals from KUKSA Databroker and write them to Eclipse Ditto."""

import asyncio
import os

import requests
from kuksa_client.grpc.aio import VSSClient


KUKSA_HOST = os.getenv("KUKSA_HOST", "127.0.0.1")
KUKSA_PORT = int(os.getenv("KUKSA_PORT", "55555"))
DITTO_URL = "http://localhost:8080/api/2/things/org.ovin:my-vehicle/features"
DITTO_AUTH = ("ditto", "ditto")

FEATURE_MAP = {
    "Vehicle.Speed": "Speed",
    "Vehicle.SteeringAngle": "SteeringAngle",
}


def update_ditto(data):
    """Write the latest KUKSA values to their matching Ditto features."""
    for kuksa_path, value in data.items():
        feature = FEATURE_MAP[kuksa_path]
        try:
            response = requests.put(
                f"{DITTO_URL}/{feature}/properties",
                json={"value": value},
                auth=DITTO_AUTH,
                timeout=10,
            )
            response.raise_for_status()
            print(f"Updated Ditto: {feature} = {value}")
        except requests.RequestException as exc:
            # Keep listening to KUKSA if an individual Ditto update fails.
            print(f"Failed to update Ditto feature {feature}: {exc}")


async def main():
    paths = list(FEATURE_MAP)
    async with VSSClient(KUKSA_HOST, KUKSA_PORT) as client:
        print(f"Subscribing to {len(paths)} KUKSA signals and reporting changes to Ditto")
        async for values in client.subscribe_current_values(paths):
            data = {
                path: values[path].value
                for path in paths
                if path in values and values[path] is not None
                and values[path].value is not None
            }
            if data:
                # HTTP requests are synchronous; keep them off the subscription loop.
                await asyncio.to_thread(update_ditto, data)


if __name__ == "__main__":
    asyncio.run(main())
