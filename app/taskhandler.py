# -*- coding:utf-8 -*-
from app import celery
from flask import current_app
from origins import *
from sendemail import sendto_kindle
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

workdir = 'app/data/mobiworkshop/'
@celery.task
def hardtask(kindle_loc,origin,bookid,bookname):

    if origin == u'起点':
        task = QidianFree(bookid,bookname)
    elif origin == u'红袖':
        task = HongxiuFree(bookid,bookname)
    elif origin == u'17K':
        task = Seventeenfree(bookid,bookname)
    elif origin == u'纵横':
        task = Zonghengfree(bookid,bookname)
    else:
        task = ''
    task.get_info()
    task.generate_txt()
    bname = origin+'_'+bookname
    #几行命令行指令，生成epub，再生成mobi，然后删除txt和epub文件，最后发送至kindle邮箱。
    subprocess.call('pandoc %s%s.txt -o %s%s.epub'%(workdir,bname,workdir,bname),shell=True)
    subprocess.call('rm %s%s.md'%(workdir,bname),shell=True)
    subprocess.call('%skindlegen -c2 %s%s.epub'%(workdir,workdir,bname),shell=True)
    subprocess.call('rm %s%s.epub'%(workdir,bname),shell=True)
    sendto_kindle(kindle_loc,bname)

    return {'status': 'Task completed!'}

