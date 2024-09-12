# College Cutoff
 
## Summary
A user friendly app to easily see colleges and the cut-off marks required to enter them. Intended for students writing college entrance exams. Similar to JOSAA but covers multiple colleges in one place. The csv files contain some dummy data as of now but can easily be updated.

## How to run
- Download MySQL and set up a username and password. Enter that in main.py line 10.
- Download tkinter library
  ```
  pip install tkinter
  ```
- Download the 5 csv files from the repository. Customize the entries as per your choice. For now we have only top few colleges under IIT, IIIT, NIT and BITS. The cut-offs are also dummy values and not accurate. Please refer to official websites and update as needed.

## Features
- Guest profile
 - Find college
   - By type (IIT, NIT, BITS, IIIT)
   - By place (Bombay, Madras, Surathkal)
 - Search cut-offs
  - Based on college name, branch, gender and category.
 - College info (includes details like the college website, entrance exam registration dates, contact details, etc. )
   
- Admin profile
   - See all tables in the database, update their contents, add and delete entries.
     
## Pictures


## Tech Stack 
- Frontend : Tkinter library in python
- Backend : MySQL
