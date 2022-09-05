import React, {useEffect, useState, useRef} from 'react'
import { 
  apiTweetCreate,
  apiTweetsList,
  apiTweetAction } from './lookup'


export function TweetsComponent(props){
    // const textAreaRef =  React.createRef()
    const textAreaRef =  useRef(null)
    const [newTweets, setNewTweets] = useState([])


    const handleBackendUpdate = (response, status) => {
      // backend api response handler
      let tempNewTweets = [...newTweets]
      if (status === 201){
        setNewTweets(tempNewTweets)
        tempNewTweets.unshift(response)
      }else{
        console.log(response)
        alert('An error occured please try again')
      }
    }
    const handleSubmit = (event) =>{
        event.preventDefault()
        const newValue = textAreaRef.current.value
        // backend api request
        apiTweetCreate(newValue, handleBackendUpdate)
        textAreaRef.current.value = ''
    } 
    return <div className={props.className}>
        <div className='col-12 mb-3'>
                <form  action="" onSubmit={handleSubmit}>
                    <textarea ref={textAreaRef} required={true} className='form-control' name="tweet">

                    </textarea>
                    <button type="submit" className='btn btn-primary my-3'>Tweet</button>
                </form>
        </div>
        <TweetsList newTweets = {newTweets} />
    </div>
}

 export function TweetsList(props) {
    const [tweetsInit, setTweetsInit] = useState([])
    // console.log(tweetsInit)
    const [tweets, setTweets] = useState([])
    // setTweetsInit([...props.newTweets].concat(tweetsInit))
    const [tweetsDidsSet, settweetsDidsSet] = useState(false)
    useEffect(() => {
        // setTweetsInit([...props.newTweets].concat(tweetsInit))
        let final = [...props.newTweets].concat(tweetsInit)
        if (final.length !== tweets.length){
            setTweets(final)
        }
    }, [props.newTweets, tweets,tweetsInit])

    useEffect(() => {
      if (tweetsDidsSet === false){
        const handleTweetLookup = (response, status) => { 
          if(status === 200){
            setTweetsInit(response)
            settweetsDidsSet(true)
          }else{
            alert('There was an error')
          }
        }
        apiTweetsList(handleTweetLookup)
      }
    }, [tweetsInit, tweetsDidsSet, settweetsDidsSet])
    return tweets.map((item, index) =>{
      return <Tweet tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-${item.id}`}/>
    } )
  }

export function ActionBtn(props){
    const {tweet, action} = props
    const [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0)
    // const [userLike, setUserLike]= useState(tweet.userLike === true ? true : false)
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'
    
    const handleActionBackendEvent = (response, status) => {
      console.log(response, status)
      if (status === 200){
        setLikes(response.likes)
        // setUserLike(true)
      }
    }
    const handleClick = (event) =>{
        event.preventDefault()
        apiTweetAction(tweet.id, action.type, handleActionBackendEvent)
       
    } 
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    return  <button className={className} onClick={handleClick}>{display}</button>
  } 
  
export function ParentTweet(props){
  const {tweet} = props
  return tweet.parent? <div className='row'>
    <div className='col-11 mx-auto p-3 border rounded'>
      <p className='mb-0 text-muted small'>Retweet</p>
      <Tweet className='col-11 mx-auto p-3 border rounded' tweet={tweet.parent} />
    </div>
  </div> : null
}

export  function Tweet(props){
    const {tweet} = props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return <div className={className}>
        <div>
          <p>{tweet.id} - {tweet.content}</p>
          <ParentTweet tweet={tweet} />
        </div>
        <div className='btn-group'>
          <ActionBtn tweet={tweet} action={{type:'like', display:'Likes'}}/>
          <ActionBtn tweet={tweet} action={{type:'unlike', display:'Unlikes'}}/>
          <ActionBtn tweet={tweet} action={{type:'retweet', display:'Retweet'}}/>
        </div>
    </div>
  }