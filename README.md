# unimelb-subject-scraper
Simple code to retrieve data containing University of Melbourne subjects, their faculties, and availability.

To run this code, simply run script.py. Make sure you installed all the necessary libraries.
Make sure faculties.xml is also in the same directory.

You can change the contents of the csv output by going to this link;
https://handbook.unimelb.edu.au/search?types%5B%5D=subject&year=2021&level_type%5B%5D=all&campus_and_attendance_mode%5B%5D=all&org_unit%5B%5D=all&page=1&sort=_score%7Cdesc
and apply the desird filters. Proceed to change the sorting to Name(ascending) and copy the link.
Replace the link in line 106 with the copied link and run the code.
