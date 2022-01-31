# Курс Python

## Инструкция по настройке окружения и сдаче заданий

Не стесняйтесь писать любые вопросы в чат курса — поможем с настройкой!

<details><summary><b>Настройка окружения</b></summary>

### Регистрация
Для начала вам нужно зарегистрироваться на [python-math-cs.compscicenter.ru](https://python-math-cs.compscicenter.ru).

Если вы уже регистрировались в системе, можно просто нажать "Login".
Если вы не помните или не уверены, то можете попробовать зарегистрироваться, и в случае, если такой пользователь уже имеется, получите сообщение об ошибке: "Email has already been taken". В таком случае тоже смело жмите "Login".

Кодовое слово, необходимое при регистрации, смотрите в [lms](https://emkn.ru/courses/2022-spring/4.79-python_lang/about/)

<img src="https://gitlab.manytask.org/spbu-math-cs-python/spring-2022/-/raw/master/img/sign_in.jpg" width=800/>

Далее вы попадете на [gitlab.manytask.org](https://gitlab.manytask.org), где должны будете залогиниться, используя логин-пароль, который вы вводили в форму регистрации ранее.
Если вы проходили эту процедуру ранее и gitlab вас помнит, то этот шаг автоматически будет пропущен.

В итоге вы должны попасть на главную python-math-cs.compscicenter.ru, которая выглядит примерно так:

<img src="https://gitlab.manytask.org/spbu-math-cs-python/spring-2022/-/raw/master/img/web_interface.png" width=800/>

### Добавление ssh-ключа
C [главной страницы](https://python-math-cs.compscicenter.ru) нужно зайти в свой репозиторий (ссылка "MY REPO" кликабельна) и добавить публичный ssh-ключ в настройках профиля в gitlab.manytask.org.

</details>

<details><summary><b>Настройка окружения в Linux</b></summary>

#### Создание ssh-ключа
Можно почитать [туториал гитлаба](https://gitlab.manytask.org/help/ssh/README#gitlab-and-ssh-keys) о том как создать и добавить в аккаунт ssh ключ, а можно проследовать инструкции ниже. Если вы используете инструкцию гитлаба, не забудьте пройти также по ссылке [declare what host](https://gitlab.manytask.org/help/ssh/README#working-with-non-default-ssh-key-pair-paths), где описано как указать какой ключ использовать для подключения к гитлабу.

Если вы не делали по инструкции гитлаба:
- Воспользуйтесь `ssh-keygen` (возможно, вам придется поставить `openssh-client`), затем скопируйте **.pub** ключ:
```bash
# Если не стоит ssh-keygen (и у вас Debian/Ubuntu):
apt-get install openssh-client

# Создаем ключ:
ssh-keygen -t ed25519 -f ~/.ssh/manytask_ed25519
# Обратите внимание, что вы можете не указывать пароль для ключа,
# чтобы не приходилось его потом вводить на каждое действие c ключом
# Это стандартная практика, хотя и не очень безопасная

# Выводим содержимое **публичного** ключа в консоль:
cat ~/.ssh/manytask_ed25519.pub
# Его надо просто скопировать, как есть, включая подпись - обычно это "ваш-логин@имя-устройства"
# ВАЖНО! Публичным ключом можно делиться, приватным (то же имя, без .pub на конце) — никогда,
# иначе злоумышленник сможет представиться вами
```

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/FMHgxsL.png" width=800/></details></br>

- Идете на [gitlab.manytask.org](https://gitlab.manytask.org)

- Жмете на иконку с вашим профилем в правом верхнем углу -> `Settings` -> слева жмете на `SSH keys`

- Вставляете ключ в формочку, жмете "Add key"

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/CSPBoGp.png" width=800/></details></br>

- Cоздайте ssh-config c таким содержимым, чтобы при подключении
к `gitlab.manytask.org` использовался ваш новый ключ:
```bash
> cat ~/.ssh/config
Host gitlab.manytask.org
    IdentityFile ~/.ssh/manytask_ed25519
```

<details><summary><a>Как проверить себя?</a></summary></br>

Из консоли выполнить:
```bash
ssh git@gitlab.manytask.org
```

Вывод должен быть примерно таким:
```
PTY allocation request failed on channel 0
Welcome to GitLab, @hiverus!
Connection to gitlab.manytask.org closed.
```
</details>

Если что-то не получилось — обращайтесь в чатик.

#### Установка git

О том, что такое гит, и как вообще с ним и с Питоном работать, мы рассказывали во [втором семинаре 2021 года](https://tinyurl.com/PythonGit).

С некоторой вероятностью гит уже установлен, проверить можно так: `git --version`.

Если не установлен, и у вас Ubuntu/Debian, то всё просто:
```bash
sudo apt-get install git
```
Если у вас другой дистрибутив, то думается, вы и сами знаете, как в нем поставить пакет.

#### Клонирование и настройка репозитория

```bash
# Заходим в домашнюю директорию, где разместится репозиторий с задачами
> cd /home/`whoami`

# Клонируем себе репозиторий с задачками
git clone git@gitlab.manytask.org:spbu-math-cs-python/spring-2022.git

# Переходим в директорию с задачами
cd spring-2022
# Настраиваем гит так, чтобы он знал нас "в лицо"
git config --local user.name "<ваш логин с python-math-cs.compscicenter.ru>"
git config --local user.email "<ваш емейл с python-math-cs.compscicenter.ru>"

# Указываем, что отправлять решения нужно в ВАШ репозиторий на gitlab.manytask.org
git remote set-url --push origin git@gitlab.manytask.org:spbu-python-spring-2022/<ваш репозиторий>

# Например для логина sidor:
git remote set-url --push origin git@gitlab.manytask.org:spbu-math-cs-python/sidor

# Имя вашего репозитория доступно по ссылке "MY REPO"
```

#### Установка интерпретатора и доп. пакетов

Мы используем версию питона 3.9.7

- Поставьте [pyenv](https://github.com/pyenv/pyenv#installation)
```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

Будет много текста, который, скорее всего, закончится
```
WARNING: seems you still have not added 'pyenv' to the load path.

# Load pyenv automatically by adding
# the following to ~/.bashrc:

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Если при попытке установить Питон вы получите ошибку в духе `bash: pyenv: command not found`, то нужно выполнить првую из команд, предлагаемых pyenv'ом, где задается PATH.

- Установите нужную версию питона
```bash
pyenv install 3.9.7
```
Если при установке возникают ошибки, то поставьте нужные пакеты в зависимости от вашего дистрибутива,
следуя [этой инструкции](https://github.com/pyenv/pyenv/wiki/Common-build-problems).
(Если под WSL не находится `llvm`, то можно взять `llvm-6.0-runtime llvm-6.0-dev`)

- Разверните виртуальное окружение с нужной версией питона в репозитории с задачами
```bash
cd <путь к склонированному репозиторию с задачами>
~/.pyenv/versions/3.9.7/bin/python -m venv mkn_env
```

- Активируйте виртуальное окружение (будет активным, пока не закроете консоль, либо не выполните `deactivate`)
```bash
source mkn_env/bin/activate
```

- Поставьте пакеты:
    * pytest для тестирования
    * flake8 для проверки на кодстайл
    * mypy для проверки типов
    * другие пакеты для задачек
```bash
# файл requirements.txt лежит в корне репозитория с задачками
(mkn_env)$ pip install --upgrade -r requirements.txt
```

- Проверьте версии:
```bash
(mkn_env)$ python --version
Python 3.9.7
(mkn_env)$ pytest --version
pytest 6.2.5
(mkn_env)$ flake8 --version
3.9.2 (mccabe: 0.6.1, pycodestyle: 2.7.0, pyflakes: 2.3.1) CPython 3.9.7 on Linux
(mkn_env)$ mypy --version
mypy 0.910
```

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/hYZFUE7.png" width=800/></details></br>

#### Установка и настройка IDE

Мы рекомендуем вам воспользоваться [PyCharm](https://www.jetbrains.com/pycharm/download/).
Скачайте бесплатную Community-версию, установите и запустите.

- Создайте новый проект (Create new project)
- Укажите путь до репозитория с задачами (см. пункт "Клонирование и настройка репозитория")
- Разверните меню "Project interpreter", выберите "Existing interpreter"
- Укажите путь до установленного интерпретатора: `<директория с задачками>/mkn_env/bin/python`
- Подтвердите создание проекта
- [Опционально] Далее, при попытке воспользоваться дебаггером может быть необходимо зайти в Settings > Tools > Python Integrated Tools и поменять там Default Test Runner на pytest. Тогда при нажатии правой кнопкой мыши на директорию с задачей должен появиться пункт Debug 'pytest in \<folder name\>'.

</details>

<details><summary><b>Настройка окружения в MacOS</b></summary>

#### Создание ssh-ключа

В консоли воспользуйтесь `ssh-keygen`, затем копируйте **.pub** ключ:

```bash
# Создаем ключ:
> ssh-keygen -t ed25519 -f ~/.ssh/manytask_ed25519
# Обратите внимание, что вы можете не указывать пароль для ключа,
# чтобы не приходилось его потом вводить на каждое действие c ключом
# Это стандартная практика, хотя и не очень безопасная

# Выводим содержимое **публичного** ключа в консоль:
> cat ~/.ssh/manytask_ed25519.pub
# Его надо просто скопировать, как есть, включая подпись - обычно это "ваш-логин@имя-устройства"
# ВАЖНО! Публичным ключом можно делиться, приватным (то же имя, без .pub на конце) - никогда,
# иначе злоумышленник сможет представиться вами
```

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/FMHgxsL.png" width=800/></details>

Идете на [gitlab.manytask.org](https://gitlab.manytask.org), находите в правом верхнем углу иконку с вашим профилем. Жмете на неё -> `Settings` -> слева жмете на `SSH keys`. Здесь вставляете ключ в формочку, жмете "Add key".
<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/CSPBoGp.png" width=800/></details>

Кроме этого, создайте ssh-config c таким содержимым, чтобы при подключении
к `gitlab.manytask.org` использовался ваш новый ключ:
```bash
> cat ~/.ssh/config
Host gitlab.manytask.org
    IdentityFile ~/.ssh/manytask_ed25519
```
Создать файл можно с помощью редактора `nano`, если он установлен
```bash
> nano ~/.ssh/config
```
затем нужно вставить в файл содержимое и нажать ctrl + O для сохранения и ctrl + X для выхода из редактора.

Либо с помощью команды
```bash
echo $'Host gitlab.manytask.org\n\tIdentityFile ~/.ssh/manytask_ed25519' > ~/.ssh/config
```

<details><summary><a>Полный процесс в консоли</a></summary><img src="https://i.imgur.com/LR6oDYQ.png" width=800/></details>

<details><summary><a>Как проверить себя?</a></summary>

Из консоли выполнить:
```bash
> ssh git@gitlab.manytask.org
```

Вывод должен быть примерно таким:
```
PTY allocation request failed on channel 0
Welcome to GitLab, @hiverus!
Connection to gitlab.manytask.org closed.
```

</details>

Если что-то не получилось — обращайтесь в чатик.

#### Установка git

О том, что такое гит, и как вообще с ним и с Питоном работать, мы рассказывали во [втором семинаре 2021 года](https://tinyurl.com/PythonGit).
```bash
# Пакеты стараемся ставить через brew — https://brew.sh
> brew install git
```

#### Клонирование и настройка репозитория

```bash
# Заходим в домашнюю директорию, где разместится репозиторий с задачами
> cd /Users/`whoami`

# Клонируем себе репозиторий с задачками
git clone git@gitlab.manytask.org:spbu-math-cs-python/spring-2022.git

# Переходим в директорию с задачами
cd spring-2022
# Настраиваем гит так, чтобы он знал нас "в лицо"
git config --local user.name "<ваш логин с python-math-cs.compscicenter.ru>"
git config --local user.email "<ваш емейл с python-math-cs.compscicenter.ru>"

# Указываем, что отправлять решения нужно в ВАШ репозиторий на gitlab.manytask.org
git remote set-url --push origin git@gitlab.manytask.org:spbu-python-spring-2022/<ваш репозиторий>

# Например для логина sidor:
git remote set-url --push origin git@gitlab.manytask.org:spbu-math-cs-python/sidor

# Имя вашего репозитория доступно по ссылке "MY REPO"
```

#### Установка интерпретатора и доппакетов

Мы используем версию питона 3.9.7

В консоли выполните:
```bash
# Устанаваливаем pyenv (менеджер версий питона)
> brew install pyenv

# Ставим нужную версию питона
> pyenv install 3.9.7
python-build: use openssl@1.1 from homebrew
python-build: use readline from homebrew
Installing Python-3.9.7...
python-build: use readline from homebrew
python-build: use zlib from xcode sdk
Installed Python-3.9.7 to /Users/ilariia/.pyenv/versions/3.9.7

# Устанаваливаем пакет для создания виртуального окужения
> brew install pyenv-virtualenv

# Создаем виртуальное окружение mkn_env с интерпретатором нужной версии
> pyenv virtualenv 3.9.7 mkn_env

# Ставим в виртуальное окружение пакеты, необходимые для курса
#   - mypy для проверки типов
#   - flake8 для проверки на кодстайл
#   - pytest для тестирования
#   - другие пакеты для задачек
> ~/.pyenv/versions/3.9.7/envs/mkn_env/bin/pip install --upgrade -r ~/<твой репозиторий>/requirements.txt

# Наш интерпретатор, который будем везде использовать
> ~/.pyenv/versions/3.9.7/envs/mkn_env/bin/python
Python 3.9.7 (default, Sep  2 2020, 19:52:21)
>>>

```

<details><summary><b>Apple silicon (!)</b></summary>
Если у вас устройство на `apple silicon m1`, то... удачи вам :3  
Мы НЕ гарантируем и не обещаем поддержку всего курса на такой архитектуре, но вы можете попробовать.

Вот один из способов установить необходимые пакеты —
Выполняем инструкцию выше, но вместо `pip install --upgrade` делаем следующее
```bash
# Устанавливаем компиляторы
> brew install openblas gfortran
> export OPENBLAS="$(brew --prefix openblas)"
# Отдельно ставим биндинговые пакеты
> pip install cython pybind11 pythran
# Ставим llvm, который нужен некоторым отдельным пакетам
> brew install llvm@11
> export LLVM_CONFIG="/opt/homebrew/Cellar/llvm@11/11.1.0_2/bin/llvm-config"

# Ставим отдельно llvmlite
> pip install llvmlite
# Самое весёлое - пробуем собрать себе капризные библиотеки (это может занять время)
> pip install --no-binary :all: --no-use-pep517 numpy==1.20.2
> pip install --no-binary :all: --no-use-pep517 scipy==1.7.1
> pip install --no-binary :all: --no-use-pep517 pandas==1.3.1

# Ну а теперь ставим всё остальное и молимся чтоб не упало
> pip install -r requirements.txt

>>>
```
(Проверьте, что тут версии такие же как и в `requirements.txt`)
</details>

#### Установка и настройка IDE

Мы рекомендуем вам воспользоваться [PyCharm](https://www.jetbrains.com/pycharm/download/).
Скачайте бесплатную Community-версию, установите и запустите.

- Создайте новый проект (Create new project)
- Укажите путь до репозитория с задачами (см. пункт "Клонирование и настройка репозитория")
- Разверните меню "Project interpreter", выберите "Existing interpreter"
- Пропишите путь к установленному интерпретатору
```bash
~/.pyenv/versions/3.9.7/envs/mkn_env/bin/python
```
- Подтвердите создание проекта

</details>
<details><summary><b>Настройка окружения в Windows</b></summary>

В Windows 10 появилась такая фича как WSL: Windows Subsystem for Linux,
с её помощью можно запускать Linux-приложения на Windows.
Мы рекомендуем воспользоваться ею, и в дальнейшем следовать инструкциям,
как будто бы у вас стоит операционная система Linux.

#### Как настроить WSL?
Оффициальная инструкция: https://docs.microsoft.com/ru-ru/windows/wsl/install-win10

Неоффициальная (с мышкой): https://www.windowscentral.com/install-windows-subsystem-linux-windows-10

При выборе операционной системы Linux берите Ubuntu.

Запустите установленную систему. При входе вы окажетесь в директории `/home/<username>`;
для того, чтобы иметь возможность работать с кодом из самой Windows (например, в PyCharm),
мы рекомендуем размещать директорию с задачами по адресу `"/mnt/c/Users/<username>/My Documents"`,
которая в самой Windows доступна по адресу `C:\Users\<username>\My Documents`.

Перейдите в указанную директорию:
```bash
cd "/mnt/c/Users/<username>/My Documents"
```
Переходите к инструкции про Linux.

</details>

<details><summary><b>Сдача заданий</b></summary>

### Получаем новые задания
Для получения новых заданий надо делать `git pull`. Для локального тестирования кода используется библиотека `pytest` (см. выше установку).

### Решаем задачу
Код относящийся к отдельной задаче находится в отдельной директории (`hello_world` и т.д.), нас будет интересовать её содержимое:
- условие задачи содержится в файле `README.md`
- заготовка в кодом задачи обычно лежит в файле с именем задачи `hello_world.py`
- публичные тесты к задаче находятся в файле `test_public.py`

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/61R3a4q.png" width=800/></details>

Вам нужно дописать код в файл с именем задачи.

### Проверяем себя
Все действия нужно производить из консоли, аналогично тому, как вы ставили нужную версию питона

<details><summary><a>Linux/Windows</a></summary>

```bash
# Переходим в задачу
$ cd hello_world
# Пишем код в файле hello_world.py, реализовывая заданный интерфейс

$ source mkn_env/bin/activate   # активируем виртуальное окружение, если не активировано
(mkn_env)$ pytest hello_world/  # запуск тестов
(mkn_env)$ flake8 hello_world/  # запуск линтера и stylecheck'а
(mkn_env)$ pycodestyle hello_world/
(mkn_env)$ mypy hello_world/    # запуск typecheck'а
```
</details>

<details><summary><a>MacOS</a></summary>

```bash
> ~/.pyenv/versions/3.9.7/envs/shad_env/bin/pytest 01.1.PythonTools/hello_world/  # запуск тестов
> ~/.pyenv/versions/3.9.7/envs/shad_env/bin/flake8 01.1.PythonTools/hello_world/  # запуск линтера и stylecheck'а
> ~/.pyenv/versions/3.9.7/envs/shad_env/bin/mypy 01.1.PythonTools/hello_world/    # запуск typecheck'а
```

NB: Заметьте, что запуск происходит из **корня проекта**. Если хочется запускать из папки с задачей, то нужно **указать путь** до `setup.cfg` как аргумент для `pytest`/`flake8`/`mypy`.
</details>

<details><summary><a>PyCharm</a></summary>

Если вы хотите проверить себя и не заходить в консоль, можно обойтись и PyCharm'ом.
Чтобы проверить pytest, можно нажать правой кнопкой на директорию с задачей и выбрать "pytest in ...".

После запуска pytest появится отдельное меню Run в котором будет список запускаемых тестов.
Любой из них можно запустить/продебажить нажав правой кнопкой мыши на него.

NB: В PyCharm можно настроить автоматический запуск `pytest`/`flake8`/`mypy` по кнопке тестирования, предоставляем вам возможность настроить это под себя.

</details>


### Отправляем задачу в тестирующую систему
```bash
git add hello_world/hello_world.py
git commit -m 'Add hello world task'
git push origin master
```

Вы можете наблюдать за результатами тестирования на странице `CI/CD -> Jobs` в своём репозитории, выбираем задачу, жмем на иконку статуса.

Там можно увидеть статусы посылок и результаты тестирования.

Выглядит это обычно так:
- Информация о последнем коммите
- Тестируемая задача (может быть несколько в одном коммите)
- Проверка стиля (PEP8)
- Проверка типов (type hints)
- Поиск тестов
- Запуск тестов и их результат

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/mgMXP1z.png" width=800/></details>

Каждая задача в рамках одной посылки проверяется отдельно,
и может быть засчитана отдельно в случае успешного прогона тестов.

Однако если хотя бы одна задача падает на тестах,
в интерфейсе гитлаба запуск будет считаться неудавшимся (failed).
Это нужно, чтобы понимать, когда нужно идти читать логи, а когда всё хорошо.
</details>


<details><summary><b>'У меня всё сломалось!'</b></summary>
В первую очередь стоит самостоятельно попробовать разобраться в причинах ошибки. Самые рабочие варианты:  

* 'метод пристального взгляда'
* google
* `FAQ.md`

(в файле `FAQ.md` содержатся решения для самых частых проблем)

Если же вышеописанные методы не помогают - чатик ждёт вашего вопроса!

-А что делать если вообще всё получается?  
-Отвечать на вопросы в чатике! Это очень ценно!   
</details>

## Лекции

<details><summary><b>Как открыть ноутбук с лекцией?</b></summary>

После того, как вы настроили окружение
по [инструкции](https://gitlab.manytask.org/spbu-math-cs-python/spring-2022/blob/master/README.md):

```bash
# Устанавливаем jupyter
~$ ~/.pyenv/versions/3.9.7/envs/mkn_env/bin/pip install jupyter==1.0.0

# Запускаем jupyter
$ ~/.pyenv/versions/3.9.7/envs/mkn_env/bin/jupyter notebook
```
</details>

<details><summary><b>Как запустить лекцию в режиме презентации?</b></summary>

```bash
# Устанавливаем RISE
~$ ~/.pyenv/versions/3.9.7/envs/mkn_env/bin/pip install rise==5.6.1
```

В jupyter notebook появится кнопка "Enter/Exit RISE Slideshow"

</details>

<details><summary><b>Как подключить cell-typeсhecker?</b></summary>

```python
from IPython.core.magic import register_cell_magic


@register_cell_magic
def typecheck(line, cell):

    from mypy import api
    cell = '\n' + cell

    mypy_result = api.run(['-c', cell] + line.split())

    if mypy_result[0]:  # print mypy stdout
        print(mypy_result[0])

    if mypy_result[1]:  # print mypy stderr
        print(mypy_result[1])
```

```bash
# Дописываем код выше в файл typecheck.py
$ nano ~/.ipython/profile_default/startup/typecheck.py

# Перезапускаем jupyter
~/.pyenv/versions/3.9.7/envs/mkn_env/bin/jupyter notebook
```

Для проверки типов добавить строчку `%%typecheck` в тестируемой ячейке.  
Для применения `mypy` ко всем запускаемым ячейкам можно использовать [Nb Mypy](https://pypi.org/project/nb-mypy/).
</details>
