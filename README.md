# Spotify playlist ETL pipeline on AWS
**Objectives**: Designing a fully-automated ETL pipeline on AWS to extract Spotify's weekly _Top Songs - Global_ playlist and store the Artist, Album and Song data on AWS Glue Data Catalog tables.

## Solution Architecture
![solution architecture](./spotify-playlist-etl-pipeline-aws.png)

## Files
`spotify-data-pipeline-project.ipynb`: to connect with the Spotify API and test the data transformation logic on your local environment.

```
spotify_api_data_extract
├── lambda_function.py
```
contains Lambda Function code to extract raw data from the Spotify API.
```
spotify_transformation_load_functions
├── lambda_function.py
```
contains Lambda Function code to transform raw data and extract artist, album and song structured data.


## Implementation of Services

**Spotify API**

One would need developer app credentials (_Client ID_, _Client Secret_) to transact with the _Spotify Web API_. You can follow how to create them [here](https://developer.spotify.com/documentation/web-api). 

**Amazon EventBridge**
- Create new **EventBridge Rule** to run at a given schedule (eg. every 1 day, week).
- Set the trigger's target to be the Lambda function for Data Extraction from the Spotify API.

**AWS Lambda - Data Extraction**
- Create the **Lambda Function** for Data Extraction _spotify_api_data_extract_ which runs on an appropriate Python runtime (eg. Python 3.8+).
- This function will be executed according to the schedule setup by the EventBridge Rule.
- Add the data extraction code to the created _lambda_function.py_. Ensure that the **spotipy** package is available in connected **Lambda Layer** for it to be accessed in the function environment.

**Amazon S3 - for Raw and Transformed data**
- Create an S3 bucket _spotify-etl-project-demo_ which will manage both raw data (from the Spotify API) as well as the processed structured data to be used downstream.
- Create two primary folders: _raw_data/_ and _transformed_data/_. 
- _raw\_data/_: will contain subfolders - _processed/_, _to_processed/_ which will contain and manage the raw playlist data.
- _transformed\_data/_: will contain subfolders - _artist\_data/_, _album\_data/_, _song\_data/_ which will contain and manage the artist, album and song structured data.

**AWS Lambda - Data Transformation**
- Create the Lambda Function for Data Transformation _spotify_transformation_load_function_ which runs on an appropriate Python runtime (eg. Python 3.8+).
- This function will be triggered whenever a new file is dropped into the _raw_data/to_processed/_ folder of the _spotify-etl-project-demo_ S3 bucket.
- The code will extract the artist, album and song data and save as structured data in the transformed folder, as well as manage the raw data by moving it into the processed folder.
- Add the data transformation code to the created _lambda_function.py_. Ensure that the _AWSSDKPandas-Python38_ AWS Lambda Layer is added to the function for the _pandas_ package to be accessed in the function environment.

**AWS Glue Crawler - infer schema & Amazon Athena - analytics**
- Create respective **Glue Crawlers** to infer schema of transformed artist, album and song data and to store their metadata in **Glue Data Catalog**.
- Set the respective S3 data folders as the data source for the crawlers; also specify the schema metadata like headers, column datatypes by creating the corresponding **Glue Classifiers**. This will allow the crawler to correctly parse the files in the data source.
- The output could be a specific database in the **Glue Data Catalog**.
- Running the created Crawlers could be based on a specific schedule or even manually (eg. a day after new data arrives).
- The Data Catalog database tables can be viewed and queried on **Amazon Athena**.

If needed, the data could also be uploaded to a database server which could then be connected to a dashboard tool like _PowerBI_, _Tableau_ to visualize your findings 📊📈.

**NB**: this project was entirely performed on [the AWS free tier](https://aws.amazon.com/free/). However, compute services like AWS Lambda, Glue Crawler, Amazon Athena can rake up high costs if unmonitored, therefore as a precaution it is advisable to set up [cost alarms](https://aws.amazon.com/cloudwatch/) and [calculate cost estimations](https://calculator.aws/#/) in prior.


