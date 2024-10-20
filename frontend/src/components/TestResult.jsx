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
  Activity,
  Bolt,
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
  AreaChart,
  Area,
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
          {test.isValid ? (
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
            className={`mt-2 p-2 rounded ${test.isValid ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}
          >
            <p>
              <strong>Status:</strong> {test.response.body.message}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

const TestResult = ({ result, darkMode }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div
      className={`border ${
        darkMode ? "border-gray-700" : "border-gray-200"
      } rounded-lg p-4 mb-4 hover:shadow-lg transition-all duration-300 ${darkMode ? "bg-gray-800" : "bg-white"}`}
    >
      <div className="flex justify-between items-center cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
        <div className="flex items-center">
          <span className={`font-semibold ${darkMode ? "text-white" : "text-gray-800"}`}>
            {result.validation} Results
          </span>
        </div>
        {isOpen ? <ChevronUp className="text-blue-500" /> : <ChevronDown className="text-blue-500" />}
      </div>
      {isOpen && (
        <div className={`mt-4 space-y-4 ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
          {result.results.map((test, index) => (
            <TestItem key={index} test={test} darkMode={darkMode} />
          ))}
        </div>
      )}
    </div>
  );
};

const ScanTypeChart = ({ results }) => {
  const data = [
    { name: "Valid", value: results.filter((r) => r.isValid).length },
    { name: "Invalid", value: results.filter((r) => !r.isValid).length },
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

const ScanType = ({ type, results, darkMode }) => {
  const [isOpen, setIsOpen] = useState(false);

  const overallResult = results.every((r) => r.isValid);
  const totalRuntime = results.reduce((sum, r) => sum + r.executionTime, 0);

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
            <TestResult result={{ validation: type, results }} darkMode={darkMode} />
          </div>
        </div>
      )}
    </div>
  );
};

const OverallMetrics = ({ data, darkMode }) => {
  const totalTests = data.reduce((sum, scanType) => sum + scanType.results.length, 0);
  const totalRuntime = data.reduce(
    (sum, scanType) => sum + scanType.results.reduce((sum, r) => sum + r.executionTime, 0),
    0
  );
  const passedTests = data.reduce((sum, scanType) => sum + scanType.results.filter((r) => r.isValid).length, 0);

  const chartData = data.map((scanType) => ({
    name: scanType.validation,
    Pass: scanType.results.filter((r) => r.isValid).length,
    Fail: scanType.results.filter((r) => !r.isValid).length,
  }));

  return (
    <div className={`${darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-800"} rounded-xl shadow-2xl p-8 mb-8`}>
      <div className="flex items-center gap-3 mb-4">
        <Bolt className="w-6 h-6 text-orange-500" />
        <h2 className="text-2xl font-bold">Overall Metrics</h2>
      </div>
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

const TrendChart = ({ darkMode, trendData }) => {
  const data = trendData.map((item) => ({
    name: new Date(item.createdAt).toLocaleString(),
    vulnerabilities: item.fail,
  }));

  const CustomTooltip = ({ active, payload, label }) => {
    if (!active || !payload?.length) return null;

    return (
      <div
        className={`${darkMode ? "bg-gray-900" : "bg-white"} p-4 rounded-lg shadow-lg border ${
          darkMode ? "border-gray-700" : "border-gray-200"
        }`}
      >
        <p className={`text-sm ${darkMode ? "text-gray-400" : "text-gray-600"}`}>{label}</p>
        <p className="text-lg font-bold mt-1">{payload[0].value} vulnerabilities</p>
      </div>
    );
  };

  return (
    <div className={`${darkMode ? "bg-gray-800 text-white" : "bg-white"} rounded-xl shadow-2xl p-8 mb-8`}>
      <div className="flex items-center gap-3 mb-6">
        <Activity className="w-6 h-6 text-orange-500" />
        <h2 className="text-2xl font-bold">Vulnerability Trend</h2>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="vulnerabilityGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#FF8042" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#FF8042" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? "#374151" : "#E5E7EB"} vertical={false} />
          <XAxis dataKey="name" stroke={darkMode ? "#9CA3AF" : "#6B7280"} fontSize={12} tickMargin={12} />
          <YAxis stroke={darkMode ? "#9CA3AF" : "#6B7280"} fontSize={12} tickMargin={8} />
          <Tooltip content={CustomTooltip} />
          <Area
            type="monotone"
            dataKey="vulnerabilities"
            stroke="#FF8042"
            strokeWidth={2}
            fill="url(#vulnerabilityGradient)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

const InfoSecAPIScanReport = ({ scanData, darkMode, setDarkMode, onBackToCreate }) => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  if (!scanData) {
    return <div>No scan data available.</div>;
  }

  const { scan, validation_results } = scanData;

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
            <p>Scan completed for {scan.url}. Review the results below.</p>
          </div>
        </div>

        <OverallMetrics data={validation_results} darkMode={darkMode} />

        {scanData.validation_results.map((scanType, index) => (
          <ScanType key={index} type={scanType.validation} results={scanType.results} darkMode={darkMode} />
        ))}

        <TrendChart darkMode={darkMode} trendData={scanData.trend_data} />

        {/* <button
          onClick={onBackToCreate}
          className={`mt-4 px-4 py-2 rounded ${
            darkMode ? "bg-blue-600 hover:bg-blue-700" : "bg-blue-500 hover:bg-blue-600"
          } text-white font-semibold transition-colors duration-300`}
        >
          Back to Create Scan
        </button> */}
      </div>
    </div>
  );
};

export default InfoSecAPIScanReport;
