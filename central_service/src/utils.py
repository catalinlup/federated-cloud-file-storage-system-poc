import uuid
import metrohash

def generate_unique_id() -> str:
    """
    Generates a unique identifier.
    """
    return str(uuid.uuid4())


def compute_hash(x):
    return metrohash.hash64_int(x, seed=0)
