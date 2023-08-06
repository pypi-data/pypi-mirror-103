# Kindle ebook tools

## Setup

    [root@localhost ~]# cd /usr/local/src/

    [root@localhost src]# git clone https://github.com/netkiller/kindle.git

    [root@localhost src]# cd kindle/

    [root@localhost kindle]# python3 setup.py sdist install 

    [root@localhost kindle]# kindle -h
    Usage: kindle [option] example@kindle.cn

    Kindle book push

    Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -p /var/book/, --path=/var/book/
                            The path of library
    -f, --force           force sendmail
    -b /path/to/book.mobi, --book=/path/to/book.mobi
                            book path
    -g {kindle|phone|ipad|email|other}, --group={kindle|phone|ipad|email|other}
                            User group
    -a, --all             Push all of books to friends
    -n, --netkiller       Push books to mine<netkiller@kindle.cn>
    -e {mobi|pdf}, --ext={mobi|pdf}
                            file extention name, default: .mobi
    -d, --debug           debug mode

    Database:
        -l, --library       list library
        -u, --user          list kindle users
        -s, --bibliography  list the user's bibliography

    Advanced:
        --smtp=SMTP         smtp server default: msn
        --size=40           file size (MB)
        -k, --azw3          azw3 file first
        -o 10, --offset=10  Index offset number
        -D 2019-01-01, --date=2019-01-01
                            from date

## SMTP

    neo@MacBook-Pro-Neo ~/git/kindle % cat ~/.kindle/smtp.ini        

    [default]
    smtp=smtp-mail.outlook.com:587
    username=netkiller@msn.com
    password=
    tls=True

## Manual

    [root@localhost kindle]# kindle -a netkiller@msn.com
    SEND: netkiller@msn.com => Book/Netkiller-Architect.mobi (2.98 MB)