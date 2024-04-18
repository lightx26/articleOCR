# ArticleOCR: Extract text from images of articles

ArticleOCR: Extract Text from Images of Articles <br>
This application is built on top of VietOCR (https://github.com/pbcquoc/vietocr), a tool for Optical Character Recognition (OCR) in Vietnamese.

The main goal of this project is to extract text from images of articles and save it to an editable plain text file.

## Installation
### Clone this project:
```angular2html
git clone https://github.com/lightx26/articleOCR
```

### Install dependencies
You can find the installation guide for **VietOCR**  [_here_](https://github.com/pbcquoc/vietocr) <br>
The other dependencies can be found in `requirements.txt`. <br>
Or you can install them by running the following command:
```
pip install -r requirements.txt
``` 

### Install config files and weights for VietOCR model
After installing the dependencies, some files need to be downloaded and moved to the correct directories. <br>
1. Create a directory `model/config` in the root directory of the project.
2. Download the config file [_here_](https://drive.google.com/file/d/1Xo9bdyp2fo-E0nGSqRsgMrXaAFBPKUO3/view?usp=drive_link) <br>
3. Download the weights file for VietOCR model  [_here_](https://drive.google.com/file/d/1z-tXzVhp2jxdCjqKIFQt-dIL9nAFzi1X/view?usp=drive_link).
> _Above is my config and weights, you can use the original config and weights from VietOCR repository, or use your own config and weights_ <br>
4. Move the downloaded config and weight files to `model/config` directory.
5. Rename the config file to `myconfig.yml` and weights file to `myseq2seq.pth`.

## Usage

[//]: # (### Set up input image)

[//]: # (Get the image file of the article you want to extract text from and put it in the `data/input` directory. <br>)

[//]: # (> You can change the path to the input image in `config/config.yml` file. <br>)

[//]: # ()
[//]: # (Change the value of `image_file` in `main.py` to the name of the image file you want to extract text from.)

### Configure reader config
For the best result, you can configure the reader config in `config/config.yml` file. <br>
- Mode `single-page` for single-page images, like: <br> <img src="https://github.com/lightx26/articleOCR/blob/952a2f562c8256f35da897703a33a279f3c14ee3/data/test/test_1.jpeg" width="200" />
- Mode `double-page` for double-page images, like: <br> <img src="https://github.com/lightx26/articleOCR/blob/952a2f562c8256f35da897703a33a279f3c14ee3/data/test/test.jpeg" width="400" />
### Run the application
Run `main.py`:
```angular2html
python main.py -i <image_file> -m <mode> -d <destination>
```

Flags:
- `--image` or `-i`: The path to the image file you want to extract text from.
- `--mode` or `-m`: The mode of the image file, `single-page` or `double-page`. Default is `double-page`.
- `--destination` or `-d`: The name of the output text file. Default is `data/output`.
### Output
The extracted text will be saved in `destination` directory with the same name as the input image file.
> You can change the default directory contains output text in `config/config.yml` file. <br>
