// src/components/Navbar.jsx
import { Link } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';

export default function Navbar() {
  return (
    <nav className="bg-white dark:bg-gray-900 text-black dark:text-white shadow px-4 py-3 flex justify-between items-center">
      <div className="font-bold text-lg">
        <Link to="/">Bukuku</Link>
      </div>
      <div className="flex gap-4 items-center">
        <Link to="/login" className="hover:underline">
          Login
        </Link>
        <Link to="/register" className="hover:underline">
          Register
        </Link>
        <ThemeToggle />
      </div>
    </nav>
  );
}
