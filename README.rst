
Django BMF understands itself as a ERP-Framework with the following design concepts:

* KISS-Principe for endusers
* Fast and easy configuration for people with medium know-how
* Highly customizeable with as few lines of code as possible for application developers

Features
===========================

* Functionality as a django application
  - for an easy integration into an existing django project
  - to make the development of modules easy
  - for the benefit to use a module in an different place of django project (i.e. an online-shop or an customer-interface)
* Login/Logout
* Notifications about activities
* Watch and unwatch models
* File-Upload and document management
* Comments on models
* Information about data-changes
* Behaviour "Django-Admin with custom views"
* Filtering of data and saving the view to a dashboard
* PDF-Reports (very simple and easy to-modify)
* Responsive design -> getbootstrap.com
* Workflows attached to models
  - easy configureable as classes (Workflow, states and transitions)
  - custom functions for transitions
  - integrated into the BMF (i.e you can delete or update a model instance only if the State allows you to do so)
* Each option should be activated and deactivated in die model definition (how needs to append files or write comments to a tax-model?)


Documentation
===========================

Getting Help
===========================

Credits
===========================

django
django-filter
django-mptt
django-celery
xhtml2pdf
