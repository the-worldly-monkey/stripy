StriPy: A Python-built visual CV
=======================

<a href="https://raw.githubusercontent.com/the-worldly-monkey/stripy/master/assets/examples/1.png"><img src="https://raw.githubusercontent.com/the-worldly-monkey/stripy/master/assets/examples/1.png" width="50%" title="Example CV" alt="Example CV"></a>

_To please the eyes of recruiters and avoid boring them with endless flows of text._

Let's be honest, who wants to spend a lot of time perusing all that stuff when you have hundreds of resumes to review? This project was conceived with the recruiter's point of view in mind. The goal is to transmit the essential information in a fun, schematic and colorful way. And, even more important, with more icons, images, keywords and less text as possible.

---

## Features
- **Easily configurable**: all the information is extracted from a JSON file.
- Conveys all the information that matters, in a **schematic fashion**, and **in a handful of seconds**.
- Highly **styleable** and **customizable** template: just change the main color, and themeable icons will change accordingly! See some examples below.

## Examples

<a href="https://raw.githubusercontent.com/the-worldly-monkey/stripy/master/assets/examples/1.png"><img src="https://raw.githubusercontent.com/the-worldly-monkey/stripy/master/assets/examples/1.png" width="33%" title="Color example 1" alt="Color example 1"></a>
<a href="https://raw.githubusercontent.com/the-worldly-monkey/stripy/master/assets/examples/2.png"><img src="https://raw.githubusercontent.com/the-worldly-monkey/stripy/master/assets/examples/2.png" width="33%" title="Color example 2" alt="Color example 2"></a>
<a href="https://raw.githubusercontent.com/the-worldly-monkey/stripy/master/assets/examples/3.png"><img src="https://raw.githubusercontent.com/the-worldly-monkey/stripy/master/assets/examples/3.png" width="33%" title="Color example 3" alt="Color example 3"></a>

## Usage
```python3 cvgen.py CV_example.json```

## Minimum requirements

> [Python](https://www.python.org) 3.5.0

> [Pillow](https://python-pillow.org) 4.2.0

The `cvgen.py` script should update/download Pillow automatically if outdated/absent.

## Acknowledgements

- [Pillow: The friendly PIL fork](https://github.com/python-pillow/Pillow)
  
  Without this amazing library none of what you see here would have been possible.

- alexanderankin's fork of [pyfpdf: FPDF for Python](https://github.com/reingart/pyfpdf)
  
  I have embedded his [`image-attempt-1`](https://github.com/alexanderankin/pyfpdf/tree/image-attempt-1) branch in this project, to save the output PDF file directly without having to save also the intermediate PNG file on disk. Another very useful thing that this library allowed me to do, unlike others, was to add external links to the PDF. All the credits go to the original developers.

- Christian Robertson, for the [Roboto](https://fonts.google.com/specimen/Roboto) font, and [Font Awesome](https://fontawesome.com), for the 4 contact info icons. They are merged in a single TTF file embedded in this project.

## Author

Michele Lo Russo — [the.worldly.monkey@gmail.com](mailto:the.worldly.monkey@gmail.com)

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

**[MIT license](http://opensource.org/licenses/mit-license.php)**
