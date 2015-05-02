#!/usr/bin/env python
# 
# DB_Handler.py version 3.1
# created by Victor Asselta
# written for project2 in Udacity's Full Stack NanoDegree

# Class currently just uses PostGreSQL python connection
import psycopg2
import bleach

# Class which enables more, hopefully, efficient database access
# for project 2 of Udacity Full Stack Nanodegree.
class DB_Handler(object):
    
    
    ''' Class Properties '''
    # Database name dbname, set the database name to connect to.
    @property    
    def dbname(self):
        return self.properties.get('dbname', 'tournament')
     
    @dbname.setter
    def dbname(self, newTourID):
        self.properties['dbname'] = newTourID
        
    @dbname.deleter
    def dbname(self):
        del self.properties['dbname']
        
    ''' Class Init and Methods '''
    # initialization: Can configure all properties with included keyword arguments
    #__ are used to label methods as private, yet this may not be enough security
    def __init__(self, **kwargs):
        self.properties = kwargs
        
    # Connection call to set database
    def __connect(self):
        
        connectionString = "dbname=" + self.properties['dbname']
        return psycopg2.connect(connectionString)
    
    # Cursor call for queries
    def __cursor(self, query):
        DB = self.__connect()
        cursor = DB.cursor()
        results = None
        
#         >>> SQL = "INSERT INTO authors (name) VALUES (%s);" # Note: no quotes
#         >>> data = ("O'Reilly", )
#         >>> cur.execute(SQL, data) # Note: no % operator
        
        cursor.execute(query)
        
        try:
            results = cursor.fetchall()
        except:
            pass
            #print("No Results to Return")
        
        DB.commit()
        DB.close()
        
        return results
    
    # Call to bleach link and clean methods to sanitize queries    
    def __cleanQuery(self, query):
        bleachClean = bleach.clean(query)
        #bleachLink = bleach.linkify(bleachClean)
        
        return bleachClean
      
    # Handle incoming query. Takes 1 argument query for requested query statement   
    def sendQuery(self, query):
        
        cleanQuery = self.__cleanQuery(query)
        queryReturn = self.__cursor(cleanQuery)
        
        return queryReturn