import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { TweetsComponent } from './tweets';
import reportWebVitals from './reportWebVitals';
/* const root = ReactDOM.createRoot(document.getElementById('root'));
if (root){
  
  root.render(
    <App />
  );
  root.render(
    <React.StrictMode>
    <App />
  </React.StrictMode>
  ); 
} */
const tweetEl = ReactDOM.createRoot(document.getElementById('tweetme-2'));
if (tweetEl){
  tweetEl.render(
    <TweetsComponent />
  );
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
