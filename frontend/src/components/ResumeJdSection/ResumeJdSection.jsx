import React, { useState } from 'react';
import './ResumeJdSection.css';

import { JDInput } from '../JDInput/JDInput';
import { ResumeSection } from '../ResumeSection/ResumeSection';
import ResultsTable from '../ResultsTable/ResultsTable';
import { matchJobs } from '../../services/api';

export const ResumeJdSection = () => {
  const [resumeData, setResumeData] = useState(null);
  const [jds, setJds] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sortBy, setSortBy] = useState('match');

  const handleResumeData = (data) => {
    setResumeData(data);
  };

  const handleJDsChange = (jobDescriptions) => {
    setJds(jobDescriptions);
  };

  const handleAnalyze = async () => {
    if (!resumeData) {
      alert('Please upload a resume first');
      return;
    }

    if (!jds.length || !jds.some(jd => jd.text.trim())) {
      alert('Please add at least one job description');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        resume_id: resumeData.resume_id,
        skills: resumeData.skills || [],
        total_yoe: resumeData.total_yoe || 0,
        roles: resumeData.roles || [],
        job_descriptions: jds.map(jd => ({
          jd_id: jd.id,
          title: jd.title || 'Untitled',
          company: jd.company || 'Unknown',
          text: jd.text,
        })),
      };

      const response = await matchJobs(payload);
      const sortedResults = sortResults(response.data.results || [], sortBy);
      setResults(sortedResults);
    } catch (error) {
      console.error('Error analyzing jobs:', error);
      alert('Failed to analyze jobs. Please check your input and try again.');
    } finally {
      setLoading(false);
    }
  };

  const sortResults = (items, sortKey) => {
    const sorted = [...items];
    if (sortKey === 'match') {
      return sorted.sort((a, b) => (b.overall_match || 0) - (a.overall_match || 0));
    }
    if (sortKey === 'gap') {
      return sorted.sort((a, b) => {
        const gapA = parseInt(a.experience_gap) || 0;
        const gapB = parseInt(b.experience_gap) || 0;
        return gapA - gapB;
      });
    }
    return sorted;
  };

  const handleSortChange = (e) => {
    const key = e.target.value;
    setSortBy(key);
    setResults(sortResults(results, key));
  };

  return (
    <>
      <section className="resume-jd">
        <div className="columns">
          <div className="col left">
            <ResumeSection onResumeData={handleResumeData} />
          </div>
          <div className="col right">
            <JDInput onChange={handleJDsChange} />
          </div>
        </div>

        <div className="controls">
          <button
            className={`analyze ${loading ? 'loading' : ''}`}
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Analyze / Recalculate'}
          </button>
          <div className="sort">
            Sort by:
            <select value={sortBy} onChange={handleSortChange} aria-label="sort-results">
              <option value="match">Match %</option>
              <option value="gap">Experience Gap</option>
            </select>
          </div>
        </div>
      </section>

      {results.length > 0 && <ResultsTable results={results} />}
    </>
  );
};
