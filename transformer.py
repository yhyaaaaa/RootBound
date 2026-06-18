import base64

class DataTransformer:
    """
    Handles the transformation of normal data into 'weird' sequences
    using Part B and the reconstruction process.
    """

    @staticmethod
    def transform(data, part_b):
        """
        Transforms plaintext data into a 'weird sequence' (Part A) using Part B.
        Algorithm: XOR with Part B (extended to match length) + Base64 encoding.
        """
        # Ensure data is in bytes
        data_bytes = data.encode() if isinstance(data, str) else data

        # Create a stream of Part B to match the length of the data
        # This is a simple XOR stream cipher for demonstration purposes
        b_len = len(part_b)
        transformed = bytearray()
        for i in range(len(data_bytes)):
            transformed.append(data_bytes[i] ^ part_b[i % b_len])

        # Convert the resulting bytes into a "weird looking sequence" (Base64)
        return base64.b64encode(transformed).decode()

    @staticmethod
    def reconstruct(transformed_data, part_b):
        """
        Reconstructs the original data from Part A using Part B.
        """
        # Decode the "weird sequence" back to bytes
        decoded_bytes = base64.b64decode(transformed_data)

        # XOR again with Part B to reverse the transformation
        b_len = len(part_b)
        original = bytearray()
        for i in range(len(decoded_bytes)):
            original.append(decoded_bytes[i] ^ part_b[i % b_len])

        return original.decode()
