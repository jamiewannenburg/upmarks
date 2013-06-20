UPMarks
=======

Checks your marks at University of Pretoria and e-mails you and opens notepad when a new one comes out. 

If you are like me you can't relax until you know all our marks. The fact that Click-Up logs you out every ten minutes is very annoying in this regard. So this program automates the process and notifies you when something changes.

To download the latest version go to the folder “binaries/windows” and download the latest .zip file. Extract to a folder of your choice. Then run “get_marks.exe”. An e-mail wil be sent to your student number gmail address. And notepad wil open; displaying your marks. 

You can automate the process. First run the program "get_marks", so that the program can get your credentials. You can make a cron job in linux, which runs the get_marks.py file. On windows go to start->all programs->accessories->system tools->task scheduler then “create task”. Give it a name. Under the triggers tab, click new. Choose “daily” and under advanced check “repeat task every” and specify your schedule. Click “ok”. Under the actions tab click “new”. Then brows to your “get_marks.exe”. Click “ok” and again “ok”. After you refresh “Task Library” you should see your task. Now, so long as your computer is turned on you wil get notified (over email) as soos as your marks change.

If you need to change your credentials; delete the "tmp/.credentials" file and rerun the program.