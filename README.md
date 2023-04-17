# DBSR API:

This is the codebase that syncs the DBSR googlesheet with the local postgres database that manages all the file locations and metadata. 

## How it works:
Triggers have been set up in the google sheet that tracks our music library, specifically an installable "onEdit" trigger. Any time a cell is editted, a api request is made to this library which will then publish the changes to the postgres database that tracks all the metadata in the library. The nextKast library will also be updated to match. The goal is that the we'll be able to manage the DBSR music library remotely using googlesheets. 


## Schema details:

## 