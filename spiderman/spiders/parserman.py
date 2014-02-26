from bs4 import BeautifulSoup

def get_review_id(html_doc):
	soup = BeautifulSoup(html_doc)
	return soup.div['id']

def get_review_location(html_doc):
	soup = BeautifulSoup(html_doc)
	return soup.find('div', {'class' : 'location'}).text.replace("\n", "")

def get_review_text(html_doc):
	soup = BeautifulSoup(html_doc)
	return soup.find('div', {'class' : 'entry'}).text.replace("\n", "")

def get_author(html_doc):
	soup = BeautifulSoup(html_doc)
	return soup.find('span', {'class' : 'scrname'}).text

def get_date(html_doc):
	soup = BeautifulSoup(html_doc)
	return soup.find('span', {'class' : 'ratingDate'})['title']

	#<img class="sprite-rating_s_fill rating_s_fill s50" src="http://c1.tacdn.com/img2/x.gif" alt="5 of 5 stars" content="5.0">

	#<span class="ratingDate relativeDate" title='February 20, 2014'>Reviewed 6 days ago