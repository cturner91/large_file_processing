# Large File Processing

Working out the most efficient way to read data from the end of large files.

## Motivation

For debugging on a project, I wanted to expose the last N logs from the local log file. I wondered what is the most efficient way to do this, so I tested a few approaches.

The file is far too large to read into memory in its entirety and return only the final N lines.

### Simple Approach

The first thought that came to me was to read through the file, count the lines, then read again and only keep lines after line N. This however, obviously incurs two reads, which is expected to be slow.

### Pre-Allocated Approach

What if we pre-allocated a list and overwrite the item at the `i % n`-th position? Then we need to reorder the results, but this means there is only a single read operation so should be much quicker.

### Pre-Allocated Approach without divmod

Wondering if running the `i % n` operation many times is slower than simple integer counting.

### Read from end of file

If we seek to the end of the file and read a large chunk that can easily fit in memory, and return only the final N lines of that. This approach should be the quickest - but by how much?

# Results

The script was run to return the final 5 lines from a log file with 10,000,000 lines.

Function | Time Taken
--- | ---
read_last_n_lines__simple | 1.071851 seconds
read_last_n_lines__divmod | 0.562677 seconds
read_last_n_lines__integer | 0.600504 seconds
read_from_end_of_file | 0.000140 seconds

# Conclusions

`read_from_end_of_file` is orders of magnitude faster that the other approaches. This makes sense as we do not need to read the entirety of the large file at any point. This is the obvious best approach to use for my application.

`read_last_n_lines__simple` is about twice as slow as the `preallocated` methods, which is exactly as expected since it has to read the whole file twice.

Surprisingly `read_last_n_lines__integer` is slower than the `divmod` method.
