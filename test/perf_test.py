import sys
from pprint import pprint
import timeit
sys.path.insert(0, '/home/ubuntu/Projects/Werkstatt/Venom/TridentFrame')
pprint(sys.path)

from pybrain.inspect_ops import _inspect_sequence


def test_inspect_sequence():
    t = timeit.timeit('iseq = _inspect_sequence(["/home/ubuntu/Projects/Werkstatt/Venom/TridentFrame/imgs/fortfade.png_078.png",\
    ])\npprint(iseq)', setup="from pybrain.inspect_ops import _inspect_sequence\nfrom pprint import pprint", number=1)
    print(t)


if __name__ == "__main__":
    test_inspect_sequence()
