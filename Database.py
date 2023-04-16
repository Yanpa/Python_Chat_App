import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
                dbname="chatapp",
                user="panayotyanev",
                password="123",
                host="localhost",
                port="5432"
            )

        self.cur = self.conn.cursor()

    def commit_to_db(self):
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def check_user_credentials(self, username, password):
        self.cur.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        
        user = self.cur.fetchone()

        return user
    
    def check_if_username_exist(self, username):
        self.cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        return self.cur.fetchone() is not None

    def check_if_email_is_used(self, email):
        self.cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        return self.cur.fetchone() is not None
    
    def create_new_user(self, username, email, password):
        self.cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        self.commit_to_db()


    def return_all_users_friends(self, username):
        self.cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        self.current_user_info = self.cur.fetchone()

        self.cur.execute("SELECT friend_id FROM friends WHERE user_id = %s", (self.current_user_info[0],))
        friend_ids = self.cur.fetchall()

        friends = []
        for friend_id in friend_ids:
            self.cur.execute("SELECT username FROM users WHERE id = %s", (friend_id[0],))
            friends.append(self.cur.fetchone())

        return friends
    
    def add_friend(self, username, toplevel):
        self.cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        new_friend = self.cur.fetchone()

        if new_friend is None:
            return 
        else:
            self.cur.execute("INSERT INTO friends (user_id, friend_id) VALUES (%s, %s)", (self.current_user_info[0], new_friend[0]))
            self.conn.commit()

            toplevel.destroy()

            return True
            

    def show_updated_chat(self, selected_friend, chat_history):
        try:
            self.cur.execute("SELECT id FROM users WHERE username = %s", (selected_friend,))
            friend_id = self.cur.fetchone()
            
            self.cur.execute("SELECT sender_id, message, timestamp FROM messages WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s) ORDER BY timestamp ASC", (self.current_user_info[0], friend_id[0], friend_id[0], self.current_user_info[0]))
            rows = self.cur.fetchall()
            for row in rows:
                sender_id, message, _ = row
                if sender_id == self.current_user_info[0]:
                    chat_history.insert("end", "You:\n{: <8}{}\n\n".format("", message), "right")
                else:
                    chat_history.insert("end", f"{selected_friend}:\n\t{message}\n\n")
        except (Exception, psycopg2.Error) as error:
            print(f"Error while fetching chat history: {error}")
            self.chat_history.insert("end", f"Error while fetching chat history: {error}\n")


    def import_message_in_db(self, receiver, message):
        self.cur.execute("SELECT id FROM users WHERE username = %s", (receiver,))
        friend_id = self.cur.fetchone()

        self.cur.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)", (self.current_user_info[0], friend_id[0], message))
        self.commit_to_db()