import React from 'react';
import './App.css';
import { DOMMessage, DOMMessageResponse, GoogleResponses } from './types';

function App() {
  const [title, setTitle] = React.useState('');
  const [headlines, setHeadlines] = React.useState<string[]>([]);
  const [url, setUrl] = React.useState<string | null>(null)
  const [companyName, setCompanyName] = React.useState<string>('')


  const getCompanyNameFromURL = (url: string): string => {
    // Parse the URL to get the hostname
    const parser = document.createElement('a');
    parser.href = url;
    const hostname = parser.hostname;
  
    // Extract the company name based on specific patterns or subdomains
    const subdomains = hostname.split('.');
    let companyName = '';
  
    // Check for common subdomains or patterns
    if (subdomains.length >= 2) {
      const secondLevelDomain = subdomains[subdomains.length - 2];
      const topLevelDomain = subdomains[subdomains.length - 1];
  
      // Check for common patterns like 'www' or 'blog' in the subdomains
      if (secondLevelDomain === 'www' && subdomains.length >= 3) {
        companyName = subdomains[subdomains.length - 3];
      } else if (secondLevelDomain === 'blog' && subdomains.length >= 3) {
        companyName = subdomains[subdomains.length - 3];
      } else {
        companyName = secondLevelDomain;
      }
    } else {
      companyName = hostname;
    }
  
    return companyName;
  }

  const submitCallback = () => {
    chrome.tabs && chrome.tabs.query({
      active: true,
      currentWindow: true
    }, tabs => {
      chrome.tabs.sendMessage(tabs[0].id || 0, {type: 'GET_GOOGLE_RESPONSES'} as GoogleResponses, (response: any) => {
        console.log(response)
      })
    })
  }

  React.useEffect(() => {
    /**
     * We can't use "chrome.runtime.sendMessage" for sending messages from React.
     * For sending messages from React we need to specify which tab to send it to.
     */
    chrome.tabs && chrome.tabs.query({
      active: true,
      currentWindow: true
    }, tabs => {
      /**
       * Sends a single message to the content script(s) in the specified tab,
       * with an optional callback to run when a response is sent back.
       *
       * The runtime.onMessage event is fired in each content script running
       * in the specified tab for the current extension.
       */
      chrome.tabs && chrome.tabs.query({
        active: true,
        currentWindow: true
      }, tabs => {
        chrome.tabs.sendMessage(
          tabs[0].id || 0,
          { type: 'GET_DOM' } as DOMMessage,
          (response: DOMMessageResponse) => {
            setTitle(response.title);
            setHeadlines(response.headlines);
          });
  
      })

      if (tabs.length > 0) {
        const url = tabs[0].url
        setUrl(url || null);
  
        if(url){
          setCompanyName(getCompanyNameFromURL(url));
        }
      }

    }, );
  }, []);

  return (
    <div className="App">
      <div className='bg-rectangle'>
        <div className='title-container'>
          <h1>Quiz Answers</h1>
        </div>
        <div className='alpha-section'>
          <p>Alpha Version</p>
        </div>
      </div>

      <div className='icons-container'>
        <img src='/img/brightspace-logo.png'/>
        <img src='/img/forms-logo.webp'/>
        <img src='/img/kahoot-logo.png'/>
        <img src='/img/microsoft-logo.png'/>
      </div>

      <div className='tabs'>
        <div className='tab-1'>
          <label>Raw text answers</label>
        </div>
        <div className='tab-2'>
          <label>Questions found</label>
        </div>
      </div>
      <div className='answerers-container'>

      </div>

      <div className='container'>
        <button className='button-start' onClick={submitCallback}>START</button>
        <div className='logo-section'>
          <h1>POWERED BY</h1>
          <img src="/logo.png" alt="codey logo" />
        </div>
      </div>
    </div>
  );
}

export default App;
