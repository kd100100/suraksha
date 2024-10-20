import React from "react";

const LoadingComponent = ({ darkMode }) => {
  return (
    <div
      className={`flex flex-col items-center justify-center min-h-screen ${
        darkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-800"
      }`}
    >
      <div className="relative w-24 h-24">
        <div className="absolute inset-0 rounded-full bg-gradient-to-r from-red-400 to-pink-500 animate-spin"></div>
        <div className={`absolute inset-1 rounded-full ${darkMode ? "bg-gray-900" : "bg-gray-100"}`}></div>
      </div>
      <div className="mt-4 text-center">
        <p className="text-lg font-semibold">Loading scan results...</p>
        <p className="mt-2 text-sm text-gray-500">This may take a few moments</p>
      </div>
    </div>
  );
};

export default LoadingComponent;
