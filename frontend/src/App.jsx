import { useState } from "react";

import { parseJobs, matchJobs } from "./services/api";
import ResultsTable from "./components/ResultsTable/ResultsTable";
import { ResumeJdSection } from "./components/ResumeJdSection/ResumeJdSection";
import {Header} from "./components/Header/Header";

export default function App() {

  return (
    <div style={{ padding: 20 }}>
      <Header />
      <ResumeJdSection />
    </div>
  );
}
