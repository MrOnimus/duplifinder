# duplifinder

**WARNING:** The project has been archived because the resulting solution was too slow.

It's the utility to find duplicates.

## How to use it

This is the basic usage instructions for this project.

```sh
usage: python duplifinder.py <path> [-v] [-h] [-c] [-d INT] [-s [-H]] [-V] [-t [-S]]

positional arguments:
  path                  define the directory path

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c, --color           provides colored output
  -d INT, --depth INT   set depth of the search
  -s, --size            provides size information
  -H, --human-readable  makes size output human readable
  -V, --verbose         verbose output
  -t, --datetime        display datetime of last file modification
  -S, --sort            sorts all files according to datetime they have been created
```

## License

This project is licensed under GNU GPLv3. For any further information, please refer to
the LICENSE.md file.
