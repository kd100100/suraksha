import React, { useState, useEffect } from "react";
import InfoSecAPIScanReport from "./components/TestResult";
import CreateScan from "./components/CreateScan";
import LoadingComponent from "./components/LoadingComponent";
import ErrorComponent from "./components/ErrorComponent";
import { getScanResults } from "./services/apiService";
import "./App.css";

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [showCreateScan, setShowCreateScan] = useState(true);
  const [scanId, setScanId] = useState(null);
  const [scanData, setScanData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  let pollInterval = null;

  useEffect(() => {
    if (scanId && !scanData) {
      pollInterval = setInterval(fetchScanResults, 1000);

      return () => clearInterval(pollInterval);
    }
    if (scanData && scanData.scan.status === "COMPLETED") {
      clearInterval(pollInterval);
    }
  }, [scanId, scanData]);

  useEffect(() => {
    // setTimeout(() => {
    // setScanId("6617ff22-ed87-4f5e-9d2b-c36de151d0ca");
    // setShowCreateScan(false);
    // setIsLoading(true);
    // }, 5000);
  }, []);

  const fetchScanResults = async () => {
    try {
      setIsLoading(true);
      const results = await getScanResults(scanId);
      if (results.scan.status === "COMPLETED") {
        setScanData(results);
        setIsLoading(false);
        clearInterval(pollInterval);
      }
    } catch (err) {
      console.error("Error fetching scan results:", err);
      setError("Failed to fetch scan results. Please try again.");
      setIsLoading(false);
    }
  };

  const handleScanCreated = (newScanId) => {
    setScanId(newScanId);
    setShowCreateScan(false);
    setScanData(null);
    setIsLoading(true);
    setError(null);
  };

  const handleBackToCreate = () => {
    setScanId(null);
    setScanData(null);
    setShowCreateScan(true);
    setIsLoading(false);
    setError(null);
  };

  const handleRetry = () => {
    setError(null);
    setIsLoading(true);
    if (scanId) {
      fetchScanResults();
    } else {
      setShowCreateScan(true);
    }
  };

  if (error) {
    return <ErrorComponent message={error} darkMode={darkMode} onRetry={handleRetry} />;
  }

  return (
    <div className={darkMode ? "dark" : ""}>
      {showCreateScan ? (
        <CreateScan darkMode={darkMode} setDarkMode={setDarkMode} onScanCreated={handleScanCreated} />
      ) : (
        <>
          {isLoading && <LoadingComponent darkMode={darkMode} />}
          {scanData && !isLoading && (
            <InfoSecAPIScanReport
              scanData={scanData}
              darkMode={darkMode}
              setDarkMode={setDarkMode}
              onBackToCreate={handleBackToCreate}
            />
          )}
        </>
      )}
    </div>
  );
}

export default App;
