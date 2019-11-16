#! /bin/sh

# If dontlog is found, the patch has already been applied
if grep dontlog /etc/httpd/conf/httpd.conf >/dev/null 2>&1; then
  echo "httpd.conf already patched"
  exit

else

  # Patch apache's conf

  # Don't log trafficstats.cgi or time-clock.cgi; no need to fill the logs
  #   with things that run this often.
  sed -i -e '/^ErrorLog/a\
SetEnvIf Request_URI "time-clock.cgi" dontlog\
SetEnvIf Request_URI "trafficstats.cgi" dontlog
s/\(CustomLog.*common$\)/\1 env=!dontlog/' /etc/httpd/conf/httpd.conf

  # The 'magic' file is not in default location.
  sed -i -e 's=share/magic=/etc/httpd/conf/magic=' \
      /etc/httpd/conf/httpd.conf

  echo "httpd.conf patched"

  # Restart apache
  killall /usr/sbin/httpd
  /usr/sbin/httpd -DSSL
  echo "httpd restarted"
fi
