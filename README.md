# INVESTABLE

## _a platform for rental property investors_

## Table of Contents

- [Summary](#summary)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Data Model](#data-model)
- [Local Installation](#installation)
- [About the Developer](#aboutme)
- [Acknowledgements](#acknowledgements)

## <a name="summary"></a>Summary

Real estate investing is fantastic way to create wealth and build a stream of passive income. Having been a real estate investor with a background in property accounting for numerous years, I have always wanted to build a tool that would assist new investors with their decision making and investing journey.<br>
<br>
**INVESTABLE** is a research tool for investors looking to make a quick decision whether a rental property is a good investment. Ultimately it strives to provide users with tools and a platform to share the passion for rental property investing.

<ul>
<li> This application allows users to input data and run the numbers quickly to see if a property is generating positive cash flows given your estimates of rental income and expenses are accurate. </li>

<li> It also allows users to ask questions, share knowledge and network through a community dashboard feature. </li>

<li> Users can also enrich their skills through the industry insights and book recommedation API features. </li>
</ul>
<!-- INVESTABLE is available online at <a href="https://investable.com/">https://investable.com/</a> -->

## <a name="tech-stack"></a>Tech Stack

**Back End:** Python3, Flask framework, SQLAlchemy ORM, Postgresql database<br/>
**Front End:** JavaScript, AJAX, JSON, Jinja2, Bootstrap5, HTML, CSS<br/>
**APIs:** Google Maps API, News API, Google Books API, Cloudinary API, Chart JS <br/>

## <a name="features"></a>Features

Non-logged in users are able to **analyze any property**; they also have access to read industry news provided to us via **News API**, read book recommendations (**Google Books API**) as well as random **inspirational quotes** related to investing (I curated a list of inspirational quotes and send them to the front end through a fetch request). Below is an overview of the front page. Simply enter your estimates in the calculator:

<br/>![Rental Cash Flow Calculator](/static/calculator1.gif)<br/><br/>
In order to save data and use more features that INVESTABLE has to offer, users might choose to sign up.
Users are able to do some research on the surroundings of a property through Google Maps API.

<br/>![ggmaps](/static/ggmaps.gif)<br/><br/>

Upon successful registration, users now can not only analyze but also save any property's data to their account and **compare the expenses** and rental income from these properties to see which one might be a better investment.
<br/>![Register and logging in](/static/calculator2.gif)<br/><br/>

Users can now post questions, seek advice and network with other like-minded investors in INVESTABLE community **dashboard**.
<br/>![Forum](/static/forum.gif)<br/><br/>
Users can also update their profile picture and add blog photos if they choose to do so. **Cloudinary API**
<br/>![cloudinary](/static/cloudinary.gif)<br/><br/>

Users can also **leave feedback** via the contact form:
<br/>![contact](/static/contact.gif)<br/><br/>

## <a name="data-model"></a>Data Model

<br/>![data-model](https://github.com/olivia-tran/Catculator-investment-tool/blob/main/project-planning/revised-datamodel.png)<br/><br/>

## <a name="installation"></a>Local Installation

#### Requirements:

<ul>
<li>Need to acquire Google API key and don't forget to limit the key to only work on your browser, this key will need to be activated for both Google Maps and Google Books API.</li>
<li>News API key </li>
<li>Cloudinary registration </li>
<ul>

To run this app on your local computer, please follow these steps:

Clone repository:

```
$ git clone https://github.com/olivia-tran/investable-rental-property-investor-tool.git
```

#### Setup Flask:

Create a virtual environment:

```
$ virtualenv env
```

Activate the virtual environment:

```
$ source env/bin/activate
```

Install dependencies:

```
$ pip3 install -r requirements.txt
```

#### Setup Credentials/Secrets:

Create a secrets.sh file

#### Setup the database:

Once your API credentials are retrieved, you can create and seed your database.

With PostgreSQL installed, create your database 'investables':

```
$ createdb investables
```

Create your database tables:

```
$ python3 model.py
```

Seed the database by using some modified data from Redfin and Bigger Pockets:

```
$ python3 seed.py
```

To start the Flask web server, run:

```
$ python3 server.py
```

In your browser, visit <a href="http://localhost:5000/">http://localhost:5000/</a>

## <a name="acknowledgements"></a>Acknowledgements

I'd like to express my greatest appreciation to all the individuals who have helped and supported me throughout the project as well the 12 week intensive coding bootcamp. I am thankful for the knowledge I've gained and also the ongoing support and encourgement I got from Hackbright instructors and cohortmates. I also appreciate the feedbacks I got on certain features which help me build a better application. I wish to thank my family and friends for their support and encouragement throughout my study because I was not as present and when I was I would be constantly speaking of my code. Couldn't have done it without your code reviews, guidance, inspiration, constructive feedbacks and support.

## <a name="aboutme"></a>About the Software Engineer

Olivia is a software engineer based in San Francisco whose passion is learning and self-development. She is an experienced accountant in the real estate property management space prior to pivoting her career to software engineering.

Connect and learn more about Olivia on <a href="https://www.linkedin.com/in/oliviatran99/">LinkedIn</a>.
