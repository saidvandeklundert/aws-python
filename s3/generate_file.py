def generate_file(size_in_mb: int) -> bool:
    """
    Generate a file of a given size in MB

    Max size is 5 GB
    """
    if size_in_mb > 5000:
        raise ValueError("File size cannot be greater than 5GB")
    with open(f"{size_in_mb}MB.bin", "wb") as f:
        f.seek(size_in_mb * 1024 * 1024 - 1)
        f.write(b"\0")
    return True


if __name__ == "__main__":
    generate_file(1000)
    generate_file(100)