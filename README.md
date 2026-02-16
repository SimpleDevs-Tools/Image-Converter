# Image Converter

A simple python-based application to convert image files from one format to another.

## Installation

1. Clone this repository
2. Create a virtual environment (to prevent mutating your home Python environment)
3. Install requirements: `pip install -r requirements.txt`

## Usage

### Via Command Line

```sh
python converter.py 
    <source file or dir.> 
    <ext. to convert to> 
    [-e --ext <Which input image extension to search for, read defaults below>] 
    [-od --output_dir <Where should the converted images be saved?>] 
    [-q --quality <for jpg-outputted images, what should the expected quality be? (0-100)>]
    [-ov --overwrite <If a duplicate output image is detected, should we overwrite it?>]
    [-r --recursive <If the provided source is a directory, should we recursively search all child directories?>]
    [-v --verbose <Should we verbosely print status messages?>]
```

By default, `-e --ext` has these image files pre-defined as accepted input formats:

- `.png`
- `.jpg`
- `.jpeg`
- `.tiff`
- `.bmp`
- `.webp`

Here is an example of a command, which converts a single `cube.png` file into a `.jpeg` file.

```sh
# Converting a single PNG file into a JPEG file, at 50% quality
python converter.py samples/cube.png .jpg -od converted -q 50 -ov -v

# Converting all PNG files within `samples/` into JPEG files, at 100% quality
python converter.py samples .jpg -od converted -q 100 -ov -v
```

### External Usage

You can import  the functions defined within `converter.py`. There are two core functions:

```python
# Helper: Identify and aggregate all image files with a provided src.
# The `src_path` can be either a single filename or a directory.
# `exts` is a list of accepted image formats, including periods
# `recursive_search` is a simple boolean toggle.
def identify_images(
        src_path:str, 
        exts, 
        recursive_search:bool=False
)
```

```python
# Helper: Given a list of Path images, convert them to the `target_ext` and within an `output_dir` if provided.
# For JPEG outputs, you can define the quality.
# Finally, you can determine whether the function overwrites an existing output file that is a duplicate.
def convert_images(
        images,
        target_ext,
        output_dir,
        quality,
        overwrite
)
```