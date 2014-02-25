# -*- coding: utf-8 -*-
import os, time, webbrowser, urllib, json, threading
from string import Template

template = '''<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body onload="Button1.click()">
<form name="form1" method="post" action="xxx" id="form1">[<input type="hidden" name="__LASTFOCUS" id="__LASTFOCUS" value="" />
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
        self.save_filename = username + '_' + str(time.time()) + '.html'


    def action(self):
        cur_time = time.time()
        if cur_time > self.punch_time:
            file = open(self.save_filename, 'w')
            file.write(self.save_content)
            file.close()
            webbrowser.open_new_tab(self.save_filename)
            print "executed:", self.username, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.punch_time))
            return True
        return False

class Timer(threading.Thread):
    def __init__(self, num, interval, username, password, punch_time):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.username = username
        self.password = password
        self.punch_time = punch_time
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            user = User(self.username, self.password, self.punch_time)
            if user.action() == True:
                self.thread_stop = True
            time.sleep(self.interval)

    def stop(self):
        self.thread_stop = True

if __name__ == "__main__":
    tasks = []
    interval = 60
    while True:
        time.sleep(interval)
        task = urllib.urlopen("http://punch360.sinaapp.com/task").read()
        if len(task) > 0:
            parse_task = json.loads(task)
            tasks.append(parse_task)
            print tasks[0]["username"], tasks[0]["password"], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(tasks[0]["trigger"])))
            Timer(1, 3, tasks[0]["username"], tasks[0]["password"], float(tasks[0]["trigger"])).start()
            tasks.remove(tasks[0])
