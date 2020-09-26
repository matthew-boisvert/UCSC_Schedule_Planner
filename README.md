# Slug Scheduler
Slug Scheduler is a web application that allows UCSC students to easily update their Google Calendars with their class schedules. Slug Scheduler was developed in Flask with the help of the existing [UCSC Courses API](https://github.com/AndrewLien/UCSC_Courses_API) by Andrew Lien. With this app, students no longer have to manually input their schedules into their calendars to make class planning much simpler.



## How to use

As of August 2020, the web app must run on one's own machine and then users can connect to it locally. To do this, all you have to do is:
1. Clone the repository
2. Go to [this page](https://developers.google.com/calendar/quickstart/python) to enable the Google Calendar API and set up your client_secret.json file
3. Run ucsc_courses.py for the first time the app is used to populate the database
4. Update relevant_term.json to have the correct info. Ex. for Fall 2020, the relevant information is: `{
  "relevant_term": "2020 Fall Quarter",
  "start": "Oct 1"
}`
    
4. Run mainPage.py
5. Connect to http://localhost:5051/

In the near future, the app will be hosted on a domain for easier use.

## Future Updates
In the near future, these are the features that we would like to add to this application in order to make it as useful and user-friendly as possible:

 1. Finishing Google Oauth2 Support
 2. Hosting the web app in the cloud
 3. Configuring the app to support other calendar services and scheduling tools