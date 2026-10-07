# KUKSA Databroker to Eclipse Ditto

This project subscribes to vehicle speed and front steering angle in KUKSA
Databroker and reports changes to Eclipse Ditto. The upstream component that
provides values to KUKSA is managed separately.

## Setup

Create and activate a virtual environment, then install the Python dependencies:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Fetch only Ditto's Docker deployment folder with a sparse checkout, then start
the Compose deployment:

```sh
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/eclipse-ditto/ditto.git ditto
cd ditto
git sparse-checkout set deployment/docker
cd deployment/docker
docker compose up -d
```

Create the Ditto policy and thing using `policy.json` and `VSS_Ditto.json` following the instructions below. The reporter expects the thing ID `org.ovin:my-vehicle`, with `Speed` and `SteeringAngle` features.   

### Creating the Policy
1. To do it through the UI, navigate to the Policies tab of `http://localhost:8080` to view policies.   
2. Click on JSON and click create to create new policy.   
3. Paste the policy.json file contents into the body.
4. Set the policy ID to `org.ovin:my-policy` and then click create.
   
### Creating the Thing
1. Navigate to Things tab of `http://localhost:8080` to view things.   
2. Click on the Manage tab and click create.   
3. Paste the contents of `VSS_Ditto.json` into the body.   
4. Set the Thing ID to `org.ovin:my-vehicle` and then click create.

## Run

In separate terminals, from this repository directory:

1. Start KUKSA Databroker with the repository's VSS definition:

   ```sh
   docker run --rm -it -p 55555:55555 \
     -v "$(pwd)/OBD.json:/OBD.json" \
     ghcr.io/eclipse-kuksa/kuksa-databroker:main --insecure --vss /OBD.json
   ```

2. Start the upstream data provider separately and ensure it writes
   `Vehicle.Speed` and `Vehicle.SteeringAngle` to this Databroker. (Can refer to testing section if no input)

3. Start the KUKSA-to-Ditto reporter with venv activated:

   ```sh
   python3 send_kuksa_data_to_ditto.py
   ```

The reporter subscribes to `Vehicle.Speed` and `Vehicle.SteeringAngle` and
updates the corresponding Ditto feature properties when KUKSA publishes a
value change. Set `KUKSA_HOST` and `KUKSA_PORT` if the broker is not at
`127.0.0.1:55555`. Open `http://localhost:8080` to view the Ditto thing.

## Testing

To test sending data run with activated venv:

   ```sh
   python3 test_kuksa.py
   ```