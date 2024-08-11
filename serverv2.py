import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import socket
import sqlite3
from datetime import datetime

# Server configuration
HOST = '127.0.0.1'
PORT = 6543

# Create and configure the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)  # Backlog parameter (number of queued connections)

print("Server listening on {}:{}".format(HOST, PORT))

conn, addr = s.accept()

# Initialize the plot with two subplots in a 1x2 grid
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Data containers for 4 different graphs
xdata = {i: [] for i in range(4)}
ydata = {i: [] for i in range(4)}

line_names = ["Set Value", "Real Value"]

# Create line objects for each subplot
lines = [ax.plot([], [], label=line_name)[0] for ax in axs for line_name in line_names]

# Setting up the plot limits and labels
def init():
    for ax in axs:
        ax.set_xlim(0, 10)  # Initial x-limit
        ax.set_ylim(0, 30)  # Adjust y-limit as necessary
        ax.legend(loc='upper left')
    return lines

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

# Function to update the plot
def update(frame):
    try:
        data = conn.recv(1024).decode('utf-8').strip()  # Receive and strip any extra whitespace
        if data:
            if ',' in data:
                parent_parts = data.split(';')
                for x in parent_parts:
                    parts = x.split(',')
                    if len(parts) == 4:
                        # Extract numeric values
                        values = [float(value) for value in parts]
                        
                        # Append new data to plot
                        for i, value in enumerate(values):
                            xdata[i].append(frame)
                            ydata[i].append(value)
                            
                            # Trim data to keep it within a visible range
                            max_points = 100  # Number of data points to display at a time
                            if len(xdata[i]) > max_points:
                                xdata[i] = xdata[i][-max_points:]
                                ydata[i] = ydata[i][-max_points:]
                            
                            lines[i].set_data(xdata[i], ydata[i])
                        
                        # Insert data into the database
                        timestamp = datetime.now()  # Capture current timestamp
                        insert_data(timestamp, values[0], values[1], values[2], values[3])
                        
                        # Update x and y limits
                        for ax in axs:
                            if len(xdata[0]) > 0:
                                ax.set_xlim(xdata[0][0], xdata[0][-1] + 1)
                                    
                    else:
                        print("Unexpected number of values:", data)
            else:
                print("Received data is not in expected format:", data)
    except socket.error as e:
        print("Socket error:", e)
        plt.close(fig)  # Close the plot window
    except Exception as e:
        print("Error:", e)
        plt.close(fig)  # Close the plot window
    return lines

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 10, 100),
                              init_func=init, blit=True, interval=50)

plt.show()

# Clean up the connection when done
conn.close()
s.close()
