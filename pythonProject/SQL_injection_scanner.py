import requests
from bs4 import BeautifulSoup


def sql_injection_scan ( url ) :
	"""

	:param url:
	:type url:
	:return:
	:rtype:
	"""
	# Send a request to the URL with a SQL injection payload
	payload = "' OR 1=1 --"
	response = requests.get ( url + payload )

	# Check if the response contains a SQL error message
	soup = BeautifulSoup ( response.text , 'html.parser' )
	if 'SQL' in soup.text :
		return True
	else :
		return False


def main () :
	"""

	"""
	url = input ( 'Enter the URL to scan: ' )
	if sql_injection_scan ( url ) :
		print ( 'SQL injection vulnerability found!' )
	else :
		print ( 'No SQL injection vulnerability found.' )


if __name__ == "__main__" :
	main ( )
