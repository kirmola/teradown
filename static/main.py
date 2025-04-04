import base64
from urllib.parse import quote

def sign2(j: str, r: str) -> bytes:
    a = [ord(j[i % len(j)]) for i in range(256)]
    p = list(range(256))

    u = 0
    for q in range(256):
        u = (u + p[q] + a[q]) % 256
        p[q], p[u] = p[u], p[q]

    i = u = 0
    o = bytearray()
    for q in range(len(r)):
        i = (i + 1) % 256
        u = (u + p[i]) % 256
        p[i], p[u] = p[u], p[i]
        k = p[(p[i] + p[u]) % 256]
        o.append(ord(r[q]) ^ k)  # Use bytes instead of str

    return bytes(o)  # Ensure output is bytes

# Given values
sign1 = input("Enter sign 1:")
sign3 = input("Enter sign 3:")

# Generate raw sign and encode in Base64
raw_sign = sign2(sign3, sign1)
base64_sign = quote(base64.b64encode(raw_sign).decode())  # Ensure correct byte encoding

# Compare with the provided sign

print("Generated Sign (Base64):", base64_sign)
