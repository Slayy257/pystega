def _encode_text_to_bytes(text: str) -> str:
    bytes_from_text = bytes(text, 'utf-8').hex()
    return [bytes_from_text[i:i+2] for i in range(0, len(bytes_from_text), 2)]

def write_data_to_image(image_path: str, data: str, output_path: str) -> None:
    with open(image_path, "rb") as f:
        bytes_read = f.read()

        bytes_read += br"\x"
        for byte in _encode_text_to_bytes(data):
            bytes_read += bytes(byte, 'ascii')

        with open(output_path, "wb") as f2:
            f2.truncate(0)
            f2.write(bytes_read)

    print("Text hided in output.jpg !")

def _get_bytes_from_pattern(bytes: str) -> str:
    for index, byte in enumerate(bytes):
        if (byte + bytes[index + 1] == r'\\'):
            return bytes[:index]
        
def extract_data_from_image(file: str) -> str:
    with open(file, "rb") as f:
        bytes_read = f.read()
        bytes_ordered = str(bytes_read)[::-1]

        pattern = _get_bytes_from_pattern(bytes_ordered)
        
        if not pattern.endswith('x'):
            raise Exception("File format not recognized")
        
        encoded_msg = pattern.replace("'", "").replace("x", "")[::-1]
        decoded_msg = bytes.fromhex(encoded_msg)
        
        return decoded_msg.decode()