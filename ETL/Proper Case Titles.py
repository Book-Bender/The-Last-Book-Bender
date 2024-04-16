import csv

# Open the input file
with open('Data/gutenberg_books.txt', 'r') as input_file:
    reader = csv.DictReader(input_file)
    
    # Open the output file
    with open('gutenberg_books_processed.txt', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
        
        # Write the header row
        writer.writeheader()
        
        # Iterate through the rows and capitalize the title and author fields
        for row in reader:
            row['title'] = row['title'].title()
            row['authors'] = row['authors'].title()
            writer.writerow(row)