# Doi

Doi is a Python library for 

## Installation

Use the package manager [pip](https://pypi.org/project/doi-lookup/) to install doi.

```bash
$ pip install doi-lookup
```

## Usage

```python
import doi

print(doi.lookup("title", doi="10.1162/0162287042379847"))
print(doi.lookup("author", doi="10.1162/0162287042379847"))
print(doi.lookup("publisher", doi="10.1162/0162287042379847"))
print(doi.lookup("link", doi="10.1162/0162287042379847"))

"""
An Archival Impulse
Hal Foster
MIT Press - Journals
https://www.mitpressjournals.org/doi/pdf/10.1162/0162287042379847
"""
```

## License

>The [MIT license](https://opensource.org/licenses/MIT) (MIT)
>
>Copyright (c) [Tahir Murata](https://github.com/asimo10)
>
>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

> GitHub [@portaltree](https://github.com/asimo10)