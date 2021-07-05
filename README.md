# Crawler domain on Python

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)


## Описание:
 Краулер, сканирующий заданный url и извлекающий ссылки, затем рекурсивно следующий по ранее извлеченным ссылкам.
 Скрипт собирает простые ссылки не только со всего сайта, но так же извлекает ссылки, выполняя javascript с помощью библиотеки selenium.
 Входной параметр **-m** указывает количество прохождений вглубь по извлеченным ссылкам, по умолчанию 5.
 Все найденные ссылки храняться в файле txt в папке output.
 Протестировано на Ubuntu 20.04 и Windows 10 20H2
 
 > **Важно**
 > Скрипт имеет вычислительную сложность O(n),
 > что при больших значениях -m увеличивает время работы.
 > Так же при сканировании крупных сайтов, может быть
 > затрачено больше времени.

## Стек:
- [Python 3.8.1](https://www.python.org)
- [beautifulsoup4 4.9.3](https://pypi.org/project/beautifulsoup4/)
- [colorama 0.4.4](https://pypi.org/project/colorama/)
- [requests 2.25.1](https://docs.python-requests.org/en/master/)
- [requests-html 0.10.0](https://docs.python-requests.org/projects/requests-html/en/latest/)
- [selenium 3.141.0](https://selenium-python.readthedocs.io/)
- [selenium-wire 4.3.1](https://pypi.org/project/selenium-wire/)

## Установка

Создаем виртальную среду:
```
python -m venv env
```

Активируем виртуальную среду:
```
# для win 10
.\env\Scripts\activate    
# для Linux
source /env/bit/activate
```

Инсталлируем зависимости:
```
pip install -r requirements.txt
```

Далее необходимо в файле **parser_link_js.py** в переменной **osdriver** указать вебдрайвер в зависимости от операционной системы
```
# для Linux
osdriver = r'./drivers/geckodriver'
# для win10 
osdriver = r'./drivers/geckodriver.exe'
```

Затем активируем сам скрипт, где _https://example.com_ url для работы краулера, а параметр m указывает на количество :
```
python main.py https://example.com -m 10
```
После запуска краулера в командной строке синим цветом будут отображаться внешние ссылки, зеленым - внутренние. Красным цветом будут выведены ошибки произошедшие при парсинге.
По завершению работы выведется итоговая информация по сканированию.


![](/output/screenshot.PNG)


#### Приятного использования!
