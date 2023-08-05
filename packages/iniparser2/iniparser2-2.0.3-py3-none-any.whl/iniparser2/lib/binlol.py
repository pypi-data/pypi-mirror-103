"""binary stuff lol"""


__version__ = "1.1.0"


class FileFormatError(Exception):
    """raised when file format is invalid"""


def parse_string(string):
    """parse string to binary tree"""
    string_char = list(string.encode())
    bin_tree = list()

    for char in string_char:
        cbin = hex(char)
        bin_tree.append(cbin[2:])

    return bin_tree


def parse_bin_tree(bin_tree):
    """parse binary tree of string to string"""
    leaves = list()

    for branch in bin_tree:
        char = chr(int(branch, base=16))
        leaves.append(char)

    return "".join(leaves)


def dump(filename, bin_tree, chunk_size=8, file_format="BINLOL"):
    """dump bin tree to file"""
    chunks = generate_chunk(bin_tree, chunk_size)

    with open(filename, "w+") as file:
        file.write("\t".join(parse_string(file_format)) + "\n")  # file format
        for chunk in chunks:
            file.write("\t".join(chunk) + "\n")


def load(filename):
    """load raw data in binary tree format from binary file"""

    chunks = parse_bin_file(filename)

    return parse_chunks(chunks)


def parse_bin_file(filename, file_format="BINLOL"):
    """parse binary file to chunks"""
    lines = open(filename, "r").readlines()
    chunks = list()

    file_format = parse_bin_tree(lines[0].strip().split("\t"))
    if file_format != file_format:
        raise FileFormatError("Incorrect file format, File: %s" % filename)

    del lines[0]  # deletes file format line

    for line in lines:
        line = line.strip()
        chunk = line.split("\t")

        chunks.append(chunk)

    return chunks


def parse_chunks(chunks):
    """parse chunks to binary tree"""
    bin_tree = list()

    for chunk in chunks:
        for block in chunk:
            bin_tree.append(block)

    return bin_tree


def generate_chunk(bin_tree, chunk_size):
    """generate chunks from binary tree"""
    chunk = list()
    chunk.append([])

    chunk_len = 0
    chunk_point = 0

    for branch in bin_tree:
        if chunk_len >= chunk_size:
            chunk_len = 0
            chunk_point += 1
            chunk.append([])

        if chunk_len < chunk_size:
            chunk_len += 1

            chunk[chunk_point].append(branch)

    return chunk
