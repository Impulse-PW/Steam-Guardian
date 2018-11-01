# Steam-Guardian
<h3><b>Steam Guard with trade and phishing protection. For Windows, Mac and Linux</b></h3>

<b>Written for Python 3</b>

When finished Steam Guardian will include functionality to encrypt your Steam Guard secrets with a password and cryptProtectData API, warn about trade offers from steamrep banned accounts, detect trade changes such as wear switching scams, show you the prices and totals of offers, and trading in general will prompt the user with tips and advice to avoid being scammed.

Item stealing protection is possible as well, if Steam Guard secrets are stolen and someone attempts to send your items elsewhere Steam Guardian will see a gift being sent to another user in your confirmations. Since this action was not triggered by Steam Guardian, the software will change your password, cancel the trade and alert you of what happened. Yes an attacker can change your password by stealing your Steam Guard secrets, however, if the attacker changes your password Steam will trade ban your account giving you the opportunity to get your account back before losing your items. Therefore, changing your password isn't in the attackers best interest.

<b>Current features:</b>

Adding Steam Guard<br>
Removing Steam Guard<br>
Generating / copying 2FA codes<br>
Switching between accounts<br>
Viewing revocation code(s)<br>

<b>To run you will need the following dependencies:</b>

gevent<br>
pyperclip<br>
pillow<br>
sqlite3<br>
steam<br>
steampy<br>
ttk
