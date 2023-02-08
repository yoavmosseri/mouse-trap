import sqlite3
from dot import Dot
from user import User
import numpy as np
class DotORM():
    def __init__(self):
        self.conn = None  # will store the DB connection
        self.cursor = None   # will store the DB connection cursor

    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect('data\\test.db')
        self.current = self.conn.cursor()

    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    # All read SQL

    def get_neural_network(self, id:int):
        """"
        if network exists return network
        if not return false
        """
        self.open_DB()
        sql = f"SELECT network FROM network WHERE id = {id};"
        res = self.current.execute(sql)
        network = res.fetchall()
        if network == []:
            network = False
        else:
            network = network[0][0]
        
        self.close_DB()
        return network

    def is_admin(self, username):
        """"
        if user exists return his password
        if not return false
        """
        self.open_DB()
        id = self.get_id(username)
        
        self.close_DB()
        return id == 0

    def get_user_password(self, username):
        """"
        if user exist return his password
        if not return false
        """
        self.open_DB()

        sql = f"SELECT password FROM users WHERE username = '{username}';"
        res = self.current.execute(sql)
        password = res.fetchall()
        if password == []:
            password = False
        else:
            password = password[0][0]


        self.close_DB()
        return password



    def insert_user(self, u: User):
        self.open_DB()

        sql = "SELECT MAX(id) FROM users;"
        res = self.current.execute(sql)
        id = res.fetchall()[0][0]+1

        sql = "INSERT INTO users (username, password, email ,id)"
        sql += f" VALUES ('{u.username}','{u.password}','{u.email}',{id});"
        res = self.current.execute(sql)
       
        self.commit()
        self.close_DB()

        return True

    def get_id(self, username):

        sql = f"SELECT id FROM users WHERE username = '{username}';"
        res = self.current.execute(sql)
        id = res.fetchall()[0][0]
        return id

    def get_user_data(self, username):
        self.open_DB()
        id = self.get_id(username)

        sql = f"SELECT x,y,v FROM motion WHERE id = {id};"
        res = self.current.execute(sql)
        id = res.fetchall()

        self.close_DB()
        return np.array(id)

    def get_others_data(self, username):
        self.open_DB()
        id = self.get_id(username)

        sql = f"SELECT x,y,v FROM motion WHERE id != {id};"
        res = self.current.execute(sql)
        id = res.fetchall()

        self.close_DB()
        return np.array(id)


    def insert_dot(self,username, d:Dot):
        self.open_DB()

        id = self.get_id(username)

        sql = "INSERT INTO motion (id, x, y, v)"
        sql += f" VALUES ({id},{d.x},{d.y},{d.v});"
        res = self.current.execute(sql)
       
        self.commit()
        self.close_DB()

        return True
        



def main_test():
    
    db = DotORM()
    print('a' == False)
    #data = db.get_all_players_in_a_team(1)
    #db.delete_player(1,24)
    #data = db.count_teams()
    #print(data)
    


if __name__ == "__main__":
    main_test()
