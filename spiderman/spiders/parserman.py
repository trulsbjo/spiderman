from bs4 import BeautifulSoup

def get_review_id(html_doc):
	soup = BeautifulSoup(html_doc)
	return soup.div['id']

def get_review_location(html_doc):
	soup = BeautifulSoup(html_doc)
	return soup.find('div', {'class' : 'location'}).text.replace("\n", "")

def get_review_text(html_doc):
	soup = BeautifulSoup(html_doc)
	return soup.find('div', {'class' : 'entry'}).find('p').text.replace("\n", "")

def get_author(html_doc):
	soup = BeautifulSoup(html_doc)
	return soup.find('span', {'class' : 'scrname'}).text

def get_date(html_doc):
	soup = BeautifulSoup(html_doc)
	value = soup.find('span', {'class' : 'ratingDate'})
	if value.has_key('title'):
		return value['title']
	else:
		return soup.find('span', {'class' : 'ratingDate'}).text.replace("Reviewed ", "").replace("\n", "")

def get_author_reviews(html_doc):
	soup = BeautifulSoup(html_doc)
	return soup.find('span', {'class' : 'badgeText'}).text

def get_author_hotel_reviews(html_doc):
	soup = BeautifulSoup(html_doc)
	value = soup.find('div', {'class', 'contributionReviewBadge'})
	if value:
		return value.text.replace("\n", "")
	else:
		return '0 hotel reviews';

def get_author_helpful_votes(html_doc):
	soup = BeautifulSoup(html_doc)
	value = soup.find('div', {'class' : 'helpfulVotesBadge'})
	if value:
		return value.text.replace("\n", "")
	else:
		return '0 helpful votes';

def get_helpfullness(html_doc):
	soup = BeautifulSoup(html_doc)
	value = soup.find('div', {'class' : 'numHlpIn'})
	if value:
		return value.text.replace("\n", "")
	else:
		return '0';

def get_review_rating(html_doc):
	soup = BeautifulSoup(html_doc)
	value = soup.find('div', 'reviewItemInline').find('img')['content']
	if value:
		return value.replace(".0", "")
	else:
		return None;

	#<span class="ratingDate relativeDate" title='February 20, 2014'>Reviewed 6 days ago