import './App.css';
import MapPage from './Map.js';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
        <Routes>
            <Route path="/" element={<MapPage/>} />
        </Routes>
    </Router>
    );
  }

export default App;
