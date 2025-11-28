import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-xl font-bold">Agent Factory</div>
        <div className="space-x-4">
          <Link to="/" className="hover:text-gray-300">Dashboard</Link>
          <Link to="/data" className="hover:text-gray-300">Data</Link>
          <Link to="/env" className="hover:text-gray-300">Environment</Link>
          <Link to="/algo" className="hover:text-gray-300">Algorithm</Link>
          <Link to="/runtime" className="hover:text-gray-300">Runtime</Link>
        </div>
      </div>
    </nav>
  );
}
