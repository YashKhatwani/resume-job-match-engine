import React, { useState } from 'react';
import './ResumeSection.css';

import { ResumeSummary } from '../ResumeSummary/ResumeSummary';
import { ResumeUpload } from '../ResumeUpload/ResumeUpload';

export const ResumeSection = ({ onResumeData }) => {
    const [resumeData, setResumeData] = useState(null);

  const handleParsed = (data) => {
    setResumeData(data);
    onResumeData?.(data);
    console.log('Resume parsed:', data);
  };
  return (
    <aside className="resume-section">
      <div className="resume-upload">
        <ResumeUpload onParsed={handleParsed} />
      </div>

      <div className="resume-summary">
        <ResumeSummary 
          skills={resumeData?.skills || []} 
          totalYoe={resumeData?.total_yoe || 0}
        />
      </div>
    </aside>
  );
};