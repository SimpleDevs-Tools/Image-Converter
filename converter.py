from PIL import Image, UnidentifiedImageError
from pathlib import Path
import argparse

_DESC = "Python-based Image Converter"
_EXTS = [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"]
_FORMAT_MAP = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "tiff": "TIFF",
    "bmp": "BMP",
}

# Helper: Identify and aggregate all image files with a provided src.
# The `src_path` can be either a single filename or a directory.
# `exts` is a list of accepted image formats, including periods
# `recursive_search` is a simple boolean toggle.
def identify_images(
        src_path:str, 
        exts, 
        recursive_search:bool=False
):
    src = Path(src_path)    # Path of `src_path``
    images = []             # Output array

    # Helper: is the provided filepath an image?
    def is_image(path: Path) -> bool:
        try:
            with Image.open(path) as img:
                img.verify()
            return True
        except(UnidentifiedImageError, OSError):
            return False
    
    # Check if file
    if src.is_file():
        if src.suffix.lower() in exts and is_image(src):
            images.append(src)
    # Check if directory
    elif src.is_dir():
        # Recursive search or not?
        iterator = src.rglob("*") if recursive_search else src.iterdir()
        for p in iterator:
            if p.is_file() and p.suffix.lower() in exts and is_image(p):
                images.append(p)
    # Error
    else:
        raise FileNotFoundError(f"Path does nto exist: {src}")

    # Final check: is `images` empty?
    if not images:
        raise ValueError("No valid image files found")
    return images

# Helper: Given a list of Path images, convert them to the `target_ext` and within an `output_dir` if provided.
# For JPEG outputs, you can define the quality.
# Finally, you can determine whether the function overwrites an existing output file that is a duplicate.
def convert_images(
    img_paths, 
    target_ext:str, 
    output_dir:str=None,
    quality:int=95,
    overwrite:bool=False
):
    target_ext = _FORMAT_MAP.get(target_ext.lower().lstrip('.'))
    if target_ext is None:
        raise ValueError(f'Unsupported output format: {target_ext}')
    output_dir = Path(output_dir) if output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []

    for src in img_paths:
        with Image.open(src) as img:
            # ---- mode correction ----
            if target_ext == "JPEG" and img.mode in {"RGBA", "LA", "P"}:
                img = img.convert("RGB")
            # ---- output path ----
            dst = (output_dir or src.parent) / f"{src.stem}.{target_ext}"
            if dst.exists() and not overwrite:
                raise FileExistsError(f"File exists: {dst}")
            # ---- save params ----
            save_kwargs = {}
            if target_ext in ["JPEG", "WEBP"]:
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True
            img.save(dst, format=target_ext.upper(), **save_kwargs)
            outputs.append(dst)
    return outputs


# ==========================================================================
# Example Usage via Command Line
# ==========================================================================

parser = argparse.ArgumentParser(description=_DESC)
parser.add_argument('src', help="The source image (or directory) relative to the root directory. If a directory is provided, it will scane for all images within the provided directory.", type=str)
parser.add_argument('ext', help="The output extension format (e.g. 'png', 'jpeg'). Make sure to prefix a period (e.g. '.jpg')", type=str)
parser.add_argument('-e', '--exts', help="Modify this argument if you want to control which kinds of extensions to check. Make sure to add the period.", nargs='+', default=_EXTS)
parser.add_argument('-od', '--output_dir', help="Define an output directory if needed. This is relative to the root directory.", type=str, default=None)
parser.add_argument('-q', '--quality', help="Quality value (0-100) for JPEG-based outputs only", type=int, default=95)
parser.add_argument('-ov', '--overwrite', help="Should we overwrite an output image if it already exists?", action='store_true')
parser.add_argument('-r', '--recursive', help="If a directory is provided, are we searching recursively?", action='store_true')
parser.add_argument('-v', '--verbose', help="Should we be verbose with printing messages?", action='store_true')
args = parser.parse_args()

if args.verbose:
    print(f"Searching provided input: {args.src}")
images = identify_images(args.src, args.exts, args.recursive)
if args.verbose:
    print(f"Found {len(images)} images within the provided input:")
    for img in images:
        print("\t", img)

converted_images = convert_images(
    images,
    target_ext=args.ext,
    output_dir=args.output_dir,
    quality=args.quality,
    overwrite=args.overwrite
)
if args.verbose:
    print(f"Converted {len(converted_images)} images")
    for img in converted_images:
        print('\t', img)