import React from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

const ErrorComponent = ({ message, darkMode, onRetry }) => {
  return (
    <div className={`flex items-center justify-center min-h-screen ${
      darkMode ? "bg-gray-900" : "bg-gray-100"
    }`}>
      <div className={`max-w-md w-full p-8 rounded-lg shadow-lg ${
        darkMode ? "bg-gray-800" : "bg-white"
      }`}>
        <div className="flex items-center justify-center mb-6">
          <div className={`p-3 rounded-full ${
            darkMode ? "bg-red-900" : "bg-red-100"
          }`}>
            <AlertCircle className={`w-8 h-8 ${
              darkMode ? "text-red-500" : "text-red-600"
            }`} />
          </div>
        </div>
        <h2 className={`text-2xl font-bold text-center mb-4 ${
          darkMode ? "text-red-400" : "text-red-600"
        }`}>
          Error Occurred
        </h2>
        <p className={`text-center mb-6 ${
          darkMode ? "text-gray-300" : "text-gray-600"
        }`}>
          {message}
        </p>
        <div className="flex justify-center">
          <button
            onClick={onRetry}
            className={`flex items-center px-4 py-2 rounded-md transition-colors duration-300 ${
              darkMode
                ? "bg-red-700 hover:bg-red-600 text-white"
                : "bg-red-600 hover:bg-red-700 text-white"
            }`}
          >
            <RefreshCw className="w-5 h-5 mr-2" />
            Retry
          </button>
        </div>
      </div>
    </div>
  );
};

export default ErrorComponent;
