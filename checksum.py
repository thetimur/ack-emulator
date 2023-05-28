BYTE_ORDER = 'big'


def count(data_to_count, mod=8):
    chunk_size = __calculate_chunk_size(mod)

    return (2 ** mod - 1) - (sum(int.from_bytes(data_to_count[idx:idx + chunk_size], BYTE_ORDER)
                                 for idx in range(0, len(data_to_count), chunk_size))
                             % (2 ** mod))


def check(data_to_check, mod=8):
    chunk_size = __calculate_chunk_size(mod)

    return sum(int.from_bytes(data_to_check[idx:idx + chunk_size], BYTE_ORDER)
               for idx in range(0, len(data_to_check), chunk_size)) % (2 ** mod) == (2 ** mod - 1)


def __calculate_chunk_size(mod):
    return mod // 8
