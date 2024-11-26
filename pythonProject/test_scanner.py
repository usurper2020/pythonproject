import logging
import unittest

from scanner import Scanner

logging.basicConfig ( filename='bug_bounty_finder.log' , level=logging.INFO )


class TestScanner ( unittest.TestCase ) :

	"""
    A test case class for testing the Scanner class functionality.
    """

	def setUp ( self ) :
		"""
        Set up the test environment before each test method is run.

        This method creates a new Scanner object for each test.
        """
		# Implementation remains the same

	def test_check_xss ( self ) :
		"""
        Test the check_xss method of the Scanner class.

        This test verifies that the method correctly identifies XSS vulnerabilities.
        """
		# Implementation remains the same

	def test_check_sql_injection ( self ) :
		"""
        Test the check_sql_injection method of the Scanner class.

        This test verifies that the method correctly identifies SQL injection vulnerabilities.
        """
		# Implementation remains the same


class TestScanner ( unittest.TestCase ) :
	def setUp ( self ) :
		"""

		"""

	self.scanner = Scanner ( )

	def test_check_xss ( self ) :
		self.assertTrue ( self.scanner.check_xss ( "<script>alert('XSS')</script>" ) )
		self.assertFalse ( self.scanner.check_xss ( "No XSS here" ) )

	def test_check_sql_injection ( self ) :
		# Add a test for SQL injection
		self.assertTrue ( self.scanner.check_sql_injection ( "https://example.com/page?id=1" ) )
		self.assertFalse ( self.scanner.check_sql_injection ( "https://example.com/page" ) )


if __name__ == '__main__' :
	unittest.main ( )
