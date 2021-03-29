from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    
    direct = os.path.dirname(filename)
    pathway = os.path.join(direct, filename)
    f = open(pathway, 'r', encoding= 'utf-8')
    url = f.read()
    f.close()

    info_list = [] 

    soup = BeautifulSoup(url, 'html.parser')

    tags = soup.find_all('a', class_= 'bookTitle')
    title_list = []
    for tag in tags:
        span = tag.find('span')
        title = span.get_text()
        title = title.strip()
        title_list.append(title)
    
    tags = soup.find_all('div', class_= 'authorName__container')
    author_list = []
    for tag in tags:
        span = tag.find('span')
        author = span.get_text()
        author = author.strip()
        author_list.append(author)
     
    # loop through each book 
   
    for i in range(len(title_list)):
        tup = (title_list[i], author_list[i])
        info_list.append(tup)
   

    return info_list

    pass

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    
    tags = soup.find_all('a', class_= 'bookTitle')
    link_list = []
    for tag in tags:
        link = tag.get('href')
        full_link = "https://www.goodreads.com" + link 
        link_list.append(full_link)
        
    top_link_list = []
    for i in range(0, 10):
        top_link_list.append(link_list[i])


    return top_link_list
    


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    url = book_url 
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    tag1 = soup.find('h1', {"id": "bookTitle"})
    book_text = tag1.get_text()
    book_text = book_text.strip()

    tag2 = soup.find('a', class_ = "authorName")
    span = tag2.find('span')
    author_text = span.get_text()
    author_text = author_text.strip()

    
    tag3 = soup.find('span', itemprop = 'numberOfPages')
    text = tag3.text
    phrase = text.split()
    pages_text = int(phrase[0])


    summary_tuple = (book_text, author_text, pages_text) 



    return summary_tuple
    
    pass

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    
    
    f = open(filepath, 'r', encoding= 'utf-8')
    url = f.read()
    f.close()

    soup = BeautifulSoup(url, 'html.parser')

    category_list = []
    category_tags = soup.find_all(class_ = "category__copy")
    for tag in category_tags:
        text = tag.get_text()
        text = text.strip()
        category_list.append(text)
    
    title_list = []
    title_tags = soup.find_all(class_ = "category__winnerImage")
    for tag in title_tags:
        text = tag.get('alt')
        text = text.strip()
        title_list.append(text)

    url_list = []
    url_tags = soup.find_all(class_ ="category clearFix")
    for tag in url_tags:
        a = tag.find('a')
        text = a.get('href')
        #text = text.strip()
        url_list.append(text)
    
    
    summary_list = []
    for i in range(len(category_list)):
        tup = (category_list[i], title_list[i], url_list[i])
        summary_list.append(tup)
    
    return summary_list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    pass


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        title_info = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(title_info), 20)
        # check that the variable you saved after calling the function is a list
        type_title_info = type(title_info)
        self.assertEqual(type_title_info, list)
        # check that each item in the list is a tuple
        tuple_list = []
        for title in title_info:
            type_title = type(title)
            if type_title == tuple:
                tuple_list.append(type_title)
        self.assertEqual(len(tuple_list), 20)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(title_info[0][0],'Harry Potter and the Deathly Hallows (Harry Potter, #7)')
        self.assertEqual(title_info[0][1],'J.K. Rowling')
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(title_info[-1][0], 'Harry Potter: The Prequel (Harry Potter, #0.5)')
        self.assertEqual(title_info[-1][1], 'J.K. Rowling')

        
    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        type_search_urls = type(TestCases.search_urls)
        self.assertEqual(type_search_urls, list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        urls = TestCases.search_urls
        url_type_list = []
        for url in urls:
            url_type = type(url)
            if url_type == str:
                url_type_list.append(url_type)
        self.assertEqual(len(url_type_list), 10)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/ `              # how do you do this`
        


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        book_summary_list = []
        for i in TestCases.search_urls:
            book_summary_list.append(get_book_summary(i))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(book_summary_list), 10)
        for summary in book_summary_list:
            # check that each item in the list is a tuple
            summary_type = type(summary)
            self.assertEqual(summary_type, tuple)   
            # check that each tuple has 3 elements
            summary_len = len(summary)
            self.assertEqual(summary_len, 3)
            # check that the first two elements in the tuple are string
            element_one_type = type(summary[0])
            self.assertEqual(element_one_type, str)
            element_two_type = type(summary[1])
            self.assertEqual(element_two_type, str)
            # check that the third element in the tuple, i.e. pages is an int
            element_three_type = type(summary[2])
            self.assertEqual(element_three_type, int)
            # check that the first book in the search has 337 pages
        self.assertEqual(book_summary_list[0][2], 337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summary = summarize_best_books('best_books_2020.htm')
        # check that we have the right number of best books (20)
        self.assertEqual(len(summary), 20)
            # assert each item in the list of best books is a tuple
        tuples_list = []
        for item in summary:
            item_type = type(item)
            if item_type == tuple:
                tuples_list.append(item_type)
        self.assertEqual(len(tuples_list), 20)
            # check that each tuple has a length of 3
        tuple_length_list = []
        for book in summary:
            length = len(book)
            if length == 3:
                tuple_length_list.append(book)
        self.assertEqual(len(tuple_length_list), 20)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(summary[0], ('Fiction', 'The Midnight Library', 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(summary[-1],('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable

        # call write csv on the variable you saved and 'test.csv'

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)


        # check that there are 21 lines in the csv

        # check that the header row is correct

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        pass



if __name__ == '__main__':
    #print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



