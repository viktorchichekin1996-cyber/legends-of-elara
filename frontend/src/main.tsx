import React from 'react';
import ReactDOM from 'react-dom/client';
import { AppRoot } from '@vkontakte/vkui';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AppRoot>
      <App />
    </AppRoot>
  </React.StrictMode>,
);