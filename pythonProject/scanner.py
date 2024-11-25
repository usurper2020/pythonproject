import sys
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime


def global_exception_handler ( exctype , value , traceback ) :
	"""
    Global exception handler for unhandled exceptions.
    """
	logging.critical ( "Unhandled exception" , exc_info=(exctype , value , traceback) )


# Setting the global exception hook
sys.excepthook = global_exception_handler


class ScannerException ( Exception ) :
	"""Base exception class for Scanner."""
	pass


class NetworkError ( ScannerException ) :
	"""Exception raised for network-related errors."""
	pass


class VulnerabilityDetected ( ScannerException ) :
	"""Exception raised when a vulnerability is detected."""
	pass


class ConfigurationError ( ScannerException ) :
	"""Exception raised for configuration-related errors."""
	pass


class ResultsManager :
	"""

	"""
	def __init__ ( self ) :
		self.results = []

	def add_result ( self , result ) :
		"""

		:param result:
		:type result:
		"""
		self.results.append ( result )

	def get_results ( self ) :
		"""

		:return:
		:rtype:
		"""
		return self.results

	def save_to_file ( self , filename ) :
		"""

		:param filename:
		:type filename:
		"""
		try :
			with open ( filename , 'w' ) as file :
				for result in self.results :
					file.write ( str ( result ) + "\n" )
		except Exception as e :
			logging.error ( f"Error saving results to {filename}: {str ( e )}" , exc_info=True )

	def load_from_file ( self , filename ) :
		"""

		:param filename:
		:type filename:
		"""
		try :
			with open ( filename ) as file :
				self.results = file.readlines ( )
		except Exception as e :
			logging.error ( f"Error loading results from {filename}: {str ( e )}" , exc_info=True )


class Scanner :
	"""

	"""
	def __init__ ( self ) :
		self.results_manager = ResultsManager ( )
		self.logger = self.setup_logger ( )

	@staticmethod
	def setup_logger () :
		"""

		:return:
		:rtype:
		"""
		logger = logging.getLogger ( 'ScannerLogger' )
		logger.setLevel ( logging.INFO )
		handler = logging.FileHandler ( 'scanner.log' )
		formatter = logging.Formatter ( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
		handler.setFormatter ( formatter )
		logger.addHandler ( handler )
		return logger

	def check_xss ( self , url: str , text: str ) :
		"""
        Check for XSS vulnerabilities.
        """
		try :
			if '<script>' in text.lower ( ) :
				result = {
						"timestamp" : datetime.now ( ) ,
						"vulnerability_type" : "XSS" ,
						"description" : f"Potential XSS vulnerability detected: {text[:100]}..." ,
						"severity" : "High" ,
						"url" : url
						}
				self.results_manager.add_result ( result )
				self.logger.warning ( f"XSS vulnerability detected at {url}" )
		except Exception as e :
			self.logger.error ( f"Error in XSS check for {url}: {str ( e )}" , exc_info=True )

	def check_sql_injection ( self , url: str ) :
		"""
        Check for SQL injection vulnerabilities.
        """
		test_url = url + "' OR '1'='1"
		try :
			response = requests.get ( test_url , timeout=10 )
			if 'error' in response.text.lower ( ) or 'sql' in response.text.lower ( ) :
				result = {
						"timestamp" : datetime.now ( ) ,
						"vulnerability_type" : "SQL Injection" ,
						"description" : "Potential SQL Injection vulnerability detected" ,
						"severity" : "High" ,
						"url" : url
						}
				self.results_manager.add_result ( result )
				self.logger.warning ( f"SQL Injection vulnerability detected at {url}" )
		except requests.RequestException as e :
			self.logger.error ( f"Request error in SQL injection check for {url}: {str ( e )}" )
		except Exception as e :
			self.logger.error ( f"Error in SQL injection check for {url}: {str ( e )}" , exc_info=True )

	def perform_scan ( self , target_website: str , depth: int , threads: int , timeout: int , verbose: bool ) :
		"""

		:param target_website:
		:type target_website:
		:param depth:
		:type depth:
		:param threads:
		:type threads:
		:param timeout:
		:type timeout:
		:param verbose:
		:type verbose:
		"""
		self.logger.info ( f"Starting scan on {target_website}" )
		visited = set ( )
		try :
			self.recursive_scan ( target_website , depth , visited , threads , timeout , verbose )
		except Exception as e :
			self.logger.error ( f"Error during scan of {target_website}: {str ( e )}" , exc_info=True )
		self.logger.info ( f"Scan completed for {target_website}" )

	def recursive_scan ( self , url: str , depth: int , visited: set , threads: int , timeout: int , verbose: bool ) :
		"""

		:param url:
		:type url:
		:param depth:
		:type depth:
		:param visited:
		:type visited:
		:param threads:
		:type threads:
		:param timeout:
		:type timeout:
		:param verbose:
		:type verbose:
		:return:
		:rtype:
		"""
		if depth <= 0 or url in visited :
			return
		visited.add ( url )
		try :
			response = requests.get ( url , timeout=timeout )
			self.check_xss ( url , response.text )
			self.check_sql_injection ( url )
			if verbose :
				self.logger.info ( f"Scanning: {url}" )
				self.logger.info ( f"Status Code: {response.status_code}" )
			soup = BeautifulSoup ( response.text , 'html.parser' )
			links = soup.find_all ( 'a' , href=True )
			for link in links :
				next_url = urljoin ( url , link['href'] )
				if self.same_domain ( url , next_url ) :
					self.recursive_scan ( next_url , depth - 1 , visited , threads , timeout , verbose )
		except requests.RequestException as e :
			self.logger.error ( f"Request error scanning {url}: {str ( e )}" )
		except Exception as e :
			self.logger.error ( f"Error scanning {url}: {str ( e )}" , exc_info=True )

	@staticmethod
	def same_domain ( url1: str , url2: str ) -> bool :
		"""

		:param url1:
		:type url1:
		:param url2:
		:type url2:
		:return:
		:rtype:
		"""
		return url1.split ( '//' )[1].split ( '/' )[0] == url2.split ( '//' )[1].split ( '/' )[0]

	def save_results ( self , filename: str ) :
		"""

		:param filename:
		:type filename:
		"""
		try :
			self.results_manager.save_to_file ( filename )
			self.logger.info ( f"Results saved to {filename}" )
		except Exception as e :
			self.logger.error ( f"Error saving results to {filename}: {str ( e )}" , exc_info=True )

	def load_results ( self , filename: str ) :
		"""

		:param filename:
		:type filename:
		"""
		try :
			self.results_manager.load_from_file ( filename )
			self.logger.info ( f"Results loaded from {filename}" )
		except Exception as e :
			self.logger.error ( f"Error loading results from {filename}: {str ( e )}" , exc_info=True )
