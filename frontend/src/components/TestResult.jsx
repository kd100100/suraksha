import React, { useState, useEffect } from "react";
import {
  AlertTriangle,
  CheckCircle,
  XCircle,
  ChevronDown,
  ChevronUp,
  AlertOctagon,
  Shield,
  Moon,
  Sun,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart as RePieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts";

const COLORS = ["#00C49F", "#FF8042", "#0088FE", "#FFBB28", "#8884d8"];

const TestItem = ({ test, darkMode }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="mb-2">
      <div
        className={`flex justify-between items-center p-2 cursor-pointer ${
          darkMode ? "bg-gray-700" : "bg-gray-100"
        } rounded`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center">
          {test.is_valid ? (
            <CheckCircle className="text-green-500 mr-2" size={16} />
          ) : (
            <XCircle className="text-red-500 mr-2" size={16} />
          )}
          <span className={`font-semibold ${darkMode ? "text-white" : "text-gray-800"}`}>
            {`${test.modification.key}: ${test.modification.value}`}
          </span>
        </div>
        {isOpen ? (
          <ChevronUp className="text-blue-500" size={16} />
        ) : (
          <ChevronDown className="text-blue-500" size={16} />
        )}
      </div>
      {isOpen && (
        <div className={`mt-2 pl-4 text-sm ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
          <p>
            <strong>URL:</strong> {test.request.url}
          </p>
          <p>
            <strong>Method:</strong> {test.request.method}
          </p>
          <p>
            <strong>Status Code:</strong> {test.response.status_code}
          </p>
          <div
            className={`mt-2 p-2 rounded ${test.is_valid ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}
          >
            <p>
              <strong>Status:</strong> {test.response.body.statusCode}
            </p>
            <p>
              <strong>Message:</strong> {test.response.body.statusMessage}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

const TestResult = ({ result, darkMode }) => {
  const [isOpen, setIsOpen] = useState(false);

  // Group tests by modification type
  const groupedTests = result.modification
    ? { [result.modification.type]: [result] }
    : result.results.reduce((acc, test) => {
        const type = test.modification.type;
        if (!acc[type]) acc[type] = [];
        acc[type].push(test);
        return acc;
      }, {});

  return (
    <div
      className={`border ${
        darkMode ? "border-gray-700" : "border-gray-200"
      } rounded-lg p-4 mb-4 hover:shadow-lg transition-all duration-300 ${darkMode ? "bg-gray-800" : "bg-white"}`}
    >
      <div className="flex justify-between items-center cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
        <div className="flex items-center">
          <span className={`font-semibold ${darkMode ? "text-white" : "text-gray-800"}`}>Test Results</span>
        </div>
        {isOpen ? <ChevronUp className="text-blue-500" /> : <ChevronDown className="text-blue-500" />}
      </div>
      {isOpen && (
        <div className={`mt-4 space-y-4 ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
          {Object.entries(groupedTests).map(([type, tests]) => (
            <div key={type} className="border-t pt-2">
              <h3 className="font-semibold mb-2">{type}</h3>
              {tests.map((test, index) => (
                <TestItem key={index} test={test} darkMode={darkMode} />
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const ScanTypeChart = ({ results }) => {
  const data = [
    { name: "Valid", value: results.filter((r) => r.is_valid).length },
    { name: "Invalid", value: results.filter((r) => !r.is_valid).length },
  ];

  return (
    <ResponsiveContainer width="100%" height={200}>
      <RePieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={80}
          fill="#8884d8"
          paddingAngle={5}
          dataKey="value"
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </RePieChart>
    </ResponsiveContainer>
  );
};

const ScanType = ({ type, results, overallResult, totalRuntime, darkMode }) => {
  const [isOpen, setIsOpen] = useState(false);

  const gradientColor = overallResult
    ? `${darkMode ? "from-green-700 to-blue-900" : "from-green-400 to-blue-500"}`
    : `${darkMode ? "from-red-500 to-pink-600" : "from-red-400 to-pink-500"}`;

  return (
    <div
      className={`mb-6 border ${
        darkMode ? "border-gray-700" : "border-gray-200"
      } rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 ${
        darkMode ? "bg-gray-800" : "bg-white"
      }`}
    >
      <div
        className={`flex justify-between items-center p-4 cursor-pointer bg-gradient-to-r ${gradientColor} text-white`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center">
          <AlertTriangle className="mr-2" />
          <span className="font-semibold text-lg">{type}</span>
        </div>
        <div className="flex items-center">
          <span className="mr-4">Tests: {results.length}</span>
          <span className="mr-4">Runtime: {totalRuntime.toFixed(2)}s</span>
          {isOpen ? <ChevronUp /> : <ChevronDown />}
        </div>
      </div>
      {isOpen && (
        <div className="p-4">
          <ScanTypeChart results={results} />
          <div className="mt-4 space-y-4">
            <TestResult result={{ type, results, is_valid: overallResult }} darkMode={darkMode} />
          </div>
        </div>
      )}
    </div>
  );
};

const OverallMetrics = ({ data, darkMode }) => {
  const totalTests = data.reduce((sum, scanType) => sum + scanType.results.length, 0);
  const totalRuntime = data.reduce((sum, scanType) => sum + scanType.total_runtime, 0);
  const passedTests = data.reduce((sum, scanType) => sum + scanType.results.filter((r) => r.is_valid).length, 0);

  const chartData = data.map(scanType => ({
    name: scanType.type,
    Pass: scanType.results.filter(r => r.is_valid).length,
    Fail: scanType.results.filter(r => !r.is_valid).length
  }));

  return (
    <div className={`${darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-800"} rounded-xl shadow-2xl p-8 mb-8`}>
      <h2 className="text-2xl font-bold mb-4">Overall Metrics</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className={`${darkMode ? "bg-blue-900" : "bg-blue-100"} p-4 rounded-lg`}>
          <p className={`${darkMode ? "text-blue-200" : "text-blue-800"} font-semibold`}>Total Tests</p>
          <p className="text-3xl font-bold">{totalTests}</p>
        </div>
        <div className={`${darkMode ? "bg-green-900" : "bg-green-100"} p-4 rounded-lg`}>
          <p className={`${darkMode ? "text-green-200" : "text-green-800"} font-semibold`}>Passed Tests</p>
          <p className="text-3xl font-bold">{passedTests}</p>
        </div>
        <div className={`${darkMode ? "bg-purple-900" : "bg-purple-100"} p-4 rounded-lg`}>
          <p className={`${darkMode ? "text-purple-200" : "text-purple-800"} font-semibold`}>Total Runtime</p>
          <p className="text-3xl font-bold">{totalRuntime.toFixed(2)}s</p>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#555" : "#ccc"} />
          <XAxis dataKey="name" stroke={darkMode ? "#fff" : "#333"} />
          <YAxis stroke={darkMode ? "#fff" : "#333"} />
          <Tooltip
            contentStyle={{
              backgroundColor: darkMode ? "#333" : "#fff",
              border: `1px solid ${darkMode ? "#555" : "#ccc"}`,
              color: darkMode ? "#fff" : "#333",
            }}
          />
          <Legend />
          <Bar dataKey="Pass" fill={darkMode ? "#8CD790" : "#A8D5BA"} />
          <Bar dataKey="Fail" fill={darkMode ? "#E57373" : "#F28C8C"} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const TrendChart = ({ darkMode }) => {
  const data = [
    { name: "1st Jan '24, 5:34 PM", vulnerabilities: 15 },
    { name: "1st Jan '24, 10:34 PM", vulnerabilities: 8 },
    { name: "2nd Jan '24, 12:11 PM", vulnerabilities: 10 },
    { name: "2nd Jan '24, 6:02 PM", vulnerabilities: 0 },
  ];

  return (
    <div className={`${darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-800"} rounded-xl shadow-2xl p-8 mb-8`}>
      <h2 className="text-2xl font-bold mb-4">Vulnerability Trend</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#555" : "#ccc"} />
          <XAxis dataKey="name" stroke={darkMode ? "#fff" : "#333"} />
          <YAxis stroke={darkMode ? "#fff" : "#333"} />
          <Tooltip
            contentStyle={{
              backgroundColor: darkMode ? "#333" : "#fff",
              border: `1px solid ${darkMode ? "#555" : "#ccc"}`,
              color: darkMode ? "#fff" : "#333",
            }}
          />
          <Legend />
          <Line type="monotone" dataKey="vulnerabilities" stroke="#FF8042" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

const InfoSecAPIScanReport = ({ data }) => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div
      className={`min-h-screen ${
        darkMode ? "bg-gray-900" : "bg-gradient-to-br from-blue-50 to-indigo-100"
      } p-8 transition-all duration-300`}
    >
      <div className="max-w-7xl mx-auto">
        <div
          className={`${
            darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-800"
          } rounded-xl shadow-2xl p-8 mb-8 transition-all duration-300`}
        >
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <img src="/logo.svg" alt="Suraksha Logo" className="w-16 h-16" />
              <div className="ml-4">
                <h1 className="text-4xl font-bold">Suraksha</h1>
                <p className={`${darkMode ? "text-gray-300" : "text-gray-600"}`}>InfoSec API Scan Dashboard</p>
              </div>
            </div>
            <div className="flex items-center">
              <div className="mr-4">
                <p className={`text-sm ${darkMode ? "text-gray-400" : "text-gray-500"}`}>Last Updated</p>
                <p className="text-lg font-semibold">{currentTime.toLocaleString()}</p>
              </div>
              <button
                onClick={() => setDarkMode(!darkMode)}
                className={`p-2 rounded-full ${darkMode ? "bg-yellow-400 text-gray-900" : "bg-gray-200 text-gray-800"}`}
              >
                {darkMode ? <Sun size={24} /> : <Moon size={24} />}
              </button>
            </div>
          </div>
          <div
            className={`flex items-center ${
              darkMode
                ? "bg-yellow-900 border-yellow-700 text-yellow-100"
                : "bg-yellow-100 border-yellow-500 text-yellow-700"
            } border-l-4 p-4 rounded transition-all duration-300`}
          >
            <AlertOctagon className="mr-2" />
            <p>Attention: Multiple security vulnerabilities detected. Immediate action required.</p>
          </div>
        </div>

        <OverallMetrics data={data} darkMode={darkMode} />

        {data.map((scanType, index) => (
          <ScanType
            key={index}
            type={scanType.type}
            results={scanType.results}
            overallResult={scanType.is_valid}
            totalRuntime={scanType.total_runtime}
            darkMode={darkMode}
          />
        ))}

        <TrendChart darkMode={darkMode} />
      </div>
    </div>
  );
};

export default InfoSecAPIScanReport;
