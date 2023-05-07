# UB Recommends
This README file provides a step-by-step guide on how to set up and run the Django-powered back-end and front-end of UB Recommends. UB Recommends is a recommendation system that uses a collaborative filtering algorithm to recommend university courses to students.

## Step 1 | Unzip the src/ directory
Start by unzipping the src/ directory. The src/ directory contains code for the front-end and the back-end. The back-end code is written in Python with Django as the framework, and the front-end uses vanilla HTML, CSS, Bootstrap, and JavaScript.

## Step 2 | Install and setup Python
This setup guide assumes that Python is installed and setup on your system. Please refer to https://python.land/installing-python to install Python for your machine. 
Once installed, you can check if your installation was successful by running the following command on your terminal:

```
python --version
```

## Step 3 | Running the Front-end
- Running the front-end should be straightforward. Simply open the src/ directory in any code editor that supports a server for the front-end. We recommend using Visual Studio Code with the Live Server plugin by Ritwik Dey.

- After the plugin is installed, open the project and click "Go Live" on the bottom right. This should take you directly to the login screen of UB Recommends.

## Step 4 | Running the Back-end
Running the back-end powered by Django requires a few steps. We start by creating a virtual environment, installing all dependencies, and then running the project.

## Step 5 | Create virtual environment
Creating a virtual environment is optional but advisable so that you can set up the dependencies different projects require separately. If you are on Windows, you can follow the commands below after setting up pip and Python:

```
pip install virtualenv
```
Once the installation is complete, run the following command to create a new virtual environment:

```
python -m venv <environment_name>
```
Once this is done, activate your virtual environment by running:

```
.\<environment_name>\Scripts\activate
```
If this step is successful, you should be able to see your terminal prompt change to include the name of your virtual environment in parentheses.



## Step 6 | Installing all requirements
The requirements.txt file is present at 
```recommendation_system_backend > recommendation_system_backend > requirements.txt```

Go to the aforementioned directory and execute:

```
pip install -r requirements.txt
```

## Step 7 | Boot the Server
To boot the server, all you have to do is run the following command in the parent recommendation_system_backend directory, and you will see that the server is up at port 8000:

```
python manage.py runserver
```
If you see the following logs on the console, it means that the server is up and running:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
To stop the server, simply press Ctrl/Cmd + C on the terminal.
```

## Step 8 | Explore
That's it! You should now have the UB Recommends back-end and front-end up and running on your machine.


# References
-  Ong, D. (n.d.). Yelp Restaurant Recommendation System — Data Science Capstone Project. Towards Data Science. https://towardsdatascience.com/yelp-restaurant-recommendation-system-data-science-capstone-project-d7d6f60d1de7
-  Gupta, S. (2018, November 8). How I would explain building LightFM Hybrid recommenders to a 5-year-old. Towards Data Science. https://towardsdatascience.com/how-i-would-explain-building-lightfm-hybrid-recommenders-to-a-5-year-old-b6ee18571309
-  Google. (n.d.). Content-Based Recommendation: Basics. Retrieved from https://developers.google.com/machine-learning/recommendation/content-based/basics
-  Zhou, T. (2020, May 10). Introduction to Recommender Systems. Towards Data Science. https://towardsdatascience.com/introduction-to-recommender-systems-1-971bd274f421
-  Upadhyay, R. (2021, March 29). Evaluating Recommender Systems in Absence of Labeled Data. SAP Blogs. https://blogs.sap.com/2021/03/29/evaluating-recommender-systems-in-absence-of-labeled-data/
-  Stack Exchange Inc. (2021). Model Performance When Ground Truth Is Not Available. Cross Validated. https://stats.stackexchange.com/questions/573798/model-performance-when-ground-truth-is-not-available
-  Surprise Team. (n.d.). Surprise Documentation. https://surprise.readthedocs.io/
-  Paul, A. (2018, January 10). Recommendation System in Python: LightFM. Towards Data Science. https://towardsdatascience.com/recommendation-system-in-python-lightfm-61c85010ce17
-  Balu, B. (2021, February 4). Content-Based Recommender Systems. Towards Data Science.https://towardsdatascience.com/content-based-recommender-systems-28a1dbd858f5
-  Neptune AI. (n.d.). Recommender Systems Metrics: Evaluation of Recommendation Algorithms. https://neptune.ai/blog/recommender-systems-metrics
-  Pande, S. (2019, June 10). Inside Recommendations: How a Recommender System Recommends. SciForce. https://medium.com/sciforce/inside-recommendations-how-a-recommender-system-recommends-9afc0458bd8f
-  Adwankar, R. (2019, April 24). Personalized Restaurant Recommender System Using Hybrid Approach. MSiA. https://sites.northwestern.edu/msia/2019/04/24/personalized-restaurant-recommender-system-using-hybrid-approach/
-  Agarwal, S. (2018, June 22). Some Metrics to Evaluate Recommendation Systems. Medium. https://flowthytensor.medium.com/some-metrics-to-evaluate-recommendation-systems-9e0cf0c8b6cf
-  Paul, A. (2018, January 10). Recommendation System in Python: LightFM. Towards Data Science. https://towardsdatascience.com/recommendation-system-in-python-lightfm-61c85010ce17
-  Balu, B. (2019, October 8). Content-Based Recommender System. Medium. https://medium.com/@bindhubalu/content-based-recommender-system-4db1b3de03e7
-  Dr Eric Mikida & Dr. Shamsad Parvin – Class Lecture Slides and Lecture videos.
-  Garg, N. (2020, April 28). Beginner’s Guide to Exploratory Data Analysis (EDA) on Text Data. Analytics Vidhya. https://www.analyticsvidhya.com/blog/2020/04/beginners-guide-exploratory-data-analysis-text-data/
-  Prusty, S. (2018, November 18). What is Exploratory Spatial Data Analysis (ESDA)? Towards Data Science. https://towardsdatascience.com/what-is-exploratory-spatial-data-analysis-esda-335da79026ee
-  Pony Biam. (n.d.). 03-enth-geospatial-eda. Kaggle. https://www.kaggle.com/code/ponybiam/03-enth-geospatial-eda
-  Kamal Chhirang. (n.d.). Detailed Exploratory Data Analysis with Python. Kaggle.https://www.kaggle.com/code/ekami66/detailed-exploratory-data-analysis-with-python/notebook
-  Panchal, P. (2021, June 16). VADER for Sentiment Analysis. Analytics Vidhya. https://www.analyticsvidhya.com/blog/2021/06/vader-for-sentiment-analysis/


