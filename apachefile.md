### Changes to apache server configurations file

- Open the apache2 server 000-default.conf file

```sh
$ sudo nano /etc/apache2/sites-available/000-default.conf
```
- Paste the following code 
<pre>
> <VirtualHost *:80> <br/>
> ServerAdmin webmaster@example.com<br/>
> DocumentRoot /home/ubuntu/django/myproject<br/>
> ErrorLog ${APACHE_LOG_DIR}/error.log<br/>
> CustomLog ${APACHE_LOG_DIR}/access.log combined<br/>
> Alias /static /home/ubuntu/django/myproject/static<br/>
> <Directory /home/ubuntu/django/myproject/static><br/>
> Require all granted<br/>
> </Directory><br/>
> <Directory /home/ubuntu/django/myproject/myproject><br/>
> <Files wsgi.py><br/>
> Require all granted<br/>
> </Files><br/>
> </Directory><br/>
> WSGIDaemonProcess myproject python-path=/home/ubuntu/django/myproject python-home=/home/ubuntu/django/myprojectenv<br/>
> WSGIProcessGroup myproject<br/>
> WSGIScriptAlias / /home/ubuntu/django/myproject/myproject/wsgi.py<br/>
> </VirtualHost><br/>
</pre>

- Save the file and execute the following command

```sh
$ sudo service apache2 restart
```

- Now visit the website at 
[https://*ip or dns name*:80/]
