import React from 'react';
import './App.css';
import Header from './components/Header/Header';
import Routes from './routes';
import history from './services/history';
import { Router } from 'react-router-dom';
import GlobalStyles from './styles/GlobalStyles';
import { ToastContainer } from 'react-toastify'
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react'
import store, {persistor} from './store';
function App() {
  return (
    <Provider store={store}>
      <PersistGate persistor={persistor}>
      <Router history={history}>
        <Header></Header>
        <Routes></Routes>
        <GlobalStyles />
        <ToastContainer autoClose={3000} />
      </Router>
      </PersistGate>
    </Provider>


  );
}

export default App;
