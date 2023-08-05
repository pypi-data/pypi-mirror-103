# Chug

[![License](https://img.shields.io/static/v1?label=license&message=MIT&color=brightgreen)](https://github.com/sblmnl/ChugPy/blobl/main/LICENSE)
[![Language](https://img.shields.io/static/v1?label=language&message=Python&color=blue)](https://www.python.org/)

Chug is a symmetric encryption algorithm in which the key is calculated from a known plaintext and a known ciphertext.

## Suggestions & Bug Reports

If you would like to suggest a feature or report a bug please see the [issues](https://github.com/sblmnl/ChugPy/issues) page.

## Mathematic Overview

### Key Creation

```
p = (10, 20)
c = (1, 2, 3, 4)
k = (
        ((((p(1) + c(1)) - c(2)) * c(3)) / c(4)),
        ((((p(2) + c(1)) - c(2)) * c(3)) / c(4))
    )
```

### Decryption

```
c = (1, 2, 3, 4)
k = (6.75, 14.25)
p = (
        ((((k(1) * c(4) / c(3)) + c(2)) - c(1)),
        ((((k(2) * c(4) / c(3)) + c(2)) - c(1))
    )
```

### Variable Definitions

* **p** :   The variable that represents the plaintext value.
* **c** :   The variable that represents the ciphertext value.
* **k** :   The variable that represents the key value.

## Usage

### Installation
```
pip install chug
```

### Sample Code

```python
import binascii
from chug import Chug

plaintext = "My secret".encode("utf8")
ciphertext = "Not my secret".encode("utf8")
key = Chug.create_key(plaintext, ciphertext)
secret = Chug.decrypt(ciphertext, key)

print("plaintext\t:\t%s" % binascii.hexlify(plaintext).decode("utf8"))
print("ciphertext\t:\t%s" % binascii.hexlify(ciphertext).decode("utf8"))
print("key\t\t:\t%s" % binascii.hexlify(key).decode("utf8"))
print("secret\t\t:\t%s" % binascii.hexlify(secret).decode("utf8"))
```

### Expected Output
```
plaintext       :       4d7920736563726574
ciphertext      :       4e6f74206d7920736563726574
key             :       4324956f4356add042e2b330434fd908433fe88d433da19f434eb592433fe88d4350fc7f
secret          :       4d7920736563726574
```

## Documentation

### Methods
* **Chug.create_key(plaintext, ciphertext)**
    * `plaintext` [`bytes`](https://docs.python.org/3/c-api/bytes.html) The plaintext bytes.
    * `ciphertext` [`bytes`](https://docs.python.org/3/c-api/bytes.html) The ciphertext bytes.
    * Returns [`bytes`](https://docs.python.org/3/c-api/bytes.html)
* **Chug.decrypt(ciphertext, key)**
    * `ciphertext` [`bytes`](https://docs.python.org/3/c-api/bytes.html) The ciphertext bytes.
    * `key` [`bytes`](https://docs.python.org/3/c-api/bytes.html) The key bytes.
    * Returns [`bytes`](https://docs.python.org/3/c-api/bytes.html)

## Authors

* **Developer** - [sblmnl](https://github.com/sblmnl)

See the [contributors](https://github.com/sblmnl/ChugPy/contributors) page for a list of all project participants.

## License

This project is licensed under the MIT license - see the [LICENSE](https://github.com/sblmnl/ChugPy/blob/main/LICENSE) file for details.
