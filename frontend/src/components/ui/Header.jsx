import React from "react";
import { Shield, Search, BellRing, Settings, Sun, Moon } from "lucide-react";

const Header = ({ darkMode, setDarkMode }) => (
  <header
    className={`
    sticky top-0 z-50
    backdrop-blur-lg bg-white/75 dark:bg-gray-900/75
    border-b border-gray-200 dark:border-gray-800
  `}
  >
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex items-center justify-between h-16">
        <div className="flex items-center space-x-3">
          <div className="relative group">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-teal-400 rounded-lg blur opacity-75 group-hover:opacity-100 transition duration-1000 group-hover:duration-200" />
            <Shield className="relative w-8 h-8 text-white bg-blue-500 rounded-lg p-1.5" />
          </div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-teal-400">
            Suraksha Security
          </span>
        </div>
        <div className="flex items-center space-x-6">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search scans..."
              className="w-full pl-10 pr-4 py-2 rounded-full
                bg-gray-100 border-transparent focus:border-blue-500 focus:ring-2 focus:ring-blue-200
                transition-all duration-300"
            />
          </div>
          <button className="relative p-2 rounded-full hover:bg-gray-100 transition-colors duration-200">
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-xs text-white flex items-center justify-center">
              3
            </div>
            <BellRing className="w-5 h-5" />
          </button>
          <button className="p-2 rounded-full hover:bg-gray-100 transition-colors duration-200">
            <Settings className="w-5 h-5" />
          </button>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors duration-200"
          >
            {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </div>
      </div>
    </div>
  </header>
);

export default Header;
