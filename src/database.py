import pymysql
from langchain.schema import Document

class DatabaseLoader:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
        return self.connection

    def load_documents(self):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sales")
        rows = cursor.fetchall()
        cursor.close()
        
        documents = []
        for row in rows:
            page_content = ", ".join([f"{key}: {value}" for key, value in row.items()])
            documents.append(Document(page_content=page_content))
            
        return documents
