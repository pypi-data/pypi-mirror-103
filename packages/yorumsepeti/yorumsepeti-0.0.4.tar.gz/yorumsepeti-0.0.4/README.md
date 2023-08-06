
# Yorumsepeti
##### A package for fetching restaurant reviews from yemeksepeti.com.

## Installation

To install via pip, run;

```
pip install yorumsepeti
```

Yorumsepeti requires [Selenium](https://selenium-python.readthedocs.io/index.html) to run. Do not forget to include Chromedriver.exe in your project file.

## Usage
```
from yorumsepeti import fetchers  
  
# to get n=100 comments  
fetchers.get_comments(100)
```

## Example Dataset

Example Yorumsepeti dataset can be found in [this](https://www.kaggle.com/dgknrsln/yorumsepeti) Kaggle page.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

GNU General Public License v3.0
