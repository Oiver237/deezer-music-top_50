import unittest
import os
from datetime import datetime
import csv
from script2 import check_directories, log_processing, top_50

class TestMusicProcessing(unittest.TestCase):

    def setUp(self):
        # Create sample data for testing
        self.date_str = (datetime.now().strftime("%Y%m%d"))
        self.log_file = f'/home/lifu237/deezer-interview/logs/listen-{self.date_str}.log'
        self.staging_file = f'/home/lifu237/deezer-interview/staging/counts-{self.date_str}.csv'
        self.output_file = f'/home/lifu237/deezer-interview/output/country_top50_{self.date_str}.txt'
        
        os.makedirs('logs', exist_ok=True)
        with open(self.log_file, 'w') as log:
            writer = csv.writer(log, delimiter='|')
            writer.writerow(['1', '1', 'US'])  
            writer.writerow(['2', '2', 'US'])  
            writer.writerow(['1', '3', 'US'])  
            writer.writerow(['3', '4', 'GB']) 
            writer.writerow(['4', '5', 'GB']) 
            writer.writerow(['4', '6', 'GB']) 
            writer.writerow(['1', '7', 'GB']) 
            # Corrupted rows
            writer.writerow(['1', '5']) 
            writer.writerow(['2', '10', 'USA']) 

    def cleanUp(self):
        # Clean up the files after tests
        os.remove(self.log_file)
        if os.path.exists(self.staging_file):
            os.remove(self.staging_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        os.rmdir('logs')

    def test_ensure_directories(self):
        # Test if the directories exist
        check_directories()
        self.assertTrue(os.path.exists('staging'))
        self.assertTrue(os.path.exists('output'))

    def test_log_processing(self):
        # Test the log processing function
        check_directories()
        log_processing(self.date_str)
        self.assertTrue(os.path.exists(self.staging_file))

        with open(self.staging_file, 'r') as file:
            reader = csv.reader(file)
            counts = {row[0]: {row[1]: int(row[2])} for row in reader}
        
        self.assertEqual(counts['US']['1'], 2) 
        self.assertEqual(counts['US']['2'], 1) 
        self.assertEqual(counts['GB']['3'], 1) 
        self.assertEqual(counts['GB']['4'], 2) 
    
    def test_top_50(self):
        # Test the top 50 function
        check_directories()
        log_processing(self.date_str)
        top_50(self.date_str)
        self.assertTrue(os.path.exists(self.output_file))

        with open(self.output_file, 'r') as file:
            lines = file.readlines()
        
        self.assertIn('US|1:2,2:1\n', lines) 
        self.assertIn('GB|4:2,3:1,1:1\n', lines) 
    

if __name__ == '__main__':
    unittest.main()
