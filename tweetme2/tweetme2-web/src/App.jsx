import { useState, useEffect } from 'react'
import './App.css'


function loadTweets(callback){
  const xhr = new XMLHttpRequest()
  const method = 'GET'//POST
  const url='http://127.0.0.1:8000/api/tweets/'
  const responseType = 'json'
  xhr.responseType = responseType
  xhr.open(method, url)
  xhr.onload = function() {
      callback(xhr.response, xhr.status)
  }    
  xhr.onerror = (e)=>{
    console.log(e);
    callback({message:'This request was an error'}, 400)
  } 
  xhr.send()
}

const Tweet = (props) => {
  const {tweet} = props
  const className = props.className ? props.className:'col-10 mx-auto col-md-6'
  return <div className={className}>
    <p>{tweet.id}- {tweet.content}</p>
  </div>
}


function App() {
  const [tweets, setTweets] = useState([])
  useEffect(() => {
    // do my lookup
    const myCallback = (response, status) =>{
      console.log(response, status);
      if (status === 200){
        setTweets(response)
      }else{
        alert('There was an error')
      }
    } 
    
    loadTweets(myCallback)
  },[])


  return (
    <div className="App">
      <p className="read-the-docs">
        {tweets.map((item, index) =>{
          return <Tweet key={index} tweet={item} className='my-5 py-5 border bg-white text-dark' />
        }) }        
      </p>
    </div>
  )
}

export default App
