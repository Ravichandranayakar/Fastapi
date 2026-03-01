# Rate limiting is: Abuse protection.

# Payload limit is: Resource protection.

# Sanitization is: Data integrity protection.

# All three are different layers.


from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)