
how communication between devices can be achieved?

Use http, avoid ftp/sftp/scp/rsync/smb/mail
Use http for data transfer. Avoid the old ways
(ftp/sftp/scp/rsync/smb/mail).
If you want to transfer files via HTTP from shell/cron you can use:
[tbzuploader](https://github.com/guettli/tbzuploader).
The next step is to avoid clever
[inotify](https://en.wikipedia.org/wiki/Inotify)-daemons. You don't need
this anymore if you receive your data via HTTP.
Why is HTTP better? Because HTTP can validate the data. If it is not
valid, the data can be rejected.
