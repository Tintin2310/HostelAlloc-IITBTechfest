from flask import Flask, request, redirect, url_for, render_template, make_response
import csv
import os
from io import StringIO

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def read_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        data = [dict((k.strip(), v.strip()) for k, v in row.items()) for row in csv_reader]
    return data

def allocate_rooms(group_data, hostel_data):
    allocation = []
    hostel_rooms = {hostel['Hostel Name']: [] for hostel in hostel_data}

    for hostel in hostel_data:
        hostel_rooms[hostel['Hostel Name']].append({
            'Room Number': hostel['Room Number'],
            'Capacity': int(hostel['Capacity']),
            'Gender': hostel['Gender'],
            'Allocated': 0,
            'Group ID': None
        })

    for group in group_data:
        try:
            group_id = group['Group ID']
            members = int(group['Members'])
            gender = group['Gender']
        except KeyError as e:
            print(f"KeyError: Missing key {e} in group data {group}")
            continue

        allocated = False
        for hostel_name, rooms in hostel_rooms.items():
            for room in rooms:
                if room['Gender'] == gender and room['Allocated'] == 0 and room['Capacity'] >= members:
                    room['Allocated'] = members
                    room['Group ID'] = group_id
                    allocation.append({
                        'Group ID': group_id,
                        'Hostel Name': hostel_name,
                        'Room Number': room['Room Number'],
                        'Members Allocated': members
                    })
                    allocated = True
                    break
            if allocated:
                break
        if not allocated:
            print(f"Could not allocate Group ID {group_id}")

    return allocation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    group_file = request.files['group_file']
    hostel_file = request.files['hostel_file']
    if group_file and hostel_file:
        group_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'group.csv'))
        hostel_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'hostel.csv'))
        return redirect(url_for('allocate_rooms_view'))
    return 'File upload failed', 400

@app.route('/allocate')
def allocate_rooms_view():
    group_data = read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'group.csv'))
    hostel_data = read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'hostel.csv'))
    allocation = allocate_rooms(group_data, hostel_data)
    return render_template('allocation.html', allocation=allocation)

@app.route('/download')
def download_csv():
    group_data = read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'group.csv'))
    hostel_data = read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'hostel.csv'))
    allocation = allocate_rooms(group_data, hostel_data)
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Group ID', 'Hostel Name', 'Room Number', 'Members Allocated'])
    for item in allocation:
        cw.writerow([item['Group ID'], item['Hostel Name'], item['Room Number'], item['Members Allocated']])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=allocation.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(debug=True)
