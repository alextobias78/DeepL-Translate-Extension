if (!chrome || !chrome.runtime || !chrome.runtime.sendMessage) {
  console.error('Chrome extension APIs are not available. The extension may not work correctly.');
}

let isTranslationEnabled = false;
let originalTexts = new Map();
let currentTargetLanguage = '';

function detectPageLanguage() {
  return document.documentElement.lang.toLowerCase().substring(0, 2) || 'en';
}

function translateText(text, targetLang) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage({
      action: "translate",
      text: text,
      targetLang: targetLang
    }, response => {
      if (response && response.translatedText) {
        resolve(response.translatedText);
      } else if (response && response.error) {
        reject(new Error(response.error));
      } else {
        reject(new Error('Unknown error occurred'));
      }
    });
  });
}

function replaceTextInNode(node, originalText, translatedText) {
  if (node.nodeType === Node.TEXT_NODE) {
    if (node.textContent.includes(originalText)) {
      if (!originalTexts.has(node)) {
        originalTexts.set(node, node.textContent);
      }
      node.textContent = node.textContent.replace(originalText, translatedText);
    }
  } else {
    for (let i = 0; i < node.childNodes.length; i++) {
      replaceTextInNode(node.childNodes[i], originalText, translatedText);
    }
  }
}

// Implement debounce function to limit API calls
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Use a Set instead of an array for faster lookup
const processedNodes = new Set();

const debouncedTranslatePage = debounce(async function() {
  const pageLanguage = detectPageLanguage();
  const targetLang = await chrome.storage.sync.get(['targetLanguage']);
  
  if (!targetLang.targetLanguage) {
    console.error('Target language not set');
    return;
  }

  currentTargetLanguage = targetLang.targetLanguage;

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);

  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (!processedNodes.has(node) && node.textContent.trim()) {
      processedNodes.add(node);
      const originalText = node.textContent.trim();
      if (originalText.length > 0) {
        try {
          const translatedText = await translateText(originalText, currentTargetLanguage);
          replaceTextInNode(node, originalText, translatedText);
        } catch (error) {
          console.error('Translation error:', error);
          chrome.runtime.sendMessage({ 
            action: "showError", 
            error: `Translation failed: ${error}. Please check your internet connection and API key.`
          });
          return;
        }
      }
    }
  }
}, 300);

// Add this function to check if the target language has changed
async function checkAndUpdateTargetLanguage() {
  const targetLang = await chrome.storage.sync.get(['targetLanguage']);
  if (targetLang.targetLanguage && targetLang.targetLanguage !== currentTargetLanguage) {
    currentTargetLanguage = targetLang.targetLanguage;
    return true;
  }
  return false;
}

// Modify the translatePage function
async function translatePage() {
  const languageChanged = await checkAndUpdateTargetLanguage();
  if (languageChanged) {
    // Clear processed nodes and original texts if the language has changed
    processedNodes.clear();
    originalTexts.clear();
  }
  await debouncedTranslatePage();
}

function revertTranslation() {
  originalTexts.forEach((originalText, node) => {
    if (node.parentNode) {  // Check if the node is still in the document
      node.textContent = originalText;
    }
  });
  originalTexts.clear();
  processedNodes.clear();
}

// Handle dynamic content changes
const observer = new MutationObserver((mutations) => {
  if (isTranslationEnabled) {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList') {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            translatePage();
          }
        });
      }
    });
  }
});

observer.observe(document.body, { childList: true, subtree: true });

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "toggleTranslation") {
    isTranslationEnabled = !isTranslationEnabled;
    if (isTranslationEnabled) {
      // Clear processed nodes and original texts when re-enabling translation
      processedNodes.clear();
      originalTexts.clear();
      translatePage();
    } else {
      revertTranslation();
    }
    sendResponse({ status: isTranslationEnabled ? 'enabled' : 'disabled' });
  }
});

// Add this function to handle page unload
function handleUnload() {
  if (isTranslationEnabled) {
    revertTranslation();
  }
}

// Add event listener for page unload
window.addEventListener('beforeunload', handleUnload);