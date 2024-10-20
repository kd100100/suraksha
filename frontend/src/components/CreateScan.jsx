import React, { useState, useEffect } from "react";
import { PlayCircle, Plus, AlertCircle, Trash2, Moon, Sun } from "lucide-react";
import { createScan } from "../services/apiService";
import ErrorComponent from "./ErrorComponent";

const KeyValuePairInput = ({ title, darkMode, onItemsChange }) => {
  const [items, setItems] = useState([]);

  const addItem = () => {
    const newItems = [...items, { key: "", value: "" }];
    setItems(newItems);
    onItemsChange(newItems);
  };

  const removeItem = (index) => {
    const newItems = items.filter((_, i) => i !== index);
    setItems(newItems);
    onItemsChange(newItems);
  };

  const updateItem = (index, field, value) => {
    const newItems = items.map((item, i) => (i === index ? { ...item, [field]: value } : item));
    setItems(newItems);
    onItemsChange(newItems);
  };

  return (
    <div className="mb-6">
      <div className="flex justify-between items-center mb-2">
        <label className={`font-medium ${darkMode ? "text-gray-300" : "text-gray-700"}`}>{title}</label>
        <button
          type="button"
          onClick={addItem}
          className={`flex items-center gap-2 px-3 py-1 rounded-md text-sm
            ${
              darkMode ? "bg-blue-900 hover:bg-blue-800 text-blue-100" : "bg-blue-100 hover:bg-blue-200 text-blue-900"
            }`}
        >
          <Plus size={16} />
          Add {title}
        </button>
      </div>
      {items.map((item, index) => (
        <div key={`${title}-${index}`} className="flex gap-2 mb-2">
          <input
            type="text"
            value={item.key}
            onChange={(e) => updateItem(index, "key", e.target.value)}
            placeholder="Key"
            className={`flex-1 p-2 rounded-md border ${
              darkMode ? "bg-gray-700 border-gray-600" : "bg-white border-gray-300"
            }`}
          />
          <input
            type="text"
            value={item.value}
            onChange={(e) => updateItem(index, "value", e.target.value)}
            placeholder="Value"
            className={`flex-1 p-2 rounded-md border ${
              darkMode ? "bg-gray-700 border-gray-600" : "bg-white border-gray-300"
            }`}
          />
          <button type="button" onClick={() => removeItem(index)} className="p-2 text-red-500 hover:text-red-700">
            <Trash2 size={20} />
          </button>
        </div>
      ))}
    </div>
  );
};

const CreateScan = ({ darkMode, setDarkMode, onScanCreated }) => {
  const [formData, setFormData] = useState({
    method: "POST",
    url: "",
    headers: [],
    urlParams: [],
    body: {},
  });
  const [currentTime, setCurrentTime] = useState(new Date());
  const [jsonError, setJsonError] = useState("");
  const [bodyString, setBodyString] = useState("{}");
  const [copyStatus, setCopyStatus] = useState("Copy to Clipboard");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const handleJsonInput = (value) => {
    setBodyString(value);
    try {
      const parsedJson = JSON.parse(value);
      setJsonError("");
      setFormData((prev) => ({ ...prev, body: parsedJson }));
    } catch (e) {
      setJsonError("Invalid JSON format");
    }
  };

  const handleCopy = async () => {
    try {
      const previewData = formatData();
      await navigator.clipboard.writeText(JSON.stringify(previewData, null, 2));
      setCopyStatus("Copied!");
      setTimeout(() => setCopyStatus("Copy to Clipboard"), 2000);
    } catch (err) {
      setCopyStatus("Failed to copy");
      setTimeout(() => setCopyStatus("Copy to Clipboard"), 2000);
    }
  };

  const updateHeaders = (items) => {
    setFormData((prev) => ({ ...prev, headers: items }));
  };

  const updateUrlParams = (items) => {
    setFormData((prev) => ({ ...prev, urlParams: items }));
  };

  const formatData = () => {
    return {
      ...formData,
      headers: Object.fromEntries(formData.headers.map((h) => [h.key, h.value]).filter((h) => h[0] !== "")),
      urlParams: Object.fromEntries(formData.urlParams.map((p) => [p.key, p.value]).filter((h) => h[0] !== "")),
    };
  };

  const handleStartScan = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const scanData = formatData();
      const result = await createScan(scanData);
      console.log("Scan created successfully:", result);
      onScanCreated(result.scan_id);
    } catch (err) {
      console.error("Error creating scan:", err);
      setError("Failed to create scan. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    setError(null);
    // You can choose to reset the form or keep the current data
    // setFormData({ method: "POST", url: "", headers: [], urlParams: [], body: {} });
    // setBodyString("{}");
  };

  if (error) {
    return <ErrorComponent message={error} darkMode={darkMode} onRetry={handleRetry} />;
  }

  return (
    <div className={`min-h-screen ${darkMode ? "bg-gray-900" : "bg-gradient-to-br from-blue-50 to-indigo-100"} p-8`}>
      <div className="max-w-7xl mx-auto">
        <div className={`${darkMode ? "bg-gray-800 text-white" : "bg-white"} rounded-xl shadow-2xl p-8 mb-8`}>
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <img src="/logo.svg" alt="Suraksha Logo" className="w-16 h-16" />
              <div className="ml-4">
                <h1 className="text-4xl font-bold">Suraksha</h1>
                <p className={`${darkMode ? "text-gray-300" : "text-gray-600"}`}>InfoSec API Scan Dashboard</p>
              </div>
            </div>
            <div className="flex items-center gap-6">
              <button
                type="button"
                onClick={handleStartScan}
                disabled={isLoading}
                className={`flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-red-400 to-pink-500 text-white rounded-md hover:bg-blue-700 ${
                  isLoading ? "opacity-50 cursor-not-allowed" : ""
                }`}
              >
                <PlayCircle size={20} />
                {isLoading ? "Creating Scan..." : "Start Scan"}
              </button>
              <button
                type="button"
                onClick={() => setDarkMode(!darkMode)}
                className={`p-2 rounded-full ${darkMode ? "bg-yellow-400 text-gray-900" : "bg-gray-200 text-gray-800"}`}
              >
                {darkMode ? <Sun size={24} /> : <Moon size={24} />}
              </button>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <strong className="font-bold">Error!</strong>
            <span className="block sm:inline"> {error}</span>
          </div>
        )}

        <div className="grid grid-cols-2 gap-8">
          <div className={`${darkMode ? "bg-gray-800 text-white" : "bg-white"} rounded-xl shadow-2xl p-8`}>
            <div className="grid grid-cols-3 gap-4 mb-6">
              <div>
                <label className={`block mb-2 font-medium ${darkMode ? "text-gray-300" : "text-gray-700"}`}>
                  Method
                </label>
                <select
                  value={formData.method}
                  onChange={(e) => setFormData((prev) => ({ ...prev, method: e.target.value }))}
                  className={`w-full p-2 rounded-md border ${
                    darkMode ? "bg-gray-700 border-gray-600" : "bg-white border-gray-300"
                  }`}
                >
                  <option>POST</option>
                  <option>GET</option>
                  <option>PUT</option>
                  <option>DELETE</option>
                </select>
              </div>
              <div className="col-span-2">
                <label className={`block mb-2 font-medium ${darkMode ? "text-gray-300" : "text-gray-700"}`}>URL</label>
                <input
                  type="text"
                  value={formData.url}
                  onChange={(e) => setFormData((prev) => ({ ...prev, url: e.target.value }))}
                  className={`w-full p-2 rounded-md border ${
                    darkMode ? "bg-gray-700 border-gray-600" : "bg-white border-gray-300"
                  }`}
                  placeholder="https://api.example.com/endpoint"
                />
              </div>
            </div>

            <KeyValuePairInput title="URL Parameters" darkMode={darkMode} onItemsChange={updateUrlParams} />

            <KeyValuePairInput title="Headers" darkMode={darkMode} onItemsChange={updateHeaders} />

            <div>
              <label className={`block mb-2 font-medium ${darkMode ? "text-gray-300" : "text-gray-700"}`}>
                Request Body (JSON)
              </label>
              <textarea
                value={bodyString}
                onChange={(e) => handleJsonInput(e.target.value)}
                rows={15}
                className={`w-full p-3 rounded-md border font-mono text-sm ${
                  darkMode ? "bg-gray-700 border-gray-600" : "bg-white border-gray-300"
                } ${jsonError ? "border-red-500" : ""}`}
                placeholder="{}"
              />
              {jsonError && (
                <div className="flex items-center gap-2 mt-2 text-red-500">
                  <AlertCircle size={16} />
                  <span className="text-sm">{jsonError}</span>
                </div>
              )}
            </div>
          </div>
          <div className={`${darkMode ? "bg-gray-800 text-white" : "bg-white"} rounded-xl shadow-2xl p-8`}>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Request Preview</h2>
              <button
                type="button"
                onClick={handleCopy}
                className={`px-3 py-1 rounded-md text-sm
                  ${
                    darkMode
                      ? "bg-blue-900 hover:bg-blue-800 text-blue-100"
                      : "bg-blue-100 hover:bg-blue-200 text-blue-900"
                  }`}
              >
                {copyStatus}
              </button>
            </div>
            <pre className={`p-4 rounded-lg ${darkMode ? "bg-gray-700" : "bg-gray-50"} overflow-auto h-[600px]`}>
              {JSON.stringify(formatData(formData), null, 2)}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateScan;
