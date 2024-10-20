import React from "react";
import { ArrowLeft } from "lucide-react";
import { Card, CardContent } from "../../ui/card";

const ScanResults = ({ onClose, showScanResults, mockScan }) => (
  <div
    className={`
    fixed inset-0 z-50 bg-white dark:bg-gray-900
    transition-transform duration-500 ease-in-out
    ${showScanResults ? "translate-x-0" : "translate-x-full"}
  `}
  >
    <div className="h-full overflow-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <div>
              <h1 className="text-2xl font-bold">Scan Results</h1>
              <p className="text-sm text-gray-500">{new Date(mockScan.timestamp).toLocaleString()}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <button className="px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors">
              Export Report
            </button>
            <button className="px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors">
              Mark as Resolved
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {Object.entries(mockScan.vulnerabilities).map(([type, data]) => (
            <Card key={type} className="bg-gradient-to-br from-white to-gray-50">
              <CardContent className="p-6">
                <h3 className="text-lg font-semibold mb-4">{type}</h3>
                <div className="space-y-2">
                  {["critical", "high", "medium"].map((severity) => (
                    <div key={severity} className="flex items-center justify-between">
                      <span className="text-sm capitalize">{severity}</span>
                      <span
                        className={`
                        px-2 py-1 rounded-full text-xs font-medium
                        ${
                          severity === "critical"
                            ? "bg-red-100 text-red-600"
                            : severity === "high"
                            ? "bg-orange-100 text-orange-600"
                            : "bg-yellow-100 text-yellow-600"
                        }
                      `}
                      >
                        {data[severity]}
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="space-y-6">
          {Object.entries(mockScan.vulnerabilities).map(([type, data]) => (
            <div key={type} className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-xl font-semibold mb-4">{type}</h3>
              <div className="space-y-4">
                {data.details.map((detail, idx) => (
                  <div key={idx} className="p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium">{detail.location}</h4>
                      <span
                        className={`
                        px-2 py-1 rounded-full text-xs font-medium
                        ${
                          detail.severity === "critical"
                            ? "bg-red-100 text-red-600"
                            : detail.severity === "high"
                            ? "bg-orange-100 text-orange-600"
                            : "bg-yellow-100 text-yellow-600"
                        }
                      `}
                      >
                        {detail.severity}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">{detail.impact}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
);

export default ScanResults;
