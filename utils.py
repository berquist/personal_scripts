def read_binary(binaryfilename):
    """Return the bytes present in the given binary file name."""
    with open(binaryfilename, 'rb') as binaryfile:
        bytes = binaryfile.read()
    return bytes


def make_file_iterator(filename):
    """Return an iterator over the contents of the given file name."""
    with open(filename) as f:
        contents = f.read()
    return iter(contents.splitlines())
