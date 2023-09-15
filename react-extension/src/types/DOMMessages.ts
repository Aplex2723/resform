export type DOMMessage = {
  type: 'GET_DOM'
}

export type GoogleResponses = {
  type: 'GET_GOOGLE_RESPONSES'
}

export type BrightspaceResponses = {
  type: 'GET_BRIGHTSPACE_RESPONSES'
}

export type DOMMessageResponse = {
  title: string;
  headlines: string[];
}
