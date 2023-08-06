import contextlib
import mmap
import os

def gen(filename, length=0, offset=0):
    create = not os.path.isfile(filename)
    mode = 'w+b' if create else 'r+b'
    with open(filename, mode) as fileobj:
        if create and length == 0: length = 1
        if length:
            fileobj.seek(length + offset - 1)
            fileobj.write(b'\x00')
            fileobj.flush()
        with mmap.mmap(fileobj.fileno(),
                       length=0,
                       access=mmap.ACCESS_WRITE,
                       #offset=offset
                       ) as mmap_obj:
            yield mmap_obj

@contextlib.contextmanager
def mio(filename, length=0, offset=0):
    handle = gen(filename, length, offset)
    yield next(handle)

if __name__ == '__main__':
    with mio('test.dat') as io:
        print(io[:])

    handle = gen('test.dat')
    io = next(handle)
    io[0] = 42
    # When handle goes out of scope, io is closed
    # this is very useful in interactive mode
