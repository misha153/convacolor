# convacolor
[![GitHub license](https://img.shields.io/github/license/misha153/convacolor)](https://github.com/misha153/convacolor)

## Information
### Current version:
- 0.9.2 (beta)
### Brief description of the functionality:
> After importing the library, you get access to functions such as:
> - `get_cmyk`
> - `get_hsv`
> - `get_hex`
> - `get_ncs`
> 
> Functions `get_cmyk` and `get_hsv` have an additional parameter `output_mode`.
> `'i'` is set by default, that is, the data will be in the standard for this color model in the form.
> If you change it to `'f'`, the values will be between 0 and 1

## Purpose: 
>- Make a library that allows to convert colors from RGB to NCS (Natural Color System).
https://en.wikipedia.org/wiki/Natural_Color_System

## To access the library functions use:
`from convacolor import *`

## Running requirements:
>- Python 3

### Install it via pip:
```python
pip install convacolor
```
