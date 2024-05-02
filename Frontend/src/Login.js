import {useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import {getAuth, signInWithEmailAndPassword} from 'firebase/auth';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.min.css';
import './Login.css';

const LoginPage = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const logIn = async () => {
        try {
            await signInWithEmailAndPassword(getAuth(), email, password);
            
            const userDetails = await fetch(`http://localhost:5000/find-user-by-email?email=${email}`);

            const user = await userDetails.json();

            localStorage.setItem("username", user.userName);
            localStorage.setItem("user_id", user.user_id);
            
            console.log(user.username);
            console.log(user.user_id);
            
            window.location.reload();
        } catch (err) {
          if (err.code === 'auth/invalid-email') {
            toast.error('Invalid email ID');
          }
          else if (err.code === 'auth/user-not-found') {
              toast.error('Please check your email');
          }
          else if (err.code === 'auth/wrong-password') {
              toast.error('Please check your password');
          }
          else if (err.code === 'auth/too-many-requests') {
              toast.error('Too many attempts, please try again later');
            
          }
          else if (err.code === 'auth/invalid-credential')
          {
            toast.error('Invalid email or password')
          }
          else {
            toast.error(err.code);
          }
        }
    };



    return (
    <div className="Login">
      <nav className="container-fluid">
        <ul>
          <li style={{ fontSize: '20px' }}><strong>Smart Park</strong></li>
        </ul>
        <ul>
          <li><a href="/AboutUs">About Us</a></li>
          <li><a href="/create-account" className="make-account-btn" role="button">Make an Account</a></li>
        </ul>
      </nav>
      <div className = "container">
        <main className="login-form">

          <h2>Sign In</h2>
          <input  type = "text" placeholder="Email Address" maxLength={50} value = {email} onChange={e=>setEmail(e.target.value)} />
          <input type="password" placeholder="Password" maxLength={30} value={password} onChange={e=>setPassword(e.target.value)} />
          <button onClick={logIn}>Log In</button>
          <Link to="/ForgotPassword" className="forgot-password-link">Forgot Password?</Link>
        </main>
      </div>
      <ToastContainer />
    </div>
  );
}

export default LoginPage;