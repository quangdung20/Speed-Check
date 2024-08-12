# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import numpy as np
# import socket
# import sqlite3
# from datetime import datetime

# # Server configuration
# HOST = '127.0.0.1'
# PORT = 6543

# # Create and configure the socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(1)  # Backlog parameter (number of queued connections)

# print("Server listening on {}:{}".format(HOST, PORT))

# conn, addr = s.accept()

# # Initialize the plot with two subplots in a 1x2 grid
# fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# # Data containers for 4 different graphs
# xdata = {i: [] for i in range(4)}
# ydata = {i: [] for i in range(4)}

# line_names = ["Set Value", "Real Value"]

# # Create line objects for each subplot
# lines = [ax.plot([], [], label=line_name)[0] for ax in axs for line_name in line_names]

# # Setting up the plot limits and labels
# def init():
#     for ax in axs:
#         ax.set_xlim(0, 10)  # Initial x-limit
#         ax.set_ylim(0, 30)  # Adjust y-limit as necessary
#         ax.legend(loc='upper left')
#     return lines

# # Function to insert data into SQLite database
# def insert_data(timestamp, speed_real_right, speed_set_right, speed_real_left, speed_set_left):
#     conn = sqlite3.connect('speed_data.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO speed_data (time, speed_real_right, speed_set_right, speed_real_left, speed_set_left)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (timestamp, speed_real_right, speed_set_right, speed_real_left, speed_set_left))
#     conn.commit()
#     conn.close()

# # Function to update the plot
# def update(frame):
#     try:
#         data = conn.recv(1024).decode('utf-8').strip()  # Receive and strip any extra whitespace
#         if data:
#             if ',' in data:
#                 parent_parts = data.split(';')
#                 for x in parent_parts:
#                     parts = x.split(',')
#                     if len(parts) == 4:
#                         # Extract numeric values
#                         values = [float(value) for value in parts]
                        
#                         # Append new data to plot
#                         for i, value in enumerate(values):
#                             xdata[i].append(frame)
#                             ydata[i].append(value)
                            
#                             # Trim data to keep it within a visible range
#                             max_points = 100  # Number of data points to display at a time
#                             if len(xdata[i]) > max_points:
#                                 xdata[i] = xdata[i][-max_points:]
#                                 ydata[i] = ydata[i][-max_points:]
                            
#                             lines[i].set_data(xdata[i], ydata[i])
                        
#                         # Insert data into the database
#                         timestamp = datetime.now()  # Capture current timestamp
#                         insert_data(timestamp, values[0], values[1], values[2], values[3])
                        
#                         # Update x and y limits
#                         for ax in axs:
#                             if len(xdata[0]) > 0:
#                                 ax.set_xlim(xdata[0][0], xdata[0][-1] + 1)
                                    
#                     else:
#                         print("Unexpected number of values:", data)
#             else:
#                 print("Received data is not in expected format:", data)
#     except socket.error as e:
#         print("Socket error:", e)
#         plt.close(fig)  # Close the plot window
#     except Exception as e:
#         print("Error:", e)
#         plt.close(fig)  # Close the plot window
#     return lines

# # Create the animation
# ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 10, 100),
#                               init_func=init, blit=True, interval=50)

# plt.show()

# # Clean up the connection when done
# conn.close()
# s.close()


# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import numpy as np
# import socket
# import sqlite3
# from datetime import datetime

# # Server configuration
# HOST = '127.0.0.1'
# PORT = 6543

# # Create and configure the socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(1)

# print("Server listening on {}:{}".format(HOST, PORT))

# conn, addr = s.accept()

# # Initialize the plot with two subplots in a 1x2 grid
# fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# # Data containers for 4 different graphs
# xdata = {i: [] for i in range(4)}
# ydata = {i: [] for i in range(4)}

# line_names = ["Set Value", "Real Value"]

# # Create line objects for each subplot
# lines = [ax.plot([], [], label=line_name)[0] for ax in axs for line_name in line_names]

# # Setting up the plot limits and labels
# def init():
#     for ax in axs:
#         ax.set_xlim(0, 10)  # Initial x-limit
#         ax.set_ylim(0, 30)  # Adjust y-limit as necessary
#         ax.legend(loc='upper left')
#     return lines

# # Function to insert data into SQLite database
# def insert_data(timestamp, speed_real_right, speed_set_right, speed_real_left, speed_set_left):
#     try:
#         conn = sqlite3.connect('speed_data.db')
#         cursor = conn.cursor()
#         cursor.execute('''
#             INSERT INTO speed_data (time, speed_real_right, speed_set_right, speed_real_left, speed_set_left)
#             VALUES (?, ?, ?, ?, ?)
#         ''', (timestamp, speed_real_right, speed_set_right, speed_real_left, speed_set_left))
#         conn.commit()
#     except sqlite3.Error as e:
#         print("SQLite error:", e)
#     finally:
#         conn.close()

# # Function to receive complete data packet
# def receive_data(connection):
#     buffer = ""
#     while True:
#         try:
#             chunk = connection.recv(1024).decode('utf-8')
#             if not chunk:
#                 break
#             buffer += chunk
#             if ';' in buffer:
#                 packets = buffer.split(';')
#                 buffer = packets.pop(-1)
#                 for packet in packets:
#                     yield packet.strip()
#         except socket.error as e:
#             print("Socket error:", e)
#             break

# # Function to update the plot
# def update(frame):
#     try:
#         for data in receive_data(conn):
#             print(data)
#             if ',' in data:
#                 parts = data.split(',')
#                 if len(parts) == 4:
#                     values = [float(value) for value in parts]
                    
#                     # Append new data to plot
#                     for i, value in enumerate(values):
#                         xdata[i].append(frame)
#                         ydata[i].append(value)
                        
#                         # Trim data to keep it within a visible range
#                         max_points = 100
#                         if len(xdata[i]) > max_points:
#                             xdata[i] = xdata[i][-max_points:]
#                             ydata[i] = ydata[i][-max_points:]
                        
#                         lines[i].set_data(xdata[i], ydata[i])
                    
#                     # Insert data into the database
#                     # timestamp = datetime.now()
#                     # insert_data(timestamp, values[0], values[1], values[2], values[3])
                    
#                     # Update x and y limits
#                     for ax in axs:
#                         if len(xdata[0]) > 0:
#                             ax.set_xlim(xdata[0][0], xdata[0][-1] + 1)
                                
#                 else:
#                     print("Unexpected number of values:", data)
#             else:
#                 print("Received data is not in expected format:", data)
#     except Exception as e:
#         print("Error during update:", e)
#         plt.close(fig)
#     return lines

# # Create the animation
# ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 10, 100),
#                               init_func=init, blit=True, interval=50)

# plt.show()

# # Clean up the connection when done
# conn.close()
# s.close()
import socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re
import threading
from datetime import datetime
import sqlite3

# Khởi tạo server socket
HOST = '127.0.0.1'
PORT = 6543

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Listening on {HOST}:{PORT}")

# Biến để lưu trữ dữ liệu theo thời gian thực và khóa để bảo vệ chúng
time_values = []
L1_values = []
R1_values = []
L2_values = []
R2_values = []

data_lock = threading.Lock()

# Hàm để phân tích chuỗi dữ liệu nhận được
def parse_data(data):
    match = re.match(r"(\d+),(\d+),(\d+),(\d+);", data)
    if match:
        L1, R1, L2, R2 = map(int, match.groups())
        return L1, R1, L2, R2
    return None


# Function to insert data into SQLite database
def insert_data(timestamp, speed_real_right, speed_set_right, speed_real_left, speed_set_left):
    conn = sqlite3.connect('speed_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO speed_data (time, speed_real_right, speed_set_right, speed_real_left, speed_set_left)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, speed_real_right, speed_set_right, speed_real_left, speed_set_left))
    conn.commit()
    conn.close()

# Thiết lập đồ thị
fig, (ax1, ax2) = plt.subplots(2, 1)

def update_plot(frame):
    with data_lock:
        ax1.clear()
        ax2.clear()
        ax1.plot(time_values, L1_values, label='L1')
        ax1.plot(time_values, R1_values, label='R1')
        ax2.plot(time_values, L2_values, label='L2')
        ax2.plot(time_values, R2_values, label='R2')
        
        ax1.legend()
        ax2.legend()

# Hàm để nhận dữ liệu từ client và cập nhật đồ thị
def receive_data():
    try:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            
            result = parse_data(data)
            if result:
                L1, R1, L2, R2 = result
                with data_lock:
                    current_time = datetime.now()  # Lấy thời gian thực tại thời điểm nhận dữ liệu
                    time_values.append(current_time)
                    L1_values.append(L1)
                    R1_values.append(R1)
                    L2_values.append(L2)
                    R2_values.append(R2)

                    insert_data(current_time, R1, L1, R2, L2)

                print(f"Received data at {current_time}: L1={L1}, R1={R1}, L2={L2}, R2={R2}")
    except KeyboardInterrupt:
        print("Server is stopping...")
    finally:
        conn.close()

# Chạy hàm nhận dữ liệu trong một luồng riêng
try:
    thread = threading.Thread(target=receive_data)
    thread.start()

    # Khởi động cập nhật đồ thị theo thời gian thực
    ani = FuncAnimation(fig, update_plot, interval=1000, cache_frame_data=False)
    plt.show()

except KeyboardInterrupt:
    print("Exiting server...")

finally:
    server_socket.close()