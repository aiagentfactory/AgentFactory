import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Training from './pages/Training';
import DataEnv from './pages/DataEnv';
import Playground from './pages/Playground';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/training" element={<Training />} />
          <Route path="/data" element={<DataEnv />} />
          <Route path="/playground" element={<Playground />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
