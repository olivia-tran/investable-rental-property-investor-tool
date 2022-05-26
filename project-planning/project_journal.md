PROJECT JOURNAL

WEEK 1

---

DATE: Monday 5/2

TO DO:
[X] Data model design
[X] Set up core view functions
[X] Name project
[X] Github repo

JOURNAL:
Today I created my data model and built relationships within my database. Decided to add images to the data model as well.

---

DATE: Tuesday 5/3

TO DO:

[X] Seed database (User, Property from Redfin CSV)
[X] Built basic calculator feature
[X] Simple app and logging function work

JOURNAL:
The calculator is working, plan to add a feature allowing user to save data to db. Had trouble accessing VSC remote, Instructor team came in to help. Had to work globally for now.

---

DATE: Wednesday 5/4

TO DO:
[X] Google API
[X] Fix logging route bug
[X] Add feature to calculator
[X] Update db

JOURNAL:
Today VSC is still not working. Working globally makes me hesitant to install more packages

---

DATE: Thursday 5/5

TO DO:
[X] Add profile page
[X] Debug and got the session pop once user log out
[X] Set up more templates

JOURNAL:
Worked a little bit on designing and read the docs to understand more about Flask while asking for help to fix my VSC

---

WEEK 1 SUMMARY:
Learning a lot about how to design a web app, thinking of the user flow and how that's translated to code. Decided on theme colors as completed building some basic functionalities for the app. Users can seamlessly log in and out of the app. Property data can be calculated but needs work with DOM manipulation. Fixed the venv issue with VSC in the weekend which was amazing. Will try to be more specific and actually leave notes in here more than just writing it down in my notepad.

---

WEEK 2

---

DATE: Monday 5/9

TO DO:
[x] Add logic to JS to change color when cash flow is negative or positive
[x] Edit profile
[x] Add Google Maps API

JOURNAL:

---

DATE: Tuesday 5/10

DONE:
[X] Refactored calculator
[X] Wrote glossary of key rental property terms
TO DO:
[x] AJAX to update cash flow calculation on index.html

JOURNAL:

--- Today felt extremely hard because I spent almost 12hrs working one feature, refactoring data model after deciding to not use Zillow API anymore. Felt like AJAX need some serious refresher. Decided to work with JS on the front end to change color instead of AJAX call

DATE: Wednesday 5/11

TO DO:
[x] Fix AJAX call to update calculator in queue
[x] Update profile and property profile for users when they log in
[x] Start building blogging and commenting functionality

JOURNAL:

---

DATE: Thursday 5/12

TO DO:
[] Google Books API (considering)
[] Gravatar API (considering)
[] OAuth (considering)
[x] Add/delete properties
[x] Building blogging and commenting functionality (finally done with designing the dashboard)
[x] Add datetime (created_at) to db for comment and blog tables
JOURNAL:

--- Did a lot of reading on understanding requests, session and fetch API to make sure I won't create bugs while setting up forms.

DATE: Friday 5/13

TO DO:
[x] Allow users to create a blog post
[] Allow users to delete a blog post
[] Allow users to update a blog post
[] Show the nums of posts by a user
[x] Show the nums of posts by all users in dashboard

JOURNAL:

--- There are still a lot of features I want to implement. Hope to get some more work done over the weekend!

DATE: Saturday 5/14:
[] Allow users to comment on a blog post
[] Allow users to delete a comment
[] Allow users to update a comment
[] How to set up the view for comments from blog
[x] Show the nums of posts by all users in dashboard
[x] Picture handling
[] Book API
[] OAuth is nice to have
[] Remember my Password option
[] Newsletter

JOURNAL:
--- I want to cry with excitement! I am so happy! Not only did I manage to use Cloudinary, but I have the logic for the profile pic to update 'instantly' for my users! I also updated the blog and changed a few different options but came back to the table format like I had initially. I definitely want to be better at querying though as I did notice some queries might be slower than others.
I am super happy to actually think of sorting the data desc to get the latest imgURL for the profile pic update for users! Feeling very accomplished! What a great Saturday!

WEEK 3:

---

DATE: Monday 5/16:
[] Allow users to comment on a blog post
[] Allow users to delete a comment
[] Allow users to update a comment
[] Set up the view for comments from blog
[] Show the nums of posts by all users in dashboard
[] Picture handling
[] Add a placeholder pic for the chart
[] Reorganize the chart and calculator on front page

JOURNAL:
What I learned today the hard way after spending minutes, hours banging my head against the desk (aka reading the documentation, reading stackoverflow, googling, rereading my code to check line by line) is that I didn't call the function! In my head, the seed db function worked before because I had my blog posts seeded before. I either must have deleted it or something.
Self-reminder regarding debugging:

1. Always try to understand the traceback to see where the errors might be from (this is something I got really comfortable with now)
2. Check the most fundamental things that you cannot believe you made: for example: a typo. Check line by line for typos
3. Add print statements where needed (I need to do this more often!)
4. Check console/network if applicable
5. If it's a function, always remember to check if the func is called!
