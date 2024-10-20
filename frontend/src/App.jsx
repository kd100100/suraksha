import React, { useState, useEffect } from "react";
import InfoSecAPIScanReport from "./components/TestResult";
import APIScan from "./components/business/api-scan";
import "./App.css";

function App() {
  const [testResults, setTestResults] = useState(null);

  useEffect(() => {
    fetch("/results.json")
      .then((response) => response.json())
      .then((data) => setTestResults(data))
      .catch((error) => console.error("Error fetching test results:", error));
  }, []);

  return (
    <div className="App">
      <main>{testResults ? <InfoSecAPIScanReport data={testResults} /> : <p>Loading test results...</p>}</main>
      {/* <main>{testResults ? <APIScan data={testResults} /> : <p>Loading test results...</p>}</main> */}
    </div>
  );
}

export default App;
