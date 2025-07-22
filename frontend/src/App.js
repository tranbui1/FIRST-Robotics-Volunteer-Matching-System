import './App.css';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Questionnaire from './pages/Questionnaire';

function App() {
  return (
    <Routes>
       <Route path="/" element={<Home />} />
       <Route path="/match" element={<Questionnaire />} />
    </Routes>
  );
}

export default App;
