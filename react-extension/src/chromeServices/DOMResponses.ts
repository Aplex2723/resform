import {GoogleResponses } from '../types/DOMMessages';


const getMessageForResponse = (msg: GoogleResponses, sender: chrome.runtime.MessageSender, sendResponse: (response: any) => void) => {
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

chrome.runtime.onMessage.addListener(getMessageForResponse)