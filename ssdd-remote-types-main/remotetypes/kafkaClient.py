import json
from kafka import KafkaProducer, KafkaConsumer
import Ice
import RemoteTypes

def load_config(file_path):
    """Reads the configuration from a .txt file and returns it as a dictionary"""
    config = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.strip():
                    key, value = line.strip().split("=", 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        raise Exception(f"Configuration file not found: {file_path}")
    return config

config = load_config("configuration.txt")

KAFKA_INPUT_TOPIC = config["KAFKA_INPUT_TOPIC"]
KAFKA_OUTPUT_TOPIC = config["KAFKA_OUTPUT_TOPIC"]
KAFKA_BOOTSTRAP_SERVERS = config["KAFKA_BOOTSTRAP_SERVERS"].split(",")
CONSUMER_GROUP = config["CONSUMER_GROUP"]
AUTO_OFFSET_RESET = config["AUTO_OFFSET_RESET"]

ICE_CONFIG = [config["ICE_CONFIG"]]

ice_communicator = Ice.initialize(ICE_CONFIG)

try:
    proxy = ice_communicator.stringToProxy("factory:default -h localhost -p 10000")
    factory = RemoteTypes.FactoryPrx.uncheckedCast(proxy)
    if not factory:
        raise Exception("Unable to connect to factory")
    print("Successful connection")
except Exception as exception:
    print(f"Could not connect to the factory: {exception}")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

consumer = KafkaConsumer(
    KAFKA_INPUT_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id=CONSUMER_GROUP,
    auto_offset_reset=AUTO_OFFSET_RESET)


processed_ids = set()
    
def validate_operation(operation):
    """Validates the format of the operation received"""
    keys = ["id", "object_identifier", "object_type", "operation"]
    missing_keys = [key for key in keys if key not in operation]

    if missing_keys:
        return False, f"Invalid operation. The keys are missing: {missing_keys}"
    if "args" in operation and not isinstance(operation["args"], dict):
        print("The format for 'args' is not valid. It must be a JSON object")
        return False

    return True, None

def process_operation(operation):
    """Processes a single operation and returns the result"""
    try:
        is_valid, error_message = validate_operation(operation)
        if not is_valid:
            return {"id": operation.get("id"), "status": "error", "error": error_message}
        if operation["id"] in processed_ids:
            return {"id": operation["id"], "status": "error", "error": "Duplicated operation"}
        processed_ids.add(operation["id"])

        print(f"\n Processing operation... {operation}")

        if operation["operation"] == "iter":
            return {"id": operation["id"],
                "status": "error",
                "error": "OperationNotSupported"}

        object_type = getattr(RemoteTypes.TypeName, operation["object_type"], None)
        if object_type is None:
            return {
                "id": operation["id"],
                "status": "error",
                "error": f"Unknown object type: {operation['object_type']}"}

        identifier = operation["object_identifier"]
        obj = factory.get(object_type, identifier)
        
        types = {
            RemoteTypes.TypeName.RList: RemoteTypes.RListPrx,
            RemoteTypes.TypeName.RDict: RemoteTypes.RDictPrx,
            RemoteTypes.TypeName.RSet: RemoteTypes.RSetPrx
        }

        obj_proxy = types.get(object_type, None)
        if obj_proxy:
            obj = obj_proxy.uncheckedCast(obj)
        else:
            return {
                "id": operation["id"],
                "status": "error",
                "error": f"Object type '{operation['object_type']}' not supported."
            }

        if obj is None:
            print(f"\n Error. The factory returned None for type {object_type} and identifier {identifier}")
            return {
                "id": operation["id"],
                "status": "error",
                "error": "Object retrieval failed."
            }

        print(f"\n Object {identifier} of type {object_type} created successfully")

        args = operation.get("args", {})
        method = getattr(obj, operation["operation"], None)

        if not method:
            return {
                "id": operation["id"],
                "status": "error",
                "error": f"Operation '{operation['operation']}' not supported."
            }

        result = method(**args) if args else method()

        print(f"\n Successful operation: ID={operation['id']}, result={result}")
        return {"id": operation["id"], "status": "ok", "result": result}

    except Exception as exception:
        print(f"\n Error processing operation ID={operation.get('id', 'unknown')}: {exception}")
        return {
            "id": operation.get("id"),
            "status": "error",
            "error": type(exception).__name__,
            "details": str(exception)}


def main():
    """KafkaClient main entry point"""
    print("--------------------------------------------------------------")
    print(f"Listening to messages in the topic '{KAFKA_INPUT_TOPIC}'...")
    print("---------------------------------------------------------------")
    try:
        for message in consumer:
            try:
                raw_message = message.value.decode("utf-8")

                if "'" in raw_message and '"' not in raw_message:
                    raw_message = raw_message.replace("'", '"')

                events = json.loads(raw_message)

                if not isinstance(events, list):
                    raise ValueError(f"Invalid message format (not a list): {events}")

                responses = []
                for operation in events:
                    if not isinstance(operation, dict):
                        print(f"Invalid operation format (not a dict): {operation}")
                        continue
                    responses.append(process_operation(operation))

                if responses:
                    serialized_responses = json.dumps(responses).encode("utf-8")
                    producer.send(KAFKA_OUTPUT_TOPIC, serialized_responses)
                    producer.flush()
                    print(f"Responses sent: {responses}")
                else:
                    print("No valid responses to send.")

            except json.JSONDecodeError as error:
                print(f"Invalid JSON received: {message.value}. Error: {error}")
            except ValueError as error:
                print(f"Error in message format: {error}")
            except Exception as error:
                print(f"Error processing message: {error}")

    except KeyboardInterrupt:
        print("\nClient shutdown")
    finally:
        consumer.close()
        ice_communicator.destroy()

if __name__ == "__main__":
    main()
