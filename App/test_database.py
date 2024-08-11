import sqlite3
import random
from datetime import datetime, timedelta
conn = sqlite3.connect('speed_data.db')

# Tạo con trỏ để thực hiện các thao tác trên database
cursor = conn.cursor()
 
# creadte table
# cursor.execute('''CREATE TABLE IF NOT EXISTS speed_data (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     time TEXT,
#                     speed_real_right REAL,
#                     speed_set_right REAL,
#                     speed_real_left REAL,
#                     speed_set_left REAL
#                 )''')


# # Dữ liệu mẫu
# data = {
#     'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#     'speed_real_right': 30.5,
#     'speed_set_right': 32.0,
#     'speed_real_left': 28.0,
#     'speed_set_left': 30.0
# }

# # Chèn dữ liệu vào bảng
# cursor.execute('''INSERT INTO speed_data (time, speed_real_right, speed_set_right, speed_real_left, speed_set_left)
#                   VALUES (:time, :speed_real_right, :speed_set_right, :speed_real_left, :speed_set_left)''', data)

# start_time = '2024-08-10 00:00:00'
# end_time = '2024-08-10 23:59:59'
speed_real_left = 32.0

cursor.execute('''SELECT * FROM speed_data''')

# In kết quả
rows = cursor.fetchall()
for row in rows:
    print(row)

# # Hàm tạo dữ liệu ngẫu nhiên
# def generate_random_data(num_records):
#     data = []
#     current_time = datetime.now()

#     for _ in range(num_records):
#         # Tạo thời gian ngẫu nhiên cách nhau 1-10 phút
#         current_time += timedelta(minutes=random.randint(1, 10))
        
#         # Tạo giá trị tốc độ ngẫu nhiên
#         speed_real_right = round(random.uniform(10, 30), 2)
#         speed_set_right = round(random.uniform(10, 30), 2)
#         speed_real_left = round(random.uniform(10, 30), 2)
#         speed_set_left = round(random.uniform(10, 30), 2)
        
#         # Thêm vào danh sách dữ liệu
#         data.append((current_time.strftime('%Y-%m-%d %H:%M:%S'), 
#                      speed_real_right, 
#                      speed_set_right, 
#                      speed_real_left, 
#                      speed_set_left))
#     return data

# # Sinh 100 bản ghi
# data = generate_random_data(100)

# # Chèn dữ liệu vào bảng
# cursor.executemany('''
# INSERT INTO speed_data (time, speed_real_right, speed_set_right, speed_real_left, speed_set_left)
# VALUES (?, ?, ?, ?, ?)
# ''', data)



# print("100 records have been successfully inserted into the database.")

# Commit các thay đổi và đóng kết nối
conn.commit()
conn.close()