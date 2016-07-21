# Engineering Project
This is a project that we use for testing potential employees on their technical skills.

## Feature Request App
Build a web application that allows the user to create "feature requests".

A "feature request" is a request for a new feature that will be added onto an existing piece of
software. Assume that the user is an employee at IWS who would be entering this information after
having some correspondence with the client that is requesting the feature.  The necessary fields
are:

* **Title:** A short, descriptive name of the feature request.
* **Description:** A long description of the feature request.
* **Client:** A selection list of clients (use "Client A", "Client B", "Client C")
* **Client Priority:** A numbered priority according to the client (1...n). Client Priority numbers
should not repeat for the given client, so if a priority is set on a new feature as "1", then all
other feature requests for that client should be reordered.
* **Target Date:** The date that the client is hoping to have the feature.
* **Ticket URL:** A field for storing any URL
* **Product Area:** A selection list of product areas (use 'Policies', 'Billing', 'Claims',
'Reports')

## Tech Stack
* OS: Ubuntu
* Server Side Scripting: Python 2.7+ or 3.5+
* Server Framework: Flask
* ORM: Sql-Alchemy
* MVVM: Knockout.js
* CSS: Bootstrap 4 or similar

Make sure that your instructions for accessing or otherwise running your code are extremely clear.

## Instructions for Submission

Build your own public repo on github, and call it whatever you like. Build your solution in your
repo, and include a README.md file that contains the detailed instructions for running your web app.
Email the URL for your github repo to phil@britecore.com once you begin the project so we can review 
your progress. Prior to submission, please bring up a live hosted example. AWS has a free tier if you 
aren't certain where to host.

## Questions and other such clarification
One of the major goals in this project is to see how you fill in ambiguities in your own creative
way. There is no such thing as a perfect project here, just interpretations of the instructions
above, so be creative in your approach. Feel free to send an email with questions about intent or approach.

Some or all of the following are typically true of the best projects we receive: 

1. Modern, Crafted Backend. We received many projects that were based on a stock Django, Rails, or PHP template. Although the requirements of the project could easily be completed by relying solely on frameworks, that is rarely the case when dealing with a production application. Candidates who stood out didn't rely solely on these tools, which showed us they have the ability to solve complex problems well.

2. Test Suites with Continuous Integration. Enterprise production requires rock solid stability. We are very test driven in our development processes and maintain a test suite of many thousands of tests for BriteCore. The best projects not only included a test suite, they were fully integrated with a Continuous Integration platform like Jenkins or Travis CI which would return a pass or fail status on the project before deployment.

3. Automated Deployment. Speaking of deployment, the most valuable engineers understand how their code is deployed and utilize provisioners such as Salt Stack, Puppet, or Chef. The best projects integrated CI with a fully automated deploy to AWS, Heroku, or similar.

4. Usable, Responsive Interface. There are many accessible CSS frameworks out there such as Bootstrap. All modern web applications should be responsive and these frameworks make it very easy to create a responsive modern interface that adheres to established design principles and formats well on all devices.

5. MVVM Frontend. The modern web is highly interactive. Projects like Knockout.js and Angular make it very easy to deploy HTML bindings that interact with interface elements dependably and efficiently.

--

PROJECT FEATURES

1. User Management. A system that holds client feature requests benefits greatly from user management. Some projects included admin controlled user accounts. Better projects included self enrollment via email. The best projects used a SSO solution like OAuth or SAML.

2. Client / Project Management. As a base requirement, you had a fixed list of clients and projects, but the best projects included a simple admin interface associated with the admin login that gives users a basic CRUD interface for these entities.

3. Filter by Client. If multiple clients are submitting feature requests, it is important to be able to view the total task list as well as a list filtered by client.

4. Sorting. This one is very important if you've ever worked on a real project and managed client priorities. Decent projects deployed unique sort rank per client. Better projects included sorting per client AND whole all client sorting. The best projects did all of this utilizing a .js drag and drop component binding from the MVVM framework.

5. Discussion Threads. A few projects went far enough to include discussion threads within each feature request and one even included push notifications utilizing SMS.

We also have a strong affinity for open source technology. If your go-to technology stack includes
proprietary software, you won't be helping yourself to use it in this project.
