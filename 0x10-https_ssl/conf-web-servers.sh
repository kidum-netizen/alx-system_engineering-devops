#!/usr/bin/env bash
# install fabric

# "Install Nginx"
if ! command -v nginx > /dev/null; then
	sudo apt-get update
	sudo apt-get install nginx -y
fi

index="<html> <body> Hello World! Holberton School </body> </html>"
notfound_page="<html> <body>Ceci n'est pas une page</body> </html>"
notfound=/usr/share/nginx/html/notfound.html
default=/etc/nginx/sites-enabled/default
# Replace the whole contents of "/etc/nginx/sites-enabled/default" with below
contents=$(cat <<END
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html;
	server_name anexe.tech www.anexe.tech;
	add_header  X-Served-By  "$HOSTNAME";

	rewrite ^/redirect_me/?$ https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;

	location /hbnb_static {
		alias /data/web_static/current;
		index index.html 0-index.html;
	}

	error_page 404 /notfound.html;
	location = /notfound.html {
		root /usr/share/nginx/html; # Default but just being explicit
		internal;
	}
}

END
)


# "Create vital folders if not exists"
[ -d /data/web_static/releases/test/ ] || mkdir -p /data/web_static/releases/test/
[ -d /data/web_static/shared/ ] || mkdir /data/web_static/shared/
echo "It works!" > /data/web_static/releases/test/index.html

# "Important symbolic links"
[ -e /data/web_static/current ] && rm /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

mkdir -p /var/www/html
mkdir -p /usr/share/nginx/html
echo "$index" | tee /var/www/html/index.html > /dev/null
echo "$notfound_page" | tee "$notfound" > /dev/null

echo "$contents" | tee "$default" > /dev/null
# nginx -t
service nginx restart # or nginx -s reload for uninterrupted silent reload of config
