# WebSite Organization and Search Engine Implementation

## WebSite Organization

### Classes:
1. **Element**: Models either directories or webpages.
2. **WebSite**: Represents a website and provides methods for managing its structure.

### Public Methods:
- `WebSite(host)`: Creates a new WebSite object for saving the website hosted at `host`.
- `getHomePage()`: Returns the home page of the website.
- `getSiteString()`: Returns a string showing the structure of the website.
- `insertPage(url, content)`: Saves and returns a new page of the website.
- `getSiteFromPage(page)`: Given a page, returns the WebSite object it belongs to.

### Private Methods:
- `__hasDir(ndir, cdir)`: Checks if a directory exists in the current directory.
- `__newDir(ndir, cdir)`: Creates a new directory if it doesn't exist.
- `__hasPage(npag, cdir)`: Checks if a webpage exists in the current directory.
- `__newPage(npag, cdir)`: Creates a new webpage if it doesn't exist.
- `__isDir(elem)`: Checks if an element is a directory.
- `__isPage(elem)`: Checks if an element is a webpage.

## Search Engine

### Classes:
1. **InvertedIndex**: Represents the core data structure of the search engine.

### Public Methods:
- `InvertedIndex()`: Creates a new empty InvertedIndex.
- `addWord(keyword)`: Adds a keyword to the InvertedIndex.
- `addPage(page)`: Processes a webpage and updates the inverted index.
- `getList(keyword)`: Retrieves the occurrence list for a given keyword.

## SearchEngine Class

### Methods:
- `SearchEngine(namedir)`: Initializes the SearchEngine with a directory containing webpage files.
- `search(keyword, k)`: Searches for the top k web pages with the maximum occurrences of the keyword.

## Efficiency Goals:
- Constant time complexity for various operations.
- Linear time complexity for generating site structure.
- Logarithmic time complexity for directory and page existence checks.
- Linear time complexity for adding keywords and retrieving occurrence lists.

## Note:
- The implementation aims to optimize efficiency for website organization and search queries.
- A test dataset is provided for evaluating the correctness and performance of the code.
