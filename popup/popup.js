let isTranslationEnabled = false;

document.addEventListener('DOMContentLoaded', function() {
  const toggleButton = document.getElementById('toggleTranslation');
  const apiKeyInput = document.getElementById('apiKeyInput');
  const saveApiKeyButton = document.getElementById('saveApiKey');
  const testApiButton = document.getElementById('testApiConnection');
  const statusDiv = document.getElementById('status');
  const targetLanguageSelect = document.getElementById('targetLanguage');

  chrome.storage.sync.get(['deeplApiKey', 'targetLanguage'], function(result) {
    if (result.deeplApiKey) {
      apiKeyInput.value = result.deeplApiKey;
    }
    if (result.targetLanguage) {
      targetLanguageSelect.value = result.targetLanguage;
    }
  });

  saveApiKeyButton.addEventListener('click', function() {
    const apiKey = apiKeyInput.value.trim();
    if (apiKey) {
      if (!apiKey.endsWith(':fx') && !apiKey.match(/^[a-f0-9]{32}$/)) {
        showNotification('Invalid API key format. Please check your DeepL account type and enter the correct key.', true);
        return;
      }
      chrome.storage.sync.set({ deeplApiKey: apiKey }, function() {
        showNotification('API key saved successfully!');
      });
    } else {
      showNotification('Please enter a valid API key.', true);
    }
  });

  // Add this function
  function saveTargetLanguage() {
    const targetLanguage = document.getElementById('targetLanguage').value;
    chrome.storage.sync.set({ targetLanguage: targetLanguage }, function() {
      console.log('Target language saved:', targetLanguage);
    });
  }

  // Modify the existing event listener for the language dropdown
  document.getElementById('targetLanguage').addEventListener('change', saveTargetLanguage);

  // Add this to the existing code that runs when the popup is opened
  chrome.storage.sync.get(['targetLanguage'], function(result) {
    if (result.targetLanguage) {
      document.getElementById('targetLanguage').value = result.targetLanguage;
    }
  });

  function updateUIState(isEnabled) {
    isTranslationEnabled = isEnabled;
    toggleButton.textContent = isEnabled ? 'Disable Translation' : 'Enable Translation';
    toggleButton.classList.toggle('active', isEnabled);
  }

  function showNotification(message, isError = false) {
    statusDiv.textContent = message;
    statusDiv.style.color = isError ? 'red' : 'green';
    statusDiv.style.display = 'block';
    setTimeout(() => { 
      statusDiv.style.display = 'none';
      statusDiv.style.color = 'initial';
    }, 5000);
  }

  toggleButton.addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {action: "toggleTranslation"}, function(response) {
        if (response) {
          updateUIState(response.status === 'enabled');
          showNotification(`Translation ${response.status}`);
        }
      });
    });
  });

  testApiButton.addEventListener('click', function() {
    const apiKey = apiKeyInput.value.trim();
    const targetLang = targetLanguageSelect.value;
    console.log('Selected target language:', targetLang); // Add this line

    if (!apiKey) {
      showNotification('Please enter an API key first.', true);
      return;
    }

    showNotification('Testing API connection...');
    
    chrome.runtime.sendMessage({
      action: "translate",
      text: "Hello, world!",
      targetLang: targetLang
    }, response => {
      console.log('Response from background:', response); // Add this line
      if (response && response.translatedText) {
        showNotification(`API connection successful! "Hello, world!" in ${targetLanguageSelect.options[targetLanguageSelect.selectedIndex].text}: ${response.translatedText}`);
      } else if (response && response.error) {
        showNotification(`API connection failed: ${response.error}`, true);
      } else {
        showNotification('Unknown error occurred during API test.', true);
      }
    });
  });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "showError") {
    showNotification(request.error, true);
  }
});

function showNotification(message, isError = false) {
  const statusDiv = document.getElementById('status');
  statusDiv.textContent = message;
  statusDiv.style.color = isError ? 'red' : 'green';
  statusDiv.style.display = 'block';
  setTimeout(() => { 
    statusDiv.style.display = 'none';
    statusDiv.style.color = 'initial';
  }, 5000);
}