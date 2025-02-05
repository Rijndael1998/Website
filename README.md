# Website
This is my website generation tool that I use on my website. It can take ODF and TXT formats and generate it into a webpage. There are still a lot of things to do. Thanks for checking out my repo.

There is a [to do](TODO.md) list that you can look at which lists things that the program will benefit from.

## Installation
The program is very simple to use and install. Essentially it's a bunch of scripts that with some external libraries generate the files to be used on the web. 

### Requirements
1. [Python](https://www.python.org/). Developed with [Python 3.8.4](https://www.python.org/downloads/release/python-384/) through [Python 3.10.9](https://www.python.org/downloads/release/python-3109/) but most likely the [latest version](https://www.python.org/downloads/) will work too.

### Optionals
1. [odfpy](https://pypi.org/project/odfpy/) is needed to read the ODF files. Not installing this will result in `.odt` files failing to generate.
2. [datauri](https://pypi.org/project/python-datauri/) is needed to generate the packed downloadable version of the website that contains all of the content embedded in itself. Not installing this library will result in `down.html` not generating. 

#### Future Optionals
1. [md-to-html](https://pypi.org/project/md-to-html/) will be needed to create html content from markdown. 

### Installing Python packages
To install the optional packages, simply invoke `pip`. You can install the optional libraries using the following command:

`pip install odfpy python-datauri`

## Copyrights
 - [Ion Icons](https://github.com/ionic-team/ionicons) for their filled icons
