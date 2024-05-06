import React, { useState, useEffect } from 'react';
import {Link, useNavigate} from "react-router-dom";
import {getAuth} from 'firebase/auth';
import { sendPasswordResetEmail } from "firebase/auth";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.min.css';
import './ForgotPassword.css';


const ForgotPasswordPage = () => {

    const [email, setEmail] = useState("");
    const navigate = useNavigate();
    const [error, setError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    const handlePasswordReset = async () => {
      try {
        await sendPasswordResetEmail(getAuth(), email).then(() => {
          toast.success("Password reset link has been sent. Please check your mailbox");
          setTimeout(() => {
            navigate('/', { replace: true });
          }, 5300)
        })
      } catch (err) {
        toast.error("An error occurred while sending mail.")
      }
    }

    useEffect(() => {
                return () => {
                    setError("");
                    setSuccessMessage("");
                };
            }, [email]);

        const linkStyle = {
            color: '#007bff',
            textDecoration: 'none',
        };

        const pageStyle = {
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100vh',
            background: '#1a2a33',
        };

        const inputStyle = {
                margin: '10px 0',
                padding: '10px',
                width: '300px',
                borderRadius: '5px',
                border: '1px solid #ccc',
            };

        const errorStyle = {
                color: '#ff0000',
                margin: '10px 0',
            };

        const buttonStyle = {
            padding: '0.75rem',
            borderRadius: '0.25rem',
            border: 'none',
            color: '#ffffff',
            backgroundColor: '#007bff',
            cursor: 'pointer',
            width: '20%',
        };


    return (
    <div style={pageStyle}>
        <h1>Forgot Password</h1>
        <div class="login-form">
            <h2>Enter valid email address to reset your password.</h2>
            <input  type = "text" placeholder="Email Address" value = {email} onChange={e=>setEmail(e.target.value)} />
            <button onClick={handlePasswordReset} style={buttonStyle}>Send Link</button>
                        {error && <p style={errorStyle}>{error}</p>}
                        {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
                        <p><Link to="/" style={linkStyle}>Back to Login</Link></p>
        </div>
        <ToastContainer />
    </div>
  );
}

export default ForgotPasswordPage;