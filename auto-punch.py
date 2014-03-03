# -*- coding: utf-8 -*-
import time, webbrowser, urllib, json, threading
from string import Template
from operator import itemgetter, attrgetter

template = '''<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body onload="Button1.click()">
<form name="form1" method="post" action="http://erp1.360buy.com/newhrm/kaoqing/frdakaji.aspx" id="form1">[<input type="hidden" name="__LASTFOCUS" id="__LASTFOCUS" value="" />
 <input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="/wEPDwULLTE1NTIwMTc0NDQPZBYCAgMPZBYEAgEPD2QWAh4Jb25rZXlkb3duBVtpZihldmVudC5rZXlDb2RlPT05IHx8IGV2ZW50LmtleUNvZGU9PTEzKXsgZG9jdW1lbnQuYWxsLnR4dF9QYXNzd29yZC5mb2N1cygpO3JldHVybiBmYWxzZTt9ZAIPDxYCHgRUZXh0ZWRkBOZ+U/f9usviT+OsIRO72gAAAAA=" />
 <input type="hidden" name="__EVENTTARGET" id="__EVENTTARGET" value="" /> <input type="hidden" name="__EVENTARGUMENT" id="__EVENTARGUMENT" value="" />
 <input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="/wEWBALLlZz2CgL3xJvhBAKM54rGBgLS9cL8AgdQXnNC6opMnjFsxIOPUFUAAAAA" />]<input name="txt_UserName" type="text" value="$u_name" id="txt_UserName"/>
 <input name="txt_Password" type="password" value="$p_wd" id="txt_Password"/><input type="submit" name="Button1" value="" id="Button1"/></form></body></html>'''

class User:
    def __init__(self, username, password, punch_time):
        self.username = username
        self.password = password
        self.punch_time = punch_time
        s = Template(template)
        self.save_content = s.substitute(u_name=self.username, p_wd=self.password)
        self.save_filename = username + '_' + time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(time.time())) + '.html'

    def action(self):
        file = open(self.save_filename, 'w')
        file.write(self.save_content)
        file.close()
        webbrowser.open_new_tab(self.save_filename)
        print "executed:", self.username, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.punch_time))

def sort_task(tasks):
    task_len = len(tasks)
    if task_len < 2:
        return tasks
    for i in range(task_len-1):
        for j in range(task_len-i-1):
            if tasks[j]['trigger'] > tasks[j+1]['trigger']:
                tasks[j], tasks[j+1] = tasks[j+1], tasks[j]
    return tasks

if __name__ == "__main__":
    tasks = []
    interval = 60
    while True:
        time.sleep(interval)
        task = urllib.urlopen("http://punch360.sinaapp.com/task").read()
        if len(task) > 0 and task.index("username") > 0:
            try:
                parse_task = json.loads(task)
            except ValueError:
                print "taskerror:" + task
            else:
                tasks.append(parse_task)
                tasks = sort_task(tasks)
                print parse_task["username"], parse_task["password"], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(parse_task["trigger"])))
        if len(tasks) > 0 and time.time() > float(tasks[0]["trigger"]):
            user = User(tasks[0]["username"], tasks[0]["password"], float(tasks[0]["trigger"]))
            user.action()
            tasks.remove(tasks[0])
