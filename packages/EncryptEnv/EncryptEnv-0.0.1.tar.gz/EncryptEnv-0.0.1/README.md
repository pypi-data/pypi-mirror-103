# Installation

# Usage
```python
from EncryptEnv.encrypt import generate_key, encyrpt_key, restore_key
key = generate_key()
print(key)

msg = "<your_msg>"
entrypted_msg = encyrpt_key(key, msg)
print(entrypted_msg)

msg = restore_key(key, entrypted_msg)
print(msg)
```
