import { backendLookup } from "../lookup"

export function apiTweetCreate(newTweet, callback){
    backendLookup('POST','/tweets/create',callback, {content:newTweet})
  }
  
  export function apiTweetsList(callback){
      backendLookup('GET', '/tweets/', callback)
    }
  