# log-monitoring
This application reads a log file, tracks job execution times, and generates warnings or errors if jobs exceed specific duration thresholds(5 minutes for WARNING,10 minutes for ERROR).
Steps:
Parses CSV formatted log files
Tracks start and end times for each job
Calculates job durations
Generates warnings for jobs taking longer than 5 minutes
Generates errors for jobs taking longer than 10 minutes
Identifies incomplete jobs (those without an END entry)
Generates detailed reports both to console and file

How to run the script:
python3 log_monitor.py logs.log

The program generates:

Console output with job statistics
A file named monitoring_report.txt with the same information

Log File Format
The expected log file format is CSV with the following columns:

Timestamp (HH:MM:SS)
Job description
Status (START or END)
Process ID (PID)

Example:
11:35:23,scheduled task 032, START,37980
11:35:56,scheduled task 032, END,37980