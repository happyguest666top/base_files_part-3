import sqlite3


db_name = "quiz.db"
conn = None
cursor = None




def open():
   global conn, cursor
   conn = sqlite3.connect(db_name)
   cursor = conn.cursor()




def close():
   cursor.close()
   conn.close()




def do(query):
    cursor.execute(query)
    conn.commit()




def clear_db():
   ''' видаляє всі таблиці '''
   open()
   query = '''DROP TABLE IF EXISTS quiz_content'''
   do(query)
   query = '''DROP TABLE IF EXISTS question'''
   do(query)
   query = '''DROP TABLE IF EXISTS quiz'''
   do(query)
   close()

def show(table):
   query = 'SELECT * FROM ' + table
   open()
   cursor.execute(query)
   print(cursor.fetchall())
   close()




def show_tables():
   show('question')
   show('quiz')
   show('quiz_content')






# task 1: Створення таблиць та опис зв'язків між ними
def create():
   open()
   cursor.execute('''PRAGMA foreign_keys=on''')
   do('''CREATE TABLE IF NOT EXISTS quiz (id INTEGER PRIMARY KEY, name VARCHAR)''')

   do('''CREATE TABLE IF NOT EXISTS question (id INTEGER PRIMARY KEY, question VARCHAR,answer VARCHAR, wrong1 VARCHAR, wrong2 VARCHAR, wrong3 VARCHAR)''')

   do('''CREATE TABLE IF NOT EXISTS quiz_content (id INTEGER PRIMARY KEY, quiz_id INTEGER, FOREIGN KEY (quiz_id) REFERENCES quiz (id), FOREIGN KEY (question_id) REFERENCES question (id) )''')
   close()



# task 2: Заповнення таблиць даними
def add_questions():
   questions =[('Коли у тебе вперше зявляються друзі?', 'садочок', 'школа', 'інститут', 'на_бали')
      , ('Яка вода не провидить струм?', 'Дисталіціона', 'звичайна', 'з_джерел', 'з_марсу'),
               ('Чи складна тема база даних?', 'Ні_не_складна', 'Складна', 'Средне', 'Легка')
    ]
   open()
   cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
   conn.commit()
   close()
def add_quiz():
   quizes = [
      ('Кахут',),
      ('Хто хоче стати мільйлонером?',),
      ('Найрозумніший',),
      ('Хто зверху?',)
   ]
   open()
   cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
   conn.commit()
   close()


def add_links():

      open()
      cursor.execute('''PRAGMA foreign_keys=on''')
      query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
      answer = input("Додати зв'язок (y / n)?")
      while answer != 'n':
         quiz_id = int(input("id вікторини: "))
         question_id = int(input("id питання: "))
         cursor.execute(query, [quiz_id, question_id])
         conn.commit()
         answer = input("Додати зв'язок (y / n)?")
      close()


# task 3: Отримання тексту запитання та варіантів відповідей
def get_question_after(question_id=0, quiz_id=1):
   ''' повертає наступне питання після запитання з переданим id
    для першого запитання передається значення за замовчуванням '''
   open()
   query = '''
       SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
       FROM question, quiz_content
       WHERE quiz_content.question_id == question.id
       AND quiz_content.id == ? AND quiz_content.quiz_id == ?
       ORDER BY quiz_content.id '''
   cursor.execute(query, [question_id, quiz_id])
   result = cursor.fetchone()
   close()
   return result


# task 3: Отримання тексту запитання та варіантів відповідей






def main():
   clear_db()
   create()
   add_questions()
   add_quiz()
   add_links()
   show_tables()
   # Виведення в консоль питання з id=3, id вікторини = 1
   print(get_question_after(3, 1))




if __name__ == "__main__":
   main()
