import poplib
import email # new statement
import re
import os
from subprocess import call

DOWNLOAD_FORMAT = os.path.join(
    os.path.expanduser('~'),
    "Videos/YouTubeInbox/%(title)s.%(ext)s"
)

EMAIL_HOST = ''
EMAIL_USER_NAME = ''
EMAIL_PASSWORD = ''

mail = poplib.POP3_SSL(EMAIL_HOST)
print(mail.getwelcome())
print(mail.user(EMAIL_USER_NAME))
print(mail.pass_(EMAIL_PASSWORD))
print(mail.stat())
print(mail.list())

if mail.stat()[1] > 0:
    print("You have new mail.")
else:
    print("No new mail.")


numMessages = len(mail.list()[1])
for i in range(numMessages):
    for j in mail.retr(i+1)[1]:
        msg = email.message_from_string(str(j, 'utf-8'))
        payload = msg.get_payload()
        url = re.search("(?P<url>https?://[^\s'\"]+)", payload)
        if url is not None:
            vurl = url.group("url")
            print(vurl)
            print("Downloading to: ", DOWNLOAD_FORMAT)
            call(["youtube-dl", "--max-downloads","1", "-o", DOWNLOAD_FORMAT, vurl])
            mail.dele(i+1)[1]

mail.quit()
