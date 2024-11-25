import nmap


def nmap_scan ( url ) :
	"""

	:param url:
	:type url:
	"""
	# Create an Nmap object
	nm = nmap.PortScanner ( )

	# Scan the URL
	nm.scan ( url , '1-1024' )

	# Get the scan results
	results = nm.get_nmap_last_output ( )

	# Print the results
	print ( results )


def main () :
	"""

	"""
	url = input ( 'Enter the URL to scan: ' )
	nmap_scan ( url )


if __name__ == "__main__" :
	main ( )
