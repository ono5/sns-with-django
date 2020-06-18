import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { Route, BrowserRouter } from 'react-router-dom';
import Login from './components/Login';
import { CookiesProvider } from 'react-cookie';

const routing = (
  <React.StrictMode>
    <BrowserRouter>
      <CookiesProvider>
          <Route exact path="/" component={Login} />
          <Route exact path="/profile" component={App} />

      </CookiesProvider>
    </BrowserRouter>
  </React.StrictMode>
)

ReactDOM.render(
  routing,
  document.getElementById('root')
);

serviceWorker.unregister();
