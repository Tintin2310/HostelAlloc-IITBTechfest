# HostelAlloc-IITBTechfest

This web development project is part of the Techfest IITB Campus Ambassador Internship.

# Room Allocation Web Application

This web application facilitates the digitalization of the hospitality process for group accommodation. It allows users to upload two CSV files containing group information and hostel room details. The application then allocates rooms based on specified criteria and provides a visual and downloadable allocation summary.

## Features

- **Upload CSV Files**: Users can upload two CSV files:
  - `group.csv`: Contains information about groups, including Group ID, number of members, and gender composition.
  - `hostel.csv`: Provides details about hostel rooms, including Hostel Name, Room Number, capacity, and gender accommodation.

- **Room Allocation Algorithm**: Allocates rooms based on the following criteria:
  - Members of the same group (same Group ID) are accommodated together.
  - Boys and girls are allocated to their respective hostels based on gender accommodation.
  - Room capacity constraints are adhered to.

- **User Interface**:
  - **Index Page**: Allows users to upload CSV files.
  - **Allocation Page**: Displays a table showing which group members are allocated to which room, along with a download link for the allocation details in CSV format.

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your/repository.git
   cd repository-folder

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Run the Application**:
   ```bash
   python app.py

## Usage

### Upload CSV Files:
1. **Navigate to the home page (`/`)** and upload `group.csv` and `hostel.csv`.

### View Allocation:
2. After uploading files, **navigate to the allocation page (`/allocation`)** to view the room allocation details.
3. **Download** the allocation details in CSV format using the provided link.

## Technologies Used

- **Python**: Backend logic and web server using Flask.
- **HTML/CSS**: Frontend templates styled for user interaction.
- **CSV Parsing**: Processing uploaded files to allocate rooms.
