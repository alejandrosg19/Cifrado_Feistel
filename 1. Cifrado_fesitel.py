def hex_to_bin(hex_val: str) -> str:
    # Convierte un caracter hexadeciamal a binario.
    decimal_val = int(hex_val, 16)
    binary_val = bin(decimal_val)[2:]
    return binary_val

def complete_binary(binary: str, size_binary: int) -> str:
    # Completa un numero binario al tamaño deseado.
    return binary.zfill(size_binary)

def generate_key(iterations: int) -> list:
    # Generar todas las claves de un caracter de 8 bits en binario = 256.
    keys = []
    for i in range(iterations):
        key = format(i, '08b')
        keys.append(key)
    return keys

def generateSubKeys(cantRotate: int, keyMain: str, address: str = "r") -> list:
    # Genera todas las subclaves de la key haciendo la rotacion tanto a la derecha como izquierda.
    return [subKey[4:] for subKey in [keyMain[i:] + keyMain[:i] if address == "r" and i < 0 
            else keyMain[i+1:] + keyMain[:i+1] if address == "l" else keyMain[i+1:] + keyMain[:i+1]  for i in range(cantRotate)]]

def xor(a, b):
    # Realiza la funcion XOR entre dos numero enteros.
    a = int(a)
    b = int(b)
    return int((a and not b) or (not a and b))

def cifrado_feistel(msg_character: str, sub_keys: list):
    # Realiza el proceso del cifrado de feistel, 
    # tomando como entradas un caracter del mensaje y las lista de las subKeys que iran iterando en cada ronda
    left = msg_character[:4]
    rigth = msg_character[4:]
    
    char_desencrypt = []
    for ronda in range(7, -1, -1):
        par_xor = list(zip(list(rigth), list(sub_keys[ronda])))
        char_desencrypt = [xor(par[0],par[1]) for par in par_xor]

        par_xor_desencrypt = list(zip(list(left), char_desencrypt))
        xor_left_fun = [xor(par[0],par[1]) for par in par_xor_desencrypt]
        left , rigth = rigth, xor_left_fun
    
    result = [str(ent) for ent in [*rigth, *left]]
    return "".join(result)

if __name__ == "__main__":
    # Funcion principal donde se definiran las variables iniciales de las cuales son:
    # El mensaje en hexadecimal a evaluar
    # La lista de las keys posibles de 0 a 256 en binario
    # El loop principal que recorre cada una de las keys que se van a evaluar en cada caracter del mensaje.

    msg_hex = ['ab','49','72','7e','22','64','6f','63','68','22','77','69','75','22','62','63','74','65','6f','60','75','67','75','23']
    msg_bin = [complete_binary(hex_to_bin(value), 8) for value in msg_hex]
    keys = generate_key(256)
    for key in keys:
        result = ''
        sub_keys = generateSubKeys(8, key, 'r')
        for msg_character in msg_bin:
            char_bin = cifrado_feistel(msg_character, sub_keys)
            char_decimal = int(char_bin, 2)
            char = chr(char_decimal)
            result += char

        print("KEY: ", key ,", Result: ",result, "\n___________________")

