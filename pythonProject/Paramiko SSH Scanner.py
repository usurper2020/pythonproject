import paramiko


def paramiko_scan ( url ) :
	"""

	:param url:
	:type url:
	"""
	# Create a Paramiko object
	ssh = paramiko.SSHClient ( )

	# Connect to the URL
	ssh.connect ( url , username='username' , password='password' )

	# Run a command on the remote server
	stdin , stdout , stderr = ssh.exec_command ( 'ls' )

	# Print the output
	print ( stdout.read ( ).decode ( ) )

	# Close the connection
	ssh.close ( )


def main () :
	"""

	"""
	url = input ( 'Enter the URL to scan: ' )
	paramiko_scan ( url )


if __name__ == "__main__" :
	main ( )
