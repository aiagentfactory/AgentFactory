import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import DataView from './pages/DataView';
import Environment from './pages/Environment';
import Algorithm from './pages/Algorithm';
import Runtime from './pages/Runtime';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/data" element={<DataView />} />
          <Route path="/env" element={<Environment />} />
          <Route path="/algo" element={<Algorithm />} />
          <Route path="/runtime" element={<Runtime />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;