import hashlib


def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Tính hash của một file.

    Parameters
    ----------
    file_path : str
        Đường dẫn file.

    algorithm : str
        "sha256" hoặc "md5"

    Returns
    -------
    str
        Chuỗi hash dạng hex.
    """

    if algorithm.lower() == "sha256":
        hasher = hashlib.sha256()

    elif algorithm.lower() == "md5":
        hasher = hashlib.md5()

    else:
        raise ValueError("Unsupported algorithm.")

    with open(file_path, "rb") as f:

        while True:

            chunk = f.read(4096)

            if not chunk:
                break

            hasher.update(chunk)

    return hasher.hexdigest()