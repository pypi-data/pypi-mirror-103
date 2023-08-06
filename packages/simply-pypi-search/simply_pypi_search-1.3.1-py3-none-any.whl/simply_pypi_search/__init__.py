import builtins

from bs4 import BeautifulSoup
from aiohttp import ClientSession


class PyPiSearch:
    def __init__(self):
        self.search = self.pypi_search
        self.usr_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/61.0.3163.100 Safari/537.36'}

    @classmethod
    async def pypi_search(cls, keyword: str) -> list:
        """
        Return the search-results in an :class:`list` with :class:`PyPiProject` 's

        :param keyword:
        :return: [result1, result2, result3, etc.]
        """
        html = await cls().pypi_get_results(keyword)
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find('ul', attrs='unstyled')
        if ul is None:
            return NoResultsFound(keyword)
        else:
            return list(cls().parse_pypi_results(ul))

    async def pypi_get_results(self, keyword):
        search_term = keyword.replace(" ", "+")
        async with ClientSession(headers=self.usr_agent) as suche:
            such_ergebnis = await suche.get(url=f"https://pypi.org/search/?q={search_term}&o")
            such_ergebnis.raise_for_status()
            results = await such_ergebnis.text()
        return results

    @classmethod
    def parse_pypi_results(cls, ul):
        result_block = ul.find_all('li')
        for result in result_block:
            link = result.find('a', href=True)['href']
            name = result.find('span', attrs={'class': 'package-snippet__name'})
            version = result.find('span', attrs={'class': 'package-snippet__version'})
            description = result.find('p', attrs={'class': 'package-snippet__description'})
            release = result.find('time')
            if release is not None:
                release = release.decode_contents().strip("\n \n")
            if name is not None:
                name = name.decode_contents()
            if version is not None:
                version = version.decode_contents()
            if description is not None:
                description = description.decode_contents()
            if name and link:
                yield PyPiProject({"name": name, "description": description, "version": version, "released": release,
                                   "link": "https://pypi.org" + link})


class PyPiProject:
    """
    The :class:`type` the parts off an :func:`~PyPiSearch.pypi_search` returned :class:`list` are out

    :class: PyPiProject

    """

    def __init__(self, data: dict):
        self.Name = data.get('name')
        self.Description: str = data.get('description')
        self.Version: str = data.get('version')
        self.Released: str = data.get('released')
        self.Link: str = data.get('link')

    @property
    def name(self):
        return self.Name

    @property
    def description(self):
        return self.Description

    @property
    def version(self):
        return self.Version

    @property
    def released(self):
        return self.Released

    @property
    def link(self):
        return self.Link


class SearchError:
    def __init__(self, args):
        self.args = args

    @property
    def error(self):
        return str(self.args)


class NoResultsFound(SearchError):
    def __init__(self, keyword):
        self.keyword = keyword
        no_results = 'No Results Found for the Keyword %s' % keyword
        super().__init__(no_results)
