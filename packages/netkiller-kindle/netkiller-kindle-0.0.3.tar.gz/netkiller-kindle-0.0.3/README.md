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

## 配置 SMTP

    neo@MacBook-Pro-Neo ~/git/kindle % cat ~/.kindle/smtp.ini        
    [default]
    smtp=smtp-mail.outlook.com:587
    username=netkiller@msn.com
    password=
    tls=True
## 准备电子书

    在当前目录下创建一个 Book 目录，将后缀为 .mobi 的电子书复制进去。
    [root@localhost ~]# ls -1 Book/
    Netkiller-Architect.mobi
    Netkiller-Blockchain.mobi
    Netkiller-Docbook.mobi
    Netkiller-Java-Spring.mobi
    Netkiller-Java.mobi
    Netkiller-Linux.mobi
    Netkiller-Management.mobi

## Manual

    [root@localhost kindle]# kindle -a netkiller@msn.com
    SEND: netkiller@msn.com => Book/Netkiller-Architect.mobi (2.98 MB)

    [root@localhost ~]# kindle netkiller@kindle.cn
    SEND: netkiller@kindle.cn => Book/Netkiller-Architect.mobi (2.98 MB)

    指定电子书推送使用 -b 参数
    [root@localhost ~]# kindle -b Book/Netkiller-Architect.mobi netkiller@kindle.cn

    强制推送，当推送失败，用户没有接受到，再次推送就需要使用 -f 参数。
    [root@localhost ~]# kindle -f -b Book/Netkiller-Architect.mobi netkiller@kindle.cn    

### 查看书库

    [root@localhost ~]# kindle -l
    1	2021-04-28 16:08:17	3124624(2.98 MB)	/Netkiller-Architect.mobi
    2	2021-04-28 16:08:17	9464863(9.03 MB)	/Netkiller-Blockchain.mobi
    3	2021-04-28 16:08:17	421122(411.25 KB)	/Netkiller-Docbook.mobi
    4	2021-04-28 16:08:17	952569(930.24 KB)	/Netkiller-Java-Spring.mobi
    5	2021-04-28 16:08:17	2212841(2.11 MB)	/Netkiller-Java.mobi
    6	2021-04-28 16:08:17	15817932(15.09 MB)	/Netkiller-Linux.mobi
    7	2021-04-28 16:08:17	1120324(1.07 MB)	/Netkiller-Management.mobi

### SMTP

    [default]
    smtp=smtp-mail.outlook.com:587
    username=netkiller@msn.com
    password=
    tls=True

    [msn]
    smtp=smtp-mail.outlook.com:587
    username=netkiller@msn.com
    password=
    tls=True

    [163]
    smtp=smtp.163.com
    username=openx@163.com
    password=
    tls=False

    [openunix]
    smtp=smtp.163.com
    username=openunix@163.com
    password=
    tls=

    [local]
    smtp=localhost
    username=netkiller@msn.com
    password=
    tls=

    [postfix]
    smtp=192.168.3.5
    username=netkiller@msn.com
    password=
    tls=False

    [root@localhost kindle]# kindle -a netkiller@msn.com --smtp=163

### 分组管理

    分组可以将用户归类管理，例如不同兴趣，不同专业，为他们单独建立分组

    计算机组
    [root@localhost ~]# kindle -g computer netkiller@kindle.cn
    SEND: netkiller@kindle.cn => Book/Netkiller-Architect.mobi (2.98 MB)
    文学组
    [root@localhost ~]# kindle -g literary tom@kindle.cn
    哲学组
    [root@localhost ~]# kindle -g philosophy jerry@kindle.cn