import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import DataFactory from './pages/factories/DataFactory';
import EnvFactory from './pages/factories/EnvFactory';
import AlgoFactory from './pages/factories/AlgoFactory';
import RewardFactory from './pages/factories/RewardFactory';
import ComputeFactory from './pages/factories/ComputeFactory';
import RuntimeFactory from './pages/factories/RuntimeFactory';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/factory/data" element={<DataFactory />} />
          <Route path="/factory/env" element={<EnvFactory />} />
          <Route path="/factory/algo" element={<AlgoFactory />} />
          <Route path="/factory/reward" element={<RewardFactory />} />
          <Route path="/factory/compute" element={<ComputeFactory />} />
          <Route path="/factory/runtime" element={<RuntimeFactory />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;