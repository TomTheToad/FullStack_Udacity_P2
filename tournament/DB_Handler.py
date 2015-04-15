
# Class currently just uses PostGreSQL python connection
import psycopg2

# Class which enables more efficient, hopefully, database access
# for project 2 of Udacity Full Stack Nanodegree.
class DB_Handler(object):
    
    #Getters, Setters
    
    # Database name dbname
    @property    
    def dbname(self):
        return self.properties.get('dbname', 'tournament')
     
    @dbname.setter
    def dbname(self, newTourID):
        self.properties['dbname'] = newTourID
        
    @dbname.deleter
    def dbname(self):
        del self.properties['dbname']
    
    # Tour ID number tourID
    @property    
    def tourID(self):
        return self.properties.get('tourID', '1')
     
    @tourID.setter
    def tourID(self, newTourID):
        self.properties['tourID'] = newTourID
        
    @tourID.deleter
    def tourID(self):
        del self.properties['tourID']
     
    # Table name property tableName   
    @property    
    def tableName(self):
        return self.properties.get('tableName', None)
     
    @tableName.setter
    def tableName(self, newTableName):
        self.properties['tableName'] = newTableName
        
    @tableName.deleter
    def tableName(self):
        del self.properties['tableName']
        
    # Use restriction or not boolean restrict
    @property    
    def restrict(self):
        return self.properties.get('restrict', None)
     
    @restrict.setter
    def restrict(self, TrueOrFalse):
        self.properties['restrict'] = True
        
    @restrict.deleter
    def restrict(self):
        self.properties['restrict'] = None
    
    # list of WHERE clause restrictions restrictWhere  
    @property    
    def restrictWhere(self):
        return self.properties.get('restrictWhere', None)
     
    @restrictWhere.setter
    def restrictWhere(self, addRestriction):
        self.properties['restrictWhere'] = (addRestriction)

    @restrictWhere.deleter
    def restrictWhere(self):
        del self.properties['restrictWhere']
        self.properties['restrict'] = False
        
    # True or False return results from a query  
    @property    
    def queryReturn(self):
        return self.properties.get('queryReturn', False)
     
    @queryReturn.setter
    def queryReturn(self, TrueOrFalse):
            self.properties['queryReturn'] = True

    @queryReturn.deleter
    def queryReturn(self):
        del self.properties['queryReturn']
        self.properties['queryReturn'] = None
        
    # True or False add count(*) functionality to a query  
    @property    
    def count(self):
        return self.properties.get('count', False)
     
    @count.setter
    def count(self, TrueOrFalse):
            self.properties['count'] = True

    @count.deleter
    def count(self):
        del self.properties['count']
        
    # True or False add ability to have multiple fields in a select statement 
    @property    
    def multiSelect(self):
        return self.properties.get('multiSelect', False)
     
    @multiSelect.setter
    def multiSelect(self, TrueOrFalse):
            self.properties['multiSelect'] = True

    @multiSelect.deleter
    def multiSelect(self):
        del self.properties['multiSelect']
        
    # list of fields for select  
    @property    
    def select(self):
        return self.properties.get('select', None)
     
    @select.setter
    def select(self, addSelect):
        self.properties['select'] = (addSelect)

    @select.deleter
    def select(self):
        del self.properties['select']
        self.properties['multiSelect'] = False
        
    # Query conditions such as join or setting a field in one table = to another.  
    @property    
    def queryConditions(self):
        return self.properties.get('queryConditions', None)
     
    @queryConditions.setter
    def queryConditions(self, addSelect):
        self.properties['queryConditions'] = (addSelect)

    @queryConditions.deleter
    def queryConditions(self):
        del self.properties['queryConditions']
        
    # Decorator to hold a returned row count variable  
    @property    
    def rowCount(self):
        return self.properties.get('rowCount', None)
     
    @rowCount.setter
    def rowCount(self, count):
        self.properties['rowCount'] = count

    @rowCount.deleter
    def rowCount(self):
        del self.properties['rowCount']
        
    # True of False Order by  
    @property    
    def orderBy(self):
        return self.properties.get('queryConditions', None)
     
    @orderBy.setter
    def orderBy(self, field):
        self.properties['orderBy'] = field

    @orderBy.deleter
    def orderBy(self):
        del self.properties['orderBy']
        
    

         
    # Class methods
    # initialization: Can configure all properties with included keyword arguments
    def __init__(self, **kwargs):
        self.properties = kwargs
        self.properties['queryConditions'] = False
        self.properties['multiSelect'] = False
        self.properties['queryReturn'] = False
        self.properties['restrict'] = False
        self.properties['orderBy'] = False
        self.properties['count'] = False
    
    # Connection call to set database
    def connect(self):
        print("Database connection established.")
        
        connectionString = "dbname=" + self.properties['dbname']
        return psycopg2.connect(connectionString)
    
    # Cursor call for queries
    def cursor(self, query):
        DB = self.connect()
        cursor = DB.cursor()
        
        print(query)
        cursor.execute(query)
        self.properties['rowCount'] = cursor.rowcount
        
        DB.commit()
        
        if self.properties['queryReturn'] == True:
            results = cursor.fetchall()
            
            
            return results
        
        DB.close()
        
    # Checks to see if restrictions are desired and iterates through the restricWhere list
    # to add if necessary.
    def checkForRestrictions(self, preQueryContent):
        
        if self.restrict == True:
            preQueryContent += " WHERE "
            # i is not used however is necessary for count_Where to work properly
            for count_WHERE, i in enumerate(self.properties['restrictWhere']):
                    if count_WHERE == (len(self.properties['restrictWhere'])-1):
                        preQueryContent += self.properties['restrictWhere'][count_WHERE][0] + " = '" + str(self.properties['restrictWhere'][count_WHERE][1])  + "' "
                    else:
                        preQueryContent += self.properties['restrictWhere'][count_WHERE][0] + " = '" + str(self.properties['restrictWhere'][count_WHERE][1])  + "' AND "
             
        
        return preQueryContent
    
    def setTables(self, preQueryContent):
        
        # i is not used however is necessary for count_Where to work properly
        for count_WHERE, i in enumerate(self.properties['tableName']):
            if count_WHERE == (len(self.properties['tableName'])-1):
                preQueryContent += self.properties['tableName'][count_WHERE] + " "
            else:
                preQueryContent += self.properties['tableName'][count_WHERE] + ", "
        
        return preQueryContent
    
    def setSelect(self, preQueryContent):
        print(self.properties)
        # i is not used however is necessary for count_Where to work properly
        for count_WHERE, i in enumerate(self.properties['select']):
            if count_WHERE == (len(self.properties['select'])-1):
                preQueryContent += self.properties['select'][count_WHERE] + " FROM "
            else:
                preQueryContent += self.properties['select'][count_WHERE] + ", "
        
        return preQueryContent
    
    def checkQueryConditions(self, preQueryContent):
        if self.queryConditions != False:
            # i is not used however is necessary for count_Where to work properly
            for count_WHERE, i in enumerate(self.properties['queryConditions']):
                if count_WHERE == (len(self.properties['queryConditions'])-1):
                    preQueryContent += self.properties['queryConditions'][count_WHERE][0] + " = " + str(self.properties['queryConditions'][count_WHERE][1])  + " "
                else:
                    preQueryContent += self.properties['queryConditions'][count_WHERE][0] + " = " + str(self.properties['queryConditions'][count_WHERE][1])  + ", "
        return preQueryContent
    
    def checkForOrderBy(self, preQueryContent):
        if self.properties['orderBy'] != False:
            preQueryContent += " ORDER BY " + self.properties['orderBy']
            
        return preQueryContent
        
    #CRUD Create, Read, Update, and Delete query creation methods to follow
    
    # Create: build INSERT query from args: insert_values tuple and insert_data tuple
    # Possibly switch values and data to decorator property?
    def create(self, insert_values, insert_data):
        
        queryContent1 = " INSERT INTO "
        
        queryContent = self.setTables(queryContent1) + " ("
        
        for count_values, v in enumerate(insert_values):
            if count_values == (len(insert_values)-1):
                queryContent += str(v) + ") VALUES("
            else:
                queryContent += str(v) + ", "
                
        for count_data, d in enumerate(insert_data):
            dString = str(d)
            # Replace any single quotes with escape single quote
            data = dString.replace("'", "")
            print(data)
            if count_data == (len(insert_data)-1):
                queryContent += "'" + data + "') RETURNING *;"
            else:
                queryContent += "'" + data + "', "
        
        results = self.cursor(queryContent)
        return results
    
    # Read: build READ query, can be run with restrictions if desired
    def read(self):
        
        if self.properties['multiSelect'] == True:
            queryContent1 = "SELECT "
            queryContent2 = self.setSelect(queryContent1)
        elif self.properties['count'] == True:
            queryContent2 = "SELECT count(*) FROM "
        else:
            queryContent2 = "SELECT * FROM "
            
        print queryContent2
            
        queryContent3 = self.setTables(queryContent2)
        
        queryContent4 = self.checkForRestrictions(queryContent3)
        
        queryContent5 = self.checkQueryConditions(queryContent4)
        
        queryContent6 = self.checkForOrderBy(queryContent5) + ";"
        
        self.properties['queryReturn'] = True
        results = self.cursor(queryContent6)
        
        return results
        
    # Update: build UPDATE query, can be run with restriction is desired
    def update(self, set_data):
        
        queryContent1 = "UPDATE "
        
        queryContent2 = self.setTables(queryContent1)
        
        queryContent2 += " SET " 
        
        if set_data != None:
            for count_data, d in enumerate(set_data):
                print(d)
                print(count_data)
                if count_data == (len(set_data)-1):
                    queryContent2 += str(d[0]) + " = '" + str(d[1]) + "' "
                else:
                    queryContent2 += str(d[0]) + " = '" + str(d[1]) + "', "
                
        queryContent3 = self.checkQueryConditions(queryContent2)

        queryContent4 = self.checkForRestrictions(queryContent3) + ";"
        
        results = self.cursor(queryContent4)
        return results
    
    # Delete: build DELETE query, can be run with restrictions if desired
    def delete(self):
         
        queryContent1 = "DELETE FROM "
        
        queryContent2 = self.setTables(queryContent1)
        
        queryContent3 = self.checkForRestrictions(queryContent2) + ";"
        
        self.cursor(queryContent3)
        