<h1>Ticket Bot 58</h1>
<h2>1. Клонирование</h2>

git clone `https://github.com/Alyrineee/ticket_bot.githttps://github.com/Alyrineee/ticket_bot.git`

<h2>2. Создание venv</h2>

* Создайте виртуальное окружение `python3 -m venv venv`
* Активируйте его `source venv/bin/activate`

<h2>3. Создание виртуального окружения</h2>

* Установите зависимости `pip3 install -r requirements.txt`

* Переименуйте файл `.env.template` на `.env`
 
* Измените `TOKEN` на **свой**

<h2>4. Создание daemon-а</h2>

* Создайте `sudo nano /lib/systemd/system/example_bot.service`

`example_bot.service` назовите так как удобно

* Напишите вот этот код
    ```
    [Unit]
    Description=Example - Telegram Bot \\ можете указать название своего бота
    
    After=syslog.target 
    After=network.target
    [Service] 
    Type=simple 
    WorkingDirectory=/home/имя_папки/
    ExecStart=/usr/bin/python3 /home/имя_папки/имя_файла.py \\ Здесь и выше укажите названия, которые установили для директории и файла с ботом.
    
    RestartSec=60 
    Restart=always
    [Install] 
    WantedBy=multi-user.target
    ```
    
* Запуск daemon-a  
    ```
    sudo systemctl enable example_bot
    sudo systemctl start example_bot
    ```
    
<h2>5. Запуск бота🚀</h2>

`python3 имя_файла.ру`
