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
2. Download the config files `base.yml` and `vgg-seq2seq.yml` from config folder in [_VietOCR_](https://github.com/pbcquoc/vietocr) <br>
3. Download the weights for VietOCR model  [_here_](https://vocr.vn/data/vietocr/vgg_seq2seq.pth) (you can find it in `vgg-seq2seq.yml`).
4. Move the downloaded config and weight files to `model/config` directory.

## Usage

### Set up input image
Get the image file of the article you want to extract text from and put it in the `data/input` directory. <br>
> You can change the path to the input image in `config/config.yml` file. <br>

Change the value of `image_file` in `main.py` to the name of the image file you want to extract text from.

### Configure reader config
For the best result, you can configure the reader config in `main.py` file. <br>
- Mode `single-page` for single-page images, like: <br> <img src="https://github.com/lightx26/articleOCR/blob/952a2f562c8256f35da897703a33a279f3c14ee3/data/test/test_1.jpeg" width="200" />
- Mode `double-page` for double-page images, like: <br> <img src="https://github.com/lightx26/articleOCR/blob/952a2f562c8256f35da897703a33a279f3c14ee3/data/test/test.jpeg" width="200" />
### Run the application
Run `main.py`:
```angular2html
python main.py
```
### Output
The extracted text will be saved in `data/output` directory with the same name as the input image file.
> You can change the path to the output text file in `config/config.yml` file. <br>
