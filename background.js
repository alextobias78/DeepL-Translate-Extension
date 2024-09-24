chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "translate") {
    console.log('Received translation request:', request); // Add this line

    chrome.storage.sync.get(['deeplApiKey'], function(result) {
      const apiKey = result.deeplApiKey;
      if (!apiKey) {
        sendResponse({ error: "API key not found. Please set your DeepL API key." });
        return;
      }

      const apiUrl = apiKey.endsWith(':fx') 
        ? 'https://api-free.deepl.com/v2/translate'
        : 'https://api.deepl.com/v2/translate';

      const requestBody = {
        text: [request.text],
        target_lang: request.targetLang
      };
      console.log('API request body:', requestBody); // Add this line

      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Authorization': `DeepL-Auth-Key ${apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      })
      .then(response => response.json())
      .then(data => {
        console.log('API response:', data); // Add this line
        if (data.translations && data.translations.length > 0) {
          sendResponse({ translatedText: data.translations[0].text });
        } else {
          sendResponse({ error: "Translation failed. Please check your API key and try again." });
        }
      })
      .catch(error => {
        console.error('Error:', error);
        sendResponse({ error: "An error occurred while translating. Please try again." });
      });
    });

    return true; // Indicates that the response is sent asynchronously
  }
});

async function translateText(text, targetLang) {
  const { deeplApiKey } = await chrome.storage.sync.get(['deeplApiKey']);
  if (!deeplApiKey) {
    throw new Error('API key not set');
  }

  // Determine the correct API endpoint based on the API key
  const apiEndpoint = deeplApiKey.endsWith(':fx') ? 'https://api-free.deepl.com/v2/translate' : 'https://api.deepl.com/v2/translate';

  const data = {
    "text": [text],
    "target_lang": targetLang
  };

  try {
    const response = await fetch(apiEndpoint, {
      method: 'POST',
      headers: {
        'Authorization': `DeepL-Auth-Key ${deeplApiKey}`,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': chrome.runtime.getURL(''),
        'Referer': chrome.runtime.getURL('')
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error:', response.status, errorText);
      throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
    }

    const responseData = await response.json();
    if (responseData.translations && responseData.translations.length > 0) {
      return responseData.translations[0].text;
    } else {
      throw new Error('No translation returned');
    }
  } catch (error) {
    console.error('Translation error:', error);
    throw error;
  }
}

// Add a function to log errors to a remote service or local storage
function logError(error) {
  console.error('Extension error:', error);
  // Implement error logging to a remote service or local storage here
}