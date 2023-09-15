import { DOMMessage, DOMMessageResponse, GoogleResponses } from '../types';

const messagesFromReactAppListener = (msg: DOMMessage, sendResponse: (response: DOMMessageResponse) => void) => {
  console.log('[content.js]. Message received', msg);

  const response: DOMMessageResponse = {
    title: document.title,
    headlines: Array.from(document.getElementsByTagName<"h1">("h1")).map(h1 => h1.innerText),
  };
  console.log('[content.js]. Message response', response);

  sendResponse(response)

}

const getMessageForResponse = (msg: GoogleResponses, sendResponse: (response: any) => void) => {
  console.log('[content.js]. Document', document)

  const elementsWithClass = document.querySelectorAll('.Qr7Oae')

  const questionsAndInputs = Array.from(elementsWithClass).map((element) => {
    // Find all input elements within each specific class element
    const new_obj: {[key: string]: any} = {}
    const question = element.querySelector('.M7eMe')?.innerHTML 
    const input = element.querySelector('.whsOnd') as HTMLInputElement;
    const textarea = element.querySelector('.KHxj8b')
    if(question){ new_obj['question'] = question}
    if(input){ {
      input.setAttribute('data-initial-value', "123");
      input.value = "123"
      new_obj['input'] = input
    }}
    if(textarea){ new_obj['textarea'] = textarea}
    return new_obj;
  });


  console.log('[conent.js] Questions and Inputs', questionsAndInputs)


  sendResponse(questionsAndInputs)
}


/**
 * Fired when a message is sent from either an extension process or a content script.
 */
chrome.runtime.onMessage.addListener((msg, sender, sendResponse: (response: any) => void) => {
  if(msg.type === 'GET_DOM'){
    messagesFromReactAppListener(msg, sendResponse)
  } if (msg.type === 'GET_GOOGLE_RESPONSES') {
    getMessageForResponse(msg, sendResponse)
  } if (msg.type === 'GET_BRIGHTSPACE_RESPONSES'){
    
  }
});
