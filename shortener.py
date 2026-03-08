"""
Short code generation using a global counter + base62 encoding.

Counter lives in Redis (INCR is atomic), so even multiple Write Service
instances produce unique codes with no collisions.
"""

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = len(ALPHABET)  # 62
COUNTER_KEY = "global_counter"


def encode(n: int) -> str:
    """Convert a positive integer to a base62 string."""
    if n == 0:
        return ALPHABET[0]
    digits = []
    while n:
        digits.append(ALPHABET[n % BASE])
        n //= BASE
    return "".join(reversed(digits))


def decode(s: str) -> int:
    """Convert a base62 string back to an integer."""
    n = 0
    for char in s:
        n = n * BASE + ALPHABET.index(char)
    return n


def generate_short_code(redis_client) -> str:
    """Atomically increment the global counter and return its base62 encoding."""
    counter = redis_client.incr(COUNTER_KEY)
    return encode(counter)
