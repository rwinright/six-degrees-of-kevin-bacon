const searchButton = document.querySelector('#searchButton');
const searchInput = document.querySelector('#searchInput');
searchInput.value= '';

const resultsOutput = document.querySelector('#results');

const handleRequest = async (value) => {
  if(value.includes('https://en.wikipedia.org/wiki/')) {
    value = value.replace('https://en.wikipedia.org/wiki/', '');
    console.log(value);
  } else if(value.includes("en.wikipedia.org/wiki/")) {
    value = value.replace('en.wikipedia.org/wiki/', '');
    console.log(value);
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/degrees/${value}`);
    if(response.status === 404) {
      throw new Error('404');
      return;
    }
    const data = await response.json(); //extract JSON from the http response
    //If data is 404, display error message
    resultsOutput.innerHTML = `You are ${data.degrees} degrees from Kevin Bacon`;
  } catch (error) {
    resultsOutput.innerHTML = 'Something went wrong, double check your search term URL';
    console.log(error);
  }
}

searchButton.addEventListener('click', () => {
  if(searchInput.value === '') {
    resultsOutput.innerHTML = 'Please enter a search term';
    return;
  } else {
    resultsOutput.innerHTML = 'Searching...';
    //Send get request to 0.0.0.0:8000/degrees/{searchpage}
    handleRequest(searchInput.value);
  }
});