# DeepL Translator Chrome Extension

This Chrome extension integrates DeepL's powerful translation capabilities directly into your browser, allowing for seamless webpage translation.

## Features

- Translate web pages on-the-fly using DeepL's API
- Support for multiple target languages
- Easy toggle for enabling/disabling translation
- Ability to test API connection
- Supports both free and pro DeepL API accounts

## Setup

1. Clone this repository or download the source code.
2. Open Chrome and navigate to `chrome://extensions/`.
3. Enable "Developer mode" in the top right corner.
4. Click "Load unpacked" and select the directory containing the extension files.

## Usage

1. Click on the extension icon in your Chrome toolbar to open the popup.
2. Enter your DeepL API key in the provided input field and click "Save API Key".
   - For free accounts, make sure your API key ends with ':fx'.
3. Select your desired target language from the dropdown menu.
4. Click "Enable Translation" to start translating the current webpage.
5. Use the "Test API Connection" button to verify your API key is working correctly.

## Supported Languages

The extension supports translation to the following languages:

- Bulgarian
- Czech
- Danish
- German
- Greek
- English (British)
- English (American)
- Spanish
- Estonian
- Finnish
- French
- Hungarian
- Italian
- Japanese
- Lithuanian
- Latvian
- Dutch
- Polish
- Portuguese
- Portuguese (Brazilian)
- Romanian
- Russian
- Slovak
- Slovenian
- Swedish
- Chinese (simplified)

## Development

This extension is built using HTML, CSS, and JavaScript. The main components are:

- `popup.html` and `popup.js`: Handle the extension's user interface and interactions.
- `background.js`: Manages API calls and browser-level operations.
- `content.js`: Interacts with webpage content for translation.

## Note

You need a valid DeepL API key to use this extension. You can obtain one by signing up at [DeepL's website](https://www.deepl.com/pro-api).
