import csv
from datetime import datetime
import sys

class LogMonitor:
    def __init__(self, log_file_path):
        """Initialize the LogMonitor with the path to the log file."""
        self.log_file_path = log_file_path
        self.jobs = {}
        self.completed_jobs = []
        self.warning_threshold = 5 * 60  # 5 minutes
        self.error_threshold = 10 * 60   # 10 minutes

    def parse_log_file(self):
        """Parse the log file and process each entry."""
        try:
            with open(self.log_file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 4:
                        continue
                    
                    timestamp, job_description, status, pid = row
                    
                    self.process_log_entry(timestamp, job_description, status, pid)
        except FileNotFoundError:
            print(f"Error: File '{self.log_file_path}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error parsing log file: {e}")
            sys.exit(1)

    def process_log_entry(self, timestamp, job_description, status, pid):
        """Process a single log entry."""
        job_id = f"{job_description.strip()}-{pid.strip()}"
        
        time_obj = datetime.strptime(timestamp.strip(), "%H:%M:%S")
        
        if status.strip() == "START":
            self.jobs[job_id] = {
                'description': job_description.strip(),
                'pid': pid.strip(),
                'start_time': time_obj
            }
        elif status.strip() == "END":
            if job_id in self.jobs:
                start_time = self.jobs[job_id]['start_time']
                duration_seconds = (time_obj - start_time).seconds
                
                self.completed_jobs.append({
                    'job_id': job_id,
                    'description': self.jobs[job_id]['description'],
                    'pid': pid.strip(),
                    'start_time': start_time,
                    'end_time': time_obj,
                    'duration_seconds': duration_seconds
                })
                
                self.jobs.pop(job_id)

    def generate_report(self):
        """Generate a report of job durations with warnings and errors."""
        print("\nJOB MONITORING REPORT")
        print("=====================")
        print(f"Total jobs completed: {len(self.completed_jobs)}")
                
        print("\nJOB DETAILS:")
        print("===========")
        
        for job in self.completed_jobs:
            duration_min = job['duration_seconds'] / 60
            status = "OK"
            
            if job['duration_seconds'] > self.error_threshold:
                status = "ERROR"
            elif job['duration_seconds'] > self.warning_threshold:
                status = "WARNING"
                
            print(f"{job['description']} (PID: {job['pid']}):")
            print(f"  Start: {job['start_time'].strftime('%H:%M:%S')}")
            print(f"  End: {job['end_time'].strftime('%H:%M:%S')}")
            print(f"  Duration: {duration_min:.2f} minutes ({job['duration_seconds']} seconds)")
            print(f"  Status: {status}")
            print()
        
        if self.jobs:
            print("\nINCOMPLETE JOBS:")
            print("===============")
            for job_id, job_info in self.jobs.items():
                print(f"{job_info['description']} (PID: {job_info['pid']})")
                print(f"  Started at: {job_info['start_time'].strftime('%H:%M:%S')}")
                print(f"  Status: INCOMPLETE - No END entry found")
                print()

    def save_report_to_file(self, output_path="monitoring_report.txt"):
        """Save the report to a file."""
        original_stdout = sys.stdout
        try:
            with open(output_path, 'w') as f:
                sys.stdout = f
                self.generate_report()
            print(f"Report saved to {output_path}")
        finally:
            sys.stdout = original_stdout

def main():
    if len(sys.argv) < 2:
        print("Usage: python log_monitor.py <log_file_path>")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    monitor = LogMonitor(log_file_path)
    monitor.parse_log_file()
    monitor.generate_report()
    monitor.save_report_to_file()

if __name__ == "__main__":
    main()