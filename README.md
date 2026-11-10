# cyber_security_project
this is a simple application demonstrating 5 security threats from OWASP top then list in 2021 and their solutions

Simple installation instructions (you may as well create a virtual environment if wish so)
git clone https://github.com/susulmtnn/cyber_security_project.git
cd cyber_security_project/diary
python3 manage.py migrate
python3 manage.py runserver

-------------------------------------------------------------------------------

Introduction to Cyber Security: MOOC 2026 

Course report 

 

Introduction 

This course project has been completed as part of the University of Helsinki’s course Introdution to Cyber Security. The project is the last part of the course and it includes the report and the code for a software project. 

The objectif of this report is to demonstrate the following 5 security threats listed in OWASP top ten list in 2021: (1) Broken Access Control, (2) Cryptographic Failures, (3) Injection, (4) Identification and Authentication Failures, (5) Security Logging and Monitoring Failures 

These threats are demonstrated in a small software project, which is a “Gossip girl diary”. In the diary, the user can log in to read the “Gossips”. They can also comment on the gossips and view their own comments. The special feature is, that to read the “Secret gossips”, user needs the secret password that they can only acquire personally from the famous Gossip Girl. 

---------------------------------------------------------------------------------------------------------- 

LINK: https://github.com/susulmtnn/cyber_security_project 
installation instructions 

Requirements: python, django 

git clone https://github.com/susulmtnn/cyber_security_project.git 

cd cyber_security_project 

cd diary 

python3 manage.py runserver 

Ps. Users alice (password: redqueen) and bob (password: squarepants) from the exercises are automatically created 

 

FLAW 1: BROKEN ACCESS CONTROL 
exact source link pinpointing flaw1: 

https://github.com/susulmtnn/cyber_security_project/blob/4d1a79366526c52741a27b848e2501e9dcc19321/diary/gossip_app/views.py#L99 

 
description of flaw 1: 

The flaw is a classic case of a broken access control, where a user can view other user’s data just by editing the url. In this case, the user is logged in as “bob” but can view the gossips that “new_user” has posted (as you can see in the flaw-1-before-1.png (check screenshots folder in the root of this project).  

Exact source link pinpoiting fix 1:  

https://github.com/susulmtnn/cyber_security_project/blob/4d1a79366526c52741a27b848e2501e9dcc19321/diary/gossip_app/views.py#L154 
how to fix it: as a fix, after the login we redirect to your_account.html but instead of using the username from the browser, we look it up from the User database table. The user sees their own gossips that are directly found to their account in the django User table by request.user. Even if you try to change the url, it will still show the gossips for the logged in user. Ideally, you would use a different path as well and only look the username up from the table, but since we use toggle the comments for this exercise, this solution still passes the username but ignores it and looks it up again. 
 
FLAW 2: CRYPTOGRAPHIC FAILURES 
exact source link pinpointing flaw 2.: 

https://github.com/susulmtnn/cyber_security_project/blob/d9fc273a024d26282cc7064fba38fcc82cc7a41a/diary/gossip_app/views.py#L16 
description of flaw 2: In the flaw 2, the password for the Very Secret Gossip space exists in the SecretPasword data table as plain text and it is “secret”. Also, the password is same to everyone. 

exact source link pinpointing fix of flaw 2... 

Exact source link pinpoiting fix 2: 

https://github.com/susulmtnn/cyber_security_project/blob/d9fc273a024d26282cc7064fba38fcc82cc7a41a/diary/gossip_app/views.py#L34 
how to fix it: Every user is asked to set their own secret password. The password is hashed by using django’s automatical hashing parameters and function make_password and only then stored to the database.  

FLAW 3: INJECTION 

exact source link pinpointing flaw 3: https://github.com/susulmtnn/cyber_security_project/blob/4d1a79366526c52741a27b848e2501e9dcc19321/diary/gossip_app/views.py#L74 
description of flaw 3: See the screenshots for flaw 3. The flaw 3 allows the user to post html to the gossip-text field. In the screenshot, Bob uses this flaw and makes a convincing new text box to the page where Gossip girl is asking the user to email their username and password to her. This is because all the input text in gossip is marked as “safe”. 

Exact source link pinpoiting fix for flaw 3: 

https://github.com/susulmtnn/cyber_security_project/blob/4d1a79366526c52741a27b848e2501e9dcc19321/diary/gossip_app/views.py#L79 
how to fix it: as a fix, it is enough to not to “mark” all text input as safe, then django will automatically make sure that nothing gets injected. You can just do this by commenting out the flaw 3. 

FLAW 4: IDENTIFICATION AND AUTHENTICATION 
exact source link pinpointing flaw 4: FAILURES https://github.com/susulmtnn/cyber_security_project/blob/4d1a79366526c52741a27b848e2501e9dcc19321/diary/secret_diary/settings.py#L30 

 
description of flaw 4: This flaw demonstrates what happens when the session cookies are not properly set up and remain in place for too long. Also, in this example, they do not expire even when the broser is closed. In the screenshots, you can see how the same user has been remaining logged in for a long time, which is a serious security risk. 

Exact source link pinpointing fix 4: https://github.com/susulmtnn/cyber_security_project/blob/4d1a79366526c52741a27b848e2501e9dcc19321/diary/secret_diary/settings.py#L37 
how to fix it: This can be easily fixed by imposing a set session, in this case for demonstration purposes the cookie age is set to 60 seconds. And the cookie will expire if the browser is closed.  
... 
 
FLAW 5: SECURITY LOGGING AND MONITORING FAILURES 
Exact source link pinpointing flaw 5: The flaw state is in place when the code does not have error logging. This is the case when the fix (5) is commented out. 
description of flaw 5: According to OWASP 2021, all the incorrect password attempts should be logged. In the beginning, logger is not used in the app. 

Exact source link pinpointing fix 5: https://github.com/susulmtnn/cyber_security_project/blob/4d1a79366526c52741a27b848e2501e9dcc19321/diary/gossip_app/views.py#L21-L22 

AND 

https://github.com/susulmtnn/cyber_security_project/blob/4d1a79366526c52741a27b848e2501e9dcc19321/diary/gossip_app/views.py#L40 

AND 

https://github.com/susulmtnn/cyber_security_project/blob/4d1a79366526c52741a27b848e2501e9dcc19321/diary/gossip_app/views.py#L12 
how to fix it:  

This flaw is fixed by using the Python library logging. Each time that some user tries to log in to the Secret Gossip space, the logger logs the event. Another even that is logged is when a user tries to change the url to view someone else’s your_account page and the list of gossips posted by that person. The screenshots demonstrate the logs in the shell. 