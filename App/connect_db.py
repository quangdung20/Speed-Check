from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Thêm dòng này để cho phép CORS

@app.route('/api/speed_data', methods=['GET'])
def get_speed_data():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    conn = sqlite3.connect('speed_data.db')
    cursor = conn.cursor()
    
    # Truy vấn gần đúng nhất
    query = '''
    SELECT time, speed_real_right, speed_set_right, speed_real_left, speed_set_left 
    FROM speed_data 
    WHERE time >= ? AND time <= ? 
    ORDER BY ABS(strftime('%s', time) - strftime('%s', ?))
    '''
    cursor.execute(query, (start_time, end_time, start_time))
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return jsonify({"message": "No data found"}), 404
    
    data = []
    for row in rows:
        data.append({
            'time': row[0],
            'speed_real_right': row[1],
            'speed_set_right': row[2],
            'speed_real_left': row[3],
            'speed_set_left': row[4]
        })
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000)
