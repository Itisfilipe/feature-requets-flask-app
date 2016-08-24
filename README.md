# Engineering Project
This is a project that we use for testing potential team members on their technical skills.

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

## Tech Stack Suggestions
The following are recommendations on tech stack. You can build a project outside of this framework,
but this stack demonstrates mastery of  tools our team favors.

* OS: Ubunutu
* Server Side Scripting: Python 2.7+ or 3.5+
* Server Framework: Flask
* ORM: Sql-Alchemy
* MVVM: Knockout.js
* CSS: Bootstrap 4 or similar

Make sure that your instructions for accessing or otherwise running your code are extremely clear.

## Guidelines

Build your own public repo on github, and call it whatever you like. Build your solution in your
repo, and include a README.md file that contains the detailed instructions for running your web app.
Email the URL for your github repo to phil@britecore.com once you begin the project so we can review 
your progress. Prior to submission, please bring up a live hosted example. AWS has a free tier if you 
aren't certain where to host.

One of the major goals in this project is to see how you fill in ambiguities in your own creative
way. There is no such thing as a perfect project here, just interpretations of the instructions
above, so be creative in your approach. While we want to see an expression of your style and problem
solving, we also want to keep you moving, so please feel free to email phil@britecore.com with questions
if you get stuck or have questions.

We want to be respectful of your time and set realistic expectations for submission. To help guide you, we 
have included the list below which details common in the best projects we receive. It is rare for 
a project to match every item in this list, but the candidates we hire typically showcase several of 
these features in their work.

--

TECHNOLOGY

1. *Open Source*. We have a strong affinity for open source technology. If your go-to technology stack includes
proprietary software, you won't be helping yourself to use it in this project.

2. *Decoupled Backend*. We are looking for candidates with a strong understanding of the entire web application stack. Move beyond a stock template or the admin page from a CMS. Show off your understanding of how frameworks are put together and create at least a couple of methods that flex your intellectual muscle. The best projects will completely decouple the backend and the front end and communciate via API.

3. *Test Suites with Continuous Integration*. Enterprise production requires rock solid stability. All code submitted into BriteCore repos must contain unit and regressions tests, so we favor candidates with experience writing quality tests. The best projects include a test suite hooked into a Continuous Integration platform like Jenkins or Travis CI.

4. *Automated Deployment*. Speaking of deployment, the most valuable engineers understand how their code is deployed and utilize provisioners such as Salt Stack, Puppet, or Chef. The best projects integrated CI with a fully automated deployment to AWS, Digital Ocean, or similar.

5. *Usable, Responsive Interface*. There are many accessible CSS frameworks out there such as Bootstrap. All modern web applications should be responsive and these frameworks make it very easy to create a modern interface that adheres to established design principles and formats well on all devices.

6. *MVVM Frontend*. The modern web is highly interactive. Projects like Knockout.js and Angular make it very easy to deploy HTML bindings that interact with interface elements dependably and efficiently.

--

PROJECT FEATURES

1. *User Management*. A system that holds client feature requests benefits greatly from user management. Some projects include admin controlled user accounts. Better projects included self enrollment via email. The best projects used a SSO solution like OAuth or SAML.

2. *Client / Project Management*. As a base requirement, you had a fixed list of clients and projects, but the best projects included a simple admin interface associated with the admin login that gives users a basic CRUD interface for these entities.

3. *Filter by Client*. If multiple clients are submitting feature requests, it is important to be able to view the total task list as well as a list filtered by client.

4. *Sorting*. This one is very important if you've ever worked on a real project and managed client priorities. Decent projects deploy unique sort rank per client. Better projects include sorting per client AND whole all client sorting. The best projects do all of this utilizing a drag and drop component bound to the MVVM framework.

5. *Discussion Threads*. A few projects go far enough to include discussion threads within each feature request and one has even included push notifications utilizing SMS.

Thank you for your time. We are excited to review your project!

