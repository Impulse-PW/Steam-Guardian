# Steam-Guardian
<h3><b>Steam Guard with trade and phishing protection. For Windows, Mac and Linux</b></h3>

<b>Written for Python 3 (Under Development)</b>

When finished Steam Guardian will include functionality to encrypt your Steam Guard secrets with a password and cryptProtectData API, warn about trade offers from steamrep banned accounts, detect trade changes such as wear switching scams, show you the prices and totals of offers, and trading in general will prompt the user with tips and advice to avoid being scammed.

Item stealing protection is possible as well. If Steam Guard secrets are stolen and someone attempts to send your items elsewhere, Steam Guardian will see a gift being sent to another user in your confirmations. Since this action was not triggered by Steam Guardian, the software will cancel the trade and alert you of what happened. Automatic password reset might also be possible, I'm currently investigating an implementation.

<b>Current features:</b>
===================

Adding Steam Guard<br>
Removing Steam Guard<br>
Generating / copying 2FA codes<br>
Switching between accounts<br>
Viewing revocation code(s)<br>

![Steam Guardian Screenshot](https://image.prntscr.com/image/UtzNGoHbRnyVU58KrsDLmQ.png)

<b>To run Steam Guardian from source code (Linux):</b>
===============================================

```
git clone https://github.com/Impulse-PW/Steam-Guardian && cd Steam-Guardian
sudo apt-get install python3-tk
pip3 install -r requirements.txt
cd project
python3 __main__.py
```

<b>setup.py</b> and <b>binaries</b> coming later at project's conclusion.

<b>Like Steam Guardian?</b>
======================

<a href='https://ko-fi.com/M4M4LOV3' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://az743702.vo.msecnd.net/cdn/kofi4.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
