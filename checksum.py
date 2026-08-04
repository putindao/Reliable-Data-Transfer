def calculate_checksum(data: bytes) -> int:
    """
    Tính checksum bằng cách cộng tất cả các byte.
    Chỉ giữ lại 16 bit cuối.
    """
    return sum(data) & 0xFFFF


def verify_checksum(data: bytes, checksum: int) -> bool:
    """
    Kiểm tra checksum có đúng hay không.
    """
    return calculate_checksum(data) == checksum