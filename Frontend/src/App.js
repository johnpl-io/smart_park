import './App.css';
import MapPage from './Map.js';
import LoginPage from './Login.js'
import CreateAccountPage from './MakeAccount.js'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';

const firebaseConfig = {
  apiKey: "AIzaSyBJXSdjGa3Lyq5iNRLQQXidjuGRCNK-4CQ",
  authDomain: "smart-park-421315.firebaseapp.com",
  projectId: "smart-park-421315",
  storageBucket: "smart-park-421315.appspot.com",
  messagingSenderId: "883347988988",
  appId: "1:883347988988:web:e18317f86f42dde7bbd279",
  measurementId: "G-42192J8Z19"
};

const app = firebase.initializeApp(firebaseConfig);

function App() {
  return (
    <Router>
        <Routes>
            <Route path="/Map" element={<MapPage/>} />
            <Route path="/" element={<LoginPage/>} />
            <Route path="/create-account" element={<CreateAccountPage/>} />
        </Routes>
    </Router>
    );
  }

export default App;
