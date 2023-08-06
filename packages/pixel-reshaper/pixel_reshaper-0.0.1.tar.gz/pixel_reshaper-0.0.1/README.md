<p align="center">
  <h3 align="center">Pixel Reshaper</h3>
  <p align="center">
    This package aims to supplement the image classification ML pipeline, particularly focused on PyTorch, by streamlining image generation from tabular data. It contains a simple combination of functions. First, to unpack an entire dataset from tabular to .png form, handling all train/test splits and file structures. Second, to provide a hand-ball function to prepare and image to be loaded for real time predicition, then move the image to archive after use.
    <br>
  </p>
</p>


## Table of contents

- [Quick start](#quick-start)
- [Usage](#usage)
- [Copyright and license](#copyright-and-license)


## Quick start

The package can be installed using pip
```
pip install pixel_reshaper
```

## Usage

Import the package.
```
import pixel_reshaper as pxR
```

Next, some parameters relating to the naming of classes, and location for data to be unpacked to. These are used by the structure generation steps
```
#Classes in the data for image and directory naming
classNames = ['dog', 'cat', 'mouse']

#Location for the data to be unpacked to, and directory to create
loc = './'
dirName = 'unpacked_images'
```
The package pre-splits the data, so just supply a split proportion. Additionally, image dimensions and channels need to be specified (Auto dimensionality detection coming soon)
```
splitPercent = 0.25
dimImage = (27, 27, 3)
```
Lastly, specify the path the the dataset to be unpacked
```
fileName = './imageDataset.csv'
```
Pass all arguments to the function and the dataset will be unpacked to the desired location!
```
pxR.unpack_images(classNames, loc, dirName, splitPercent, dimImage, fileName)
```


## Copyright and license

Code released under the [MIT Licence](https://github.com/je-c/pixel_reshaper/blob/main/LICENSE).