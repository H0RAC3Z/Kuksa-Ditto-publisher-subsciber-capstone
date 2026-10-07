"""Publish sample vehicle speed and front steering angle to KUKSA."""

import asyncio
import random

from kuksa_client.grpc import Datapoint
from kuksa_client.grpc.aio import VSSClient


KUKSA_HOST = "127.0.0.1"
KUKSA_PORT = 55555
PUBLISH_INTERVAL_SECONDS = 1


async def main():
    async with VSSClient(KUKSA_HOST, KUKSA_PORT) as client:
        while True:
            # Speed is in km/h; the steering angle is in radians, positive left.
            speed = random.uniform(0.0, 120.0)
            steering_angle = random.uniform(-0.6, 0.6)
            values = {
                "Vehicle.Speed": Datapoint(speed),
                "Vehicle.SteeringAngle": Datapoint(steering_angle),
            }
            await client.set_current_values(values)

            print(f"Vehicle speed = {speed:.1f} km/h")
            print(f"Front steering angle = {steering_angle:.3f} rad")
            print("-----------------------------")
            await asyncio.sleep(PUBLISH_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
