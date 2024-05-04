import './App.css';
import MapPage from './Map.js';
import LoginPage from './Login.js';
import CreateAccountPage from './MakeAccount.js';
import ForgotPasswordPage from './ForgotPassword.js';
import GaragePage from './Garage.js';
import BrowseCarsPage from './BrowseCars.js';
import AboutUsPage from './AboutUs.js';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import useUser from "./useUser.js";

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

  const {user, isLoading} = useUser();

  if(user != null && user.emailVerified){
    return (
      <Router>
        <Routes>
            <Route path="/login" element={<LoginPage/>} />
            <Route path="/" element={<MapPage/>} />
            <Route path="/create-account" element={<CreateAccountPage/>} />
            <Route path="/ForgotPassword" element={<ForgotPasswordPage/>} />
            <Route path="/Garage" element={<GaragePage/>} />
            <Route path="/BrowseCars" element={<BrowseCarsPage/>} />
            <Route path="/AboutUs" element={<AboutUsPage/>} />
        </Routes>
      </Router>
      );
  }
  else {
    return (
      <Router>
        <Routes>
            <Route path="/map" element={<MapPage/>} />
            <Route path="/" element={<LoginPage/>} />
            <Route path="/create-account" element={<CreateAccountPage/>} />
            <Route path="/ForgotPassword" element={<ForgotPasswordPage/>} />
            <Route path="/AboutUs" element={<AboutUsPage/>} />
        </Routes>
      </Router>
      );
    }
  }

export default App;
