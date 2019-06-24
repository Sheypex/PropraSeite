# Gruppe 4 - Message Alert System

## **General Information**

This Readme file should contain information about **How To** deploy, install and execute our project, as the **Requirements** to do it. Please, try to document all the steps and information required to do it, so everybody has an understanding of how to start our project. Make it as simple and easy as possible to avoid any problems. Document everything you might think its important. Feel free to make any changes to this file. 

Please, try to make contantly commits to the repository so it is easy to follow each others activity and contributions to the project

Happy coding!

## **Technologie**

The following technologies have been used to develop this Project:
- KNIME: KNIME is a Analytics Platform leading open solution for data-driven innovation, designed for discovering the potential hidden in data, mining for fresh insights, or predicting new futures. (https://www.knime.com/about)
- Python (https://www.python.org) and Frameworks (Pandas, MIME, smtplib)
- Raspberry Pi Model B+ (https://www.raspberrypi.org)
- Angular
- node.js
- Web Technologie (HTML, JS, CSS, SCSS)
- Plotly (JS Framework for Data visualization)
- JSON to pass data between instances
- Gitlab
- Github

## **Requirements**

This project is thought to be running on a Raspberry Pi 3 Modell B+

- Python 3
- node.js

## **How To**
This section is meant for the developers, to get an idea of any configuration stuff, how some technologies are used in the project and some general information required to further develop the project. Its also meant to document things that might be required for the other members to get the project running

#### Tables format

To analize the tweets, the following tables are generated as CSV files and passed to the analizers for further processing. The tables below show the used data from each table type. The project was developed static, so the files must follow the naming format below, where SEARCH should be replaced with the name of the Tweet topic. The naming on the tables is also important and must follow the Columns naming format

###### SEARCH_TermsCounted.csv
|Anzahl     | Term |
|:---------:|------|
| Number    |String|


###### SEARCH.csv
|Tweet |Tweet ID|Time               |Favorited|Retweeted|Is Favourited|Is Retweeted|Is Retweet|Retweet from|Latitude|Longitude|Country|User  | 
|:---: |--------|-------------------|---------|---------|-------------|------------|----------|------------|--------|---------|-------|------|
|String|Number  |yyyy-mm-dd hh:MM:ss|(0,1)    |Number   |(0,1)        |(0,1)       |(0,1)     |String      |Number  |Number   |String |String| 

###### SEARCH_Sentiment.csv
|  Tweet_ID | Term  |Time               |Sentiment |
|:---------:|-------|-------------------|----------|
|  Number   |String |yyyy-mm-dd hh:MM:ss|String    |

###### SEARCH_TopUsers.csv
|  User | Count  |
|:-----:|--------|
| String| Number |

#### _Run Knime on the Console_
To run Knime on the Console just execute this code (linux):

```
knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION​
```

If needed, Specify the working directory as following:

```
knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowDir="MY_DIRECTORY/Knime_project"
```

Lastly if it is on a zip file:

```
knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowFile="PATH_TO_FILE/Knime_project.zip"
```

Some useful Options:

- ```-consoleLog``` Causes a new window to be opened containing the log messages and will keep the window open after the execution has finished. You will need to close the window manually and an error message is produced from the Java process which you can safely ignore
- ```-nosave``` If this is specified, the workflow is not saved after execution has finished.
- ```-reset``` Reset workflow prior to execution.


#### _Schedule Jobs with Crontab_

For our project we need to execute our workflow in a Scheduled basis. Therefore the most effective way to do it, is to create a cron job that executes a skript. Here you can find how to use Cron jobs and how to use it to create and configure the scheduler. 

With Cron you can schedule jobs (Execution from Skripts/Commands) easily. To see the current cron jobs use this command:

```
crontab -l
```

To edit or create a new cron job:

```
crontab -e
```

this will open an editor. each cron job has to be written on a single line and must follow its format. Add your job at the end of the file. The Job must follow this format: 

```
* * * * * command to be executed
- - - - -
| | | | |
| | | | ----- Day of week (0 - 7) (Sunday=0 or 7)
| | | ------- Month (1 - 12)
| | --------- Day of month (1 - 31)
| ----------- Hour (0 - 23)
------------- Minute (0 - 59)
```

it is also possible to use some of the following reserved words:

- @reboot: Executed just once at the start.
- @yearly/@annually: Execute each Year.
- @monthly: Execute once a Month.
- @weekly: Once a week.
- @daily/@midnight: Execute once a day.
- @hourly: once an hour.

Here is an example: 

```@hourly /bin/execute/script.sh```

In our project this is the predefinded cron job (Run our skript every 30 minutes during the week):

```
0,30 * * * 1-5 $PROJECT/start-workflow.sh
```

