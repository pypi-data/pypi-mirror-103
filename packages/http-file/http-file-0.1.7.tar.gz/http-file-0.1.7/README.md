# http_file

## Usage

Install using pip:
```shell
$ pip install http_file
```
Применение
=====

.. кодовый блок :: python

    #импорт вспомогательных библиотек
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    import requests
    #импорт http_file
    from http_file import download_file
    #создание новой сессии
    s = requests.Session()
    #соеденение с сервером через созданную сессию
    s.get('URL_MAIN', verify=False)
    """
    загрузка файла в 'local_filename' из 'fileUrl' через созданную сессию
    download_file('local_filename', 'fileUrl', s)