import argparse as arg
from PIL import Image


def colored_square(hex_rgb: str):
    rgb = hex_rgb.strip("#")
    r = int(rgb[:2], 16)
    g = int(rgb[2:4], 16)
    b = int(rgb[4:], 16)
    return f"\033[48:2::{r}:{g}:{b}m \033[49m"

def clamp(n: int, minn: int, maxx: int):
    return min(maxx, max(n, minn))

parser = arg.ArgumentParser()
parser.add_argument("-i", "--image", dest="image_path", help="image path")
parser.add_argument("-n", "--number", dest="number", help="number of points", type=int)
parser.add_argument("-m", "--mode", dest="mode", type=int, 
                    help="""direction: 0 - vertical;
                          1 - horizontal;
                          2 - top left to bottom right;
                          3 - bottom left to top right""")
parser.add_argument("-v", "--verbose", dest="verbose", action="store_true")

args = parser.parse_args()

if not args.image_path:
    print("provide a path with -i or --image")
    exit(1)

try:
    image = Image.open(args.image_path)
    rgb_image = image.convert("RGB")
except FileNotFoundError:
    print("no such file")
    exit(2)

if args.number is None or args.number < 0:
    print("invalid number of points")
    exit(3)

if args.mode is None or not (0 <= args.mode <= 3):
    print("invalid mode")
    exit(4)

size = [image.size[0] - 1, image.size[1] - 1]

if args.mode == 0:
    first_point = [size[0] // 2, 0]
    last_point  = [size[0] // 2, size[1]]
elif args.mode == 1:
    first_point = [0, size[1] // 2]
    last_point  = [size[0], size[1] // 2]
elif args.mode == 2:
    first_point = [0, 0]
    last_point  = list(size)
else:
    first_point = [0, size[1]]
    last_point  = [size[0], 0]

dX = last_point[0] - first_point[0]
dY = last_point[1] - first_point[1]
stepX = dX // (args.number + 1)
stepY = dY // (args.number + 1)

points = [first_point.copy()]

if args.verbose:
    print(f"image size: {size}")

for i in range(args.number + 1):
    first_point[0] = clamp(first_point[0] + stepX, 1, size[0])
    first_point[1] = clamp(first_point[1] + stepY, 1, size[1])
    points.append(first_point.copy())

for point in points:
    rgb_tuple = rgb_image.getpixel(tuple(point))
    rgb = "#"
    for i in range(3):
        rgb += hex(rgb_tuple[i])[2:].zfill(2)
    if args.verbose:
        print(f"{colored_square(rgb)}{point} : {rgb}")
    else:
        print(rgb)
