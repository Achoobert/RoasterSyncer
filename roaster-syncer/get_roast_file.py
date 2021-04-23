#!/usr/bin/python3

from bs4 import BeautifulSoup
import csv
import logging
import requests
import os, sys
# from requests_file import FileAdapter
from urllib.parse import urljoin
from roast_file_processor import fileSplit

roaster_url = "http://192.168.1.104/logs/log2/"
test_roaster_url = "http://192.168.1.1/"
file_url = "file:///opt/Repos/gitlab/internetofbeans/roaster-syncer/test/"

if sys.version_info.major < 3:
	from urllib import url2pathname
else:
	from urllib.request import url2pathname

# from https://stackoverflow.com/questions/10123929/python-requests-fetch-a-file-from-a-local-url/22989322#
class LocalFileAdapter(requests.adapters.BaseAdapter):
	"""Protocol Adapter to allow Requests to GET file:// URLs

	@todo: Properly handle non-empty hostname portions.
	"""

	@staticmethod
	def _chkpath(method, path):
		"""Return an HTTP status for the given filesystem path."""
		logging.info("file url path: %s", path)
		if method.lower() in ('put', 'delete'):
			return 501, "Not Implemented"  # TODO
		elif method.lower() not in ('get', 'head'):
			return 405, "Method Not Allowed"
		elif os.path.isdir(path):
			return 400, "Path Not A File"
		elif not os.path.isfile(path):
			return 404, "File Not Found"
		elif not os.access(path, os.R_OK):
			return 403, "Access Denied"
		else:
			return 200, "OK"

	def send(self, req, **kwargs):  # pylint: disable=unused-argument
		"""Return the file specified by the given request

		@type req: C{PreparedRequest}
		@todo: Should I bother filling `response.headers` and processing
			   If-Modified-Since and friends using `os.stat`?
		"""
		path = os.path.normcase(os.path.normpath(url2pathname(req.path_url)))
		response = requests.Response()

		response.status_code, response.reason = self._chkpath(req.method, path)
		if response.status_code == 200 and req.method.lower() != 'head':
			try:
				response.raw = open(path, 'rb')
			except (OSError, IOError) as err:
				response.status_code = 500
				response.reason = str(err)

		if isinstance(req.url, bytes):
			response.url = req.url.decode('utf-8')
		else:
			response.url = req.url

		response.request = req
		response.connection = self

		return response

	def close(self):
		pass


def get_roaster_page(kb_url):
	try:
		# requests_session = requests.session()
		# requests_session.mount('file://', FileAdapter())
		# response = requests_session.get(kb_url, timeout=0.1)
		response = requests.get(kb_url, timeout=0.1)
		if response.status_code == 200:
			return response.text
		else:
			logging.warning("status: %d reason: %s", response.status_code, response.reason)
			return None
	except requests.exceptions.ConnectionError as ece:
		logging.warning("Connection Error")
		return None
	except requests.exceptions.Timeout as et:
		logging.warning("Timeout Error")
		return None
	except requests.exceptions.RequestException as e:
		logging.warning("Some Ambiguous Exception:", e)
		return None

def get_file_list(url):
	logging.info("getting files from url %s", url)
	page = get_roaster_page(url)
	if page:
		logging.info("parsing page")
		soup = BeautifulSoup(page, 'html.parser')
		return [url + node.get('href') for node in soup.find_all('a')]
	else:
		logging.info("no page to parse")
		return None

def get_roaster_file(url, csvfile):
	downloadfile = None

	requests_session = requests.session()
	requests_session.mount('file://', LocalFileAdapter())
	logging.info("getting roaster file %s", url)
	response = requests_session.get(url, timeout=0.1)

	if response.status_code == 200:
		with open(csvfile, 'wb') as f:
			f.write(response.content)
			downloadfile = csvfile
	return downloadfile

def main(argv):
	logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
	filelist = get_file_list(roaster_url)
	logging.info("filelist: %s", filelist)
	base_url = roaster_url
	if not filelist:
		filelist = get_file_list(test_roaster_url)
		logging.info("filelist: %s", filelist)
		base_url = test_roaster_url
	if not filelist:
		filelist = os.listdir("test")
		logging.info("filelist: %s", filelist)
		base_url = file_url

	if filelist:
		if not os.path.exists("process"):
			os.makedirs("process")
		if not os.path.exists("input"):
			os.makedirs("input")
		for csvfile in filelist:
			logging.info("file: %s", csvfile)
			input_file = os.path.join("input", csvfile)
			if not os.path.exists(input_file):
				url = urljoin(base_url, csvfile)
				get_roaster_file(url, input_file)
				if os.path.exists(input_file):
					fileSplit(csv.reader(open(input_file)), "process")
				else:
					logging.warning("csv file not downloaded")


if __name__ == "__main__":
	main(sys.argv[1:])