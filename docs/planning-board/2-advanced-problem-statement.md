# Advanced problem statement
> We will focus on AWS for the purpose of this project.

> DISCLAIMER: Done completely by me without any AI inference, it is basically a summary

Create an API based on **AWS services**, mostly relying on its **serverless platform**. The purpose of the API is to be able to ***<u>create and manage VPCs and their associated subnets</u>***. Besides managing actual infrastructure in the cloud, the automation should also ***<u>store the results</u>*** in a suitable database (SQL - due to the nature of the application VPCs and Subnets are related). The API should be written in Python, and also **protected with an authentication layer**. Authorization should be open to all authenticated users (?? authenticated in the API, or authenticated in what? Still need to find out how the auth will be managed, but most likely there's going to be another aws service in front).

The project should be well documented, well configured and stored in a Github repository. Besides providing good DevOps practices through documentation and structuring, it should also be as automated as possible, so it is prefferred that the platform will be automatically deployed through a GithubActions Pipeline