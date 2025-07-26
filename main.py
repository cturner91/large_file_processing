import unittest
from time import perf_counter


FILENAME = './large_file.log'


def make_large_file() -> None:
    with open(FILENAME, 'w') as f:
        for i in range(10_000_000):
            f.write(f"This is line {i}\n")


def read_last_n_lines__simple(n: int) -> list[str]:
    # read file to get the number of lines, then read again and keep all lines after X-N
    with open(FILENAME, 'r') as f:
        for i, line in enumerate(f.readlines()):
            pass
    max_lines = i

    result = []    
    with open(FILENAME, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if i > (max_lines - n):
                result.append(line)

    return [x.strip() for x in result]


def read_last_n_lines__divmod(n: int) -> list[str]:
    # pre-allocate a list of length N. Overwrite the i-th term each time

    result = [None] * n
    with open(FILENAME, 'r') as f:
        for i, line in enumerate(f.readlines()):
            result[i % n] = line
    
    # probably finished in the middle of the list, so re-order it
    idx = i % n + 1
    result = result[idx:] + result[:idx]
    return [x.strip() for x in result]


def read_last_n_lines__integer(n: int) -> list[str]:
    # Same as above but rather than using divmod, use an integer counter

    result = [None] * n
    with open(FILENAME, 'r') as f:
        r = 0
        for i, line in enumerate(f.readlines()):
            result[r] = line

            r += 1
            if r >= n:
                r = 0

    # probably finished in the middle of the list, so re-order it
    idx = i % n + 1
    result = result[idx:] + result[:idx]
    return [x.strip() for x in result]


def read_from_end_of_file(n: int) -> list[str]:
    # read the file backwards, keeping track of the number of lines read

    with open(FILENAME, 'r') as f:  # Open in binary mode for better performance
        f.seek(0, 2)  # Move to the end of the file
        position = f.tell()

        # Read a chunk backwards (more efficient than reading byte by byte)
        # set chunk big enough that it definitely covers enogh lines
        chunk_size = min(4096, position)  # 4kb is enough
        position -= chunk_size
        f.seek(position)
        chunk = f.read(chunk_size)

    lines = chunk.split('\n')
    result = lines[-n-1:-1]

    return [x.strip() for x in result]


class ReadTests(unittest.TestCase):

    def test__5_lines(self):
        for func in (
            read_last_n_lines__simple,
            read_last_n_lines__divmod,
            read_last_n_lines__integer,
            read_from_end_of_file,
        ):
            dt0 = perf_counter()
            result = func(5)
            dt1 = perf_counter()

            self.assertEqual(result, [
                'This is line 9999995',
                'This is line 9999996',
                'This is line 9999997',
                'This is line 9999998',
                'This is line 9999999',
            ])

            print(f"{func.__name__:>40} took {dt1 - dt0:.6f} seconds to run")


if __name__ == "__main__":
    # make_large_file()
    unittest.main()
