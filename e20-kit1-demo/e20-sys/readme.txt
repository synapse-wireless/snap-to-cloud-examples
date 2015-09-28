This directory contains files needed to enable demo on the E20.
(see E20 User Guide for details of these changes)

------------------------------------------------------------
Files changed/added to enable Wifi AP mode
  Note: ssid="synapse-e20", password="synapse1"
------------------------------------------------------------

/etc/network/interfaces

/etc/rc2.d/S10wifiAP

NOTE! - make sureS10wifiAP is executable, or it won't have any effect.
(ex. chmod 777 /etc/rc2.d/S10wifiAP)


------------------------------------------------------------
File to start demo app at boot, as service
------------------------------------------------------------

/etc/init/e20-kit1-demo.conf

NOTE! - this file assumes/requires that directory tree e20-kit1-demo resides in /home/snap.
If you pulled the example souce code directly from github, you may need to move the files,
OR change the path to app_server.py in file e20-kit1-demo.conf.

