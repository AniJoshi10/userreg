### Changes to apache server configurations file

- Open the apache2 server 000-default.conf file

```sh
$ sudo nano /etc/apache2/sites-available/000-default.conf
```
- Paste the following code 

> <VirtualHost *:80> 
> ServerAdmin webmaster@example.com
> DocumentRoot /home/ubuntu/django/myproject
> ErrorLog ${APACHE_LOG_DIR}/error.log
> CustomLog ${APACHE_LOG_DIR}/access.log combined
> Alias /static /home/ubuntu/django/myproject/static
> <Directory /home/ubuntu/django/myproject/static>
> Require all granted
> </Directory>
> <Directory /home/ubuntu/django/myproject/myproject>
> <Files wsgi.py>
> Require all granted
> </Files>
> </Directory>
> WSGIDaemonProcess myproject python-path=/home/ubuntu/django/myproject python-home=/home/ubuntu/django/myprojectenv
> WSGIProcessGroup myproject
> WSGIScriptAlias / /home/ubuntu/django/myproject/myproject/wsgi.py
> </VirtualHost>

- Save the file and execute the following command

```sh
$ sudo service apache2 restart
```

- Now visit the website at 
[https://<ip or dns name>:80/]
