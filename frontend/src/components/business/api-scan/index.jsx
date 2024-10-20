import React, { useState } from "react";
import { AlertTriangle, Shield, Activity, ChevronRight } from "lucide-react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { Card, CardContent } from "../../ui/card";
import { Alert } from "../../ui/Alert";
import Header from "../../ui/Header";
import MetricCard from "./MetricCard";
import ScanResults from "./ScanResults";

const APIScan = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [hoveredCard, setHoveredCard] = useState(null);
  const [showScanResults, setShowScanResults] = useState(false);

  const mockScan = {
    id: "SCAN-2024-001",
    timestamp: "2024-03-20T14:35:23",
    endpoint: "/api/users/authentication",
    vulnerabilities: {
      SQL_INJECTION: {
        critical: 2,
        high: 3,
        medium: 1,
        details: [
          { location: "username_field", severity: "critical", impact: "Data breach risk" },
          { location: "password_validation", severity: "high", impact: "Authentication bypass" },
        ],
      },
      DOM_INJECTION: {
        critical: 1,
        high: 2,
        medium: 3,
        details: [
          { location: "user_input_display", severity: "critical", impact: "XSS vulnerability" },
          { location: "comment_section", severity: "high", impact: "Client-side injection" },
        ],
      },
      STRING_LENGTH: {
        critical: 0,
        high: 1,
        medium: 2,
        details: [
          { location: "email_field", severity: "high", impact: "Buffer overflow risk" },
          { location: "description_input", severity: "medium", impact: "Data truncation" },
        ],
      },
    },
  };

  const trendData = [
    { date: "2024-01", vulnerabilities: 15, resolved: 5 },
    { date: "2024-02", vulnerabilities: 12, resolved: 8 },
    { date: "2024-03", vulnerabilities: 8, resolved: 10 },
    { date: "2024-04", vulnerabilities: 5, resolved: 15 },
  ];

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? "bg-gray-900" : "bg-gray-50"}`}>
      <Header darkMode={darkMode} setDarkMode={setDarkMode} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Alert className="mb-8 border-red-500 bg-red-50">
          <AlertTriangle className="h-5 w-5 text-red-500" />
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Critical Security Alert</h3>
            <p className="text-sm text-red-700 mt-1">
              34 vulnerabilities detected across your APIs. Immediate attention required.
            </p>
          </div>
        </Alert>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <MetricCard
            title="Critical Vulnerabilities"
            value="0"
            trend={12}
            type="critical"
            icon={AlertTriangle}
            hoveredCard={hoveredCard}
            setHoveredCard={setHoveredCard}
          />
          <MetricCard
            title="Active Scans"
            value="3"
            trend={-5}
            type="info"
            icon={Activity}
            hoveredCard={hoveredCard}
            setHoveredCard={setHoveredCard}
          />
          <MetricCard
            title="Security Score"
            value="85%"
            trend={8}
            type="success"
            icon={Shield}
            hoveredCard={hoveredCard}
            setHoveredCard={setHoveredCard}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="lg:col-span-2 overflow-hidden">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold">Vulnerability Trend</h2>
                <div className="flex items-center space-x-2">
                  <div className="flex items-center">
                    <div className="w-3 h-3 rounded-full bg-red-400 mr-2" />
                    <span className="text-sm text-gray-500">Vulnerabilities</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-3 h-3 rounded-full bg-green-400 mr-2" />
                    <span className="text-sm text-gray-500">Resolved</span>
                  </div>
                </div>
              </div>
              <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={trendData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorVuln" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f87171" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#f87171" stopOpacity={0} />
                      </linearGradient>
                      <linearGradient id="colorResolved" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#4ade80" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#4ade80" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="date" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis
                      stroke="#888888"
                      fontSize={12}
                      tickLine={false}
                      axisLine={false}
                      tickFormatter={(value) => `${value}`}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "rgba(255, 255, 255, 0.8)",
                        borderRadius: "0.5rem",
                        border: "none",
                        boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                      }}
                    />
                    <Area
                      type="monotone"
                      dataKey="vulnerabilities"
                      stroke="#f87171"
                      fillOpacity={1}
                      fill="url(#colorVuln)"
                    />
                    <Area
                      type="monotone"
                      dataKey="resolved"
                      stroke="#4ade80"
                      fillOpacity={1}
                      fill="url(#colorResolved)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card
            className="lg:col-span-1 cursor-pointer hover:shadow-lg transition-all duration-300"
            onClick={() => setShowScanResults(true)}
          >
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold">Latest Scan Results</h2>
                <ChevronRight className="w-5 h-5 text-gray-400" />
              </div>
              <div className="p-4 rounded-xl bg-blue-50 border border-blue-100 mb-4">
                <p className="text-sm text-blue-600">
                  Endpoint: <span className="font-mono">{mockScan.endpoint}</span>
                </p>
              </div>
              <div className="text-sm text-gray-500">Click to view detailed results</div>
            </CardContent>
          </Card>
        </div>
      </main>

      <ScanResults onClose={() => setShowScanResults(false)} showScanResults={showScanResults} mockScan={mockScan} />
    </div>
  );
};

export default APIScan;
