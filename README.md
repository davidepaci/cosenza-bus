web app to query cosenza bus routes

time taken to complete: within 1 day

see live at https://cosenza-bus.onrender.com/

# data
this folder gets data from tables within a pdf, fixes them and saves them to sqlite (_python, pandas, pdfplumber, sqlite_)

# app
simple web app (_node, sql, tailwind, js_)

<img width="554" alt="image" src="https://github.com/user-attachments/assets/8a79e4cb-11f9-4156-9096-8965732e2429">

design with https://www.usegalileo.ai/

# issues
- imperfect db (needs to be checked for random 00:00 values in stops)
- issues with night routes (a 00:06 stop is listed before a 23:52 stop, logically)
- not showing routes in the correct period
- no option to choose custom date and time to check
- svgs loading too slowly?
- serverless hosting/static website generation are perhaps ideal?
