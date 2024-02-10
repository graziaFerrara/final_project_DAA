<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSite Organization and Search Engine Implementation</title>
</head>
<body>
    <h1>WebSite Organization and Search Engine Implementation</h1>

    <h2>WebSite Organization</h2>

    <h3>Classes:</h3>
    <ol>
        <li><strong>Element</strong>: Models either directories or webpages.</li>
        <li><strong>WebSite</strong>: Represents a website and provides methods for managing its structure.</li>
    </ol>

    <h3>Public Methods:</h3>
    <ul>
        <li><code>WebSite(host)</code>: Creates a new WebSite object for saving the website hosted at <code>host</code>.</li>
        <li><code>getHomePage()</code>: Returns the home page of the website.</li>
        <li><code>getSiteString()</code>: Returns a string showing the structure of the website.</li>
        <li><code>insertPage(url, content)</code>: Saves and returns a new page of the website.</li>
        <li><code>getSiteFromPage(page)</code>: Given a page, returns the WebSite object it belongs to.</li>
    </ul>

    <h3>Private Methods:</h3>
    <ul>
        <li><code>__hasDir(ndir, cdir)</code>: Checks if a directory exists in the current directory.</li>
        <li><code>__newDir(ndir, cdir)</code>: Creates a new directory if it doesn't exist.</li>
        <li><code>__hasPage(npag, cdir)</code>: Checks if a webpage exists in the current directory.</li>
        <li><code>__newPage(npag, cdir)</code>: Creates a new webpage if it doesn't exist.</li>
        <li><code>__isDir(elem)</code>: Checks if an element is a directory.</li>
        <li><code>__isPage(elem)</code>: Checks if an element is a webpage.</li>
    </ul>

    <h2>Search Engine</h2>

    <h3>Classes:</h3>
    <ol>
        <li><strong>InvertedIndex</strong>: Represents the core data structure of the search engine.</li>
    </ol>

    <h3>Public Methods:</h3>
    <ul>
        <li><code>InvertedIndex()</code>: Creates a new empty InvertedIndex.</li>
        <li><code>addWord(keyword)</code>: Adds a keyword to the InvertedIndex.</li>
        <li><code>addPage(page)</code>: Processes a webpage and updates the inverted index.</li>
        <li><code>getList(keyword)</code>: Retrieves the occurrence list for a given keyword.</li>
    </ul>

    <h2>SearchEngine Class</h2>

    <h3>Methods:</h3>
    <ul>
        <li><code>SearchEngine(namedir)</code>: Initializes the SearchEngine with a directory containing webpage files.</li>
        <li><code>search(keyword, k)</code>: Searches for the top k web pages with the maximum occurrences of the keyword.</li>
    </ul>

    <h2>Efficiency Goals:</h2>
    <ul>
        <li>Constant time complexity for various operations.</li>
        <li>Linear time complexity for generating site structure.</li>
        <li>Logarithmic time complexity for directory and page existence checks.</li>
        <li>Linear time complexity for adding keywords and retrieving occurrence lists.</li>
    </ul>

    <h2>Note:</h2>
    <ul>
        <li>The implementation aims to optimize efficiency for website organization and search queries.</li>
        <li>A test dataset is provided for evaluating the correctness and performance of the code.</li>
    </ul>
</body>
</html>
