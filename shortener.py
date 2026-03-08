"""
Short code generation using a global counter + shuffled-base62 encoding.

Counter lives in Redis (INCR is atomic), so even multiple Write Service
instances produce unique codes with no collisions.

The alphabet is deliberately shuffled so sequential counter values produce
non-sequential, non-guessable short codes. All codes are padded to MIN_LEN
characters so early codes aren't trivially enumerable (e.g. "1", "2", "3").
"""

# Shuffled base62 — same 62 chars as standard, reordered to break sequential patterns.
# Built by interleaving from opposite ends of the sorted charset:
#   z,0, y,1, x,2, w,3, v,4, u,5, t,6, s,7, r,8, q,9,
#   p,A, o,B, n,C, m,D, l,E, k,F, j,G, i,H, h,I, g,J,
#   f,K, e,L, d,M, c,N, b,O, a,P, Z,Q, Y,R, X,S, W,T, V,U
ALPHABET = "z0y1x2w3v4u5t6s7r8q9pAoBnCmDlEkFjGiHhIgJfKeLdMcNbOaPZQYRXSWTVU"
BASE = len(ALPHABET)  # 62
MIN_LEN = 6           # all generated codes are at least 6 characters
COUNTER_KEY = "global_counter"


def encode(n: int) -> str:
    """Convert a positive integer to a shuffled-base62 string of at least MIN_LEN chars."""
    if n == 0:
        return ALPHABET[0] * MIN_LEN
    digits = []
    while n:
        digits.append(ALPHABET[n % BASE])
        n //= BASE
    code = "".join(reversed(digits))
    return code.rjust(MIN_LEN, ALPHABET[0])


def decode(s: str) -> int:
    """Convert a shuffled-base62 string back to an integer."""
    n = 0
    for char in s:
        n = n * BASE + ALPHABET.index(char)
    return n


def generate_short_code(redis_client) -> str:
    """Atomically increment the global counter and return its shuffled-base62 encoding."""
    counter = redis_client.incr(COUNTER_KEY)
    return encode(counter)
