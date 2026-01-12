import { useState } from "react";

import { parseJobs, matchJobs } from "./services/api";
import JDInput from "./components/JDInput";
import ResultsTable from "./components/ResultsTable";
import { ResumeJdSection } from "./components/ResumeJdSection/ResumeJdSection";
import {Header} from "./components/Header/Header";

export default function App() {
  const [resume, setResume] = useState(null);
  const [results, setResults] = useState([]);

  const analyze = async (jobs) => {
    const parsedJobs = await parseJobs(jobs);
    const res = await matchJobs({
      resume,
      jobs: parsedJobs.data.jobs
    });
    setResults(res.data.results);
  };
  console.log("resume:", resume);

  return (
    <div style={{ padding: 20 }}>
      <Header />
      <ResumeJdSection />

      {/* <ResumeUpload onParsed={setResume} />

      <JDInput onSubmit={analyze} /> */}

      <ResultsTable results={results} />
    </div>
  );
}
