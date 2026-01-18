import './ResultsTable.css';

const ResultCard = ({ result, resumeYoe }) => {
  const matchPercent = result.overall_match || 0;
  const isGoodMatch = matchPercent >= 75;
  const hasMatchedRequired = result.matched_required && result.matched_required.length > 0;
  const hasMissingRequired = result.missing_required && result.missing_required.length > 0;
  const hasMissingPreferred = result.missing_preferred && result.missing_preferred.length > 0;
  const hasMatchedEducation = result.matched_education && result.matched_education.length > 0;
  const hasMissingEducation = result.missing_education && result.missing_education.length > 0;
  const hasMatchedQualifications = result.matched_qualifications && result.matched_qualifications.length > 0;
  const hasMissingQualifications = result.missing_qualifications && result.missing_qualifications.length > 0;

  return (
    <div className="result-card">
      <div className="result-header">
        <div className="result-title-section">
          <h3 className="result-title">{result.title}</h3>
          <p className="result-company">{result.company}</p>
        </div>
        <div className={`match-badge ${isGoodMatch ? 'good' : 'fair'}`}>
          {matchPercent}%
        </div>
      </div>

      <div className="result-body">
        {/* Matched Required Skills */}
        {hasMatchedRequired && (
          <div className="result-section">
            <h4 className="section-label">✓ Matched Skills</h4>
            <div className="skill-list">
              {result.matched_required.map((skill, i) => (
                <span key={i} className="skill-badge matched">✓ {skill}</span>
              ))}
            </div>
          </div>
        )}

        {/* Missing Required Skills */}
        {hasMissingRequired && (
          <div className="result-section">
            <h4 className="section-label">✖ Missing Required Skills</h4>
            <div className="skill-list">
              {result.missing_required.map((skill, i) => (
                <span key={i} className="skill-badge missing">✖ {skill}</span>
              ))}
            </div>
          </div>
        )}

        {/* Missing Preferred Skills */}
        {hasMissingPreferred && (
          <div className="result-section">
            <h4 className="section-label">~ Missing Preferred Skills</h4>
            <div className="skill-list">
              {result.missing_preferred.map((skill, i) => (
                <span key={i} className="skill-badge preferred-missing">~ {skill}</span>
              ))}
            </div>
          </div>
        )}

        {/* Matched Education */}
        {hasMatchedEducation && (
          <div className="result-section">
            <h4 className="section-label">✓ Matched Education</h4>
            <div className="skill-list">
              {result.matched_education.map((edu, i) => (
                <span key={i} className="skill-badge matched">✓ {edu}</span>
              ))}
            </div>
          </div>
        )}

        {/* Missing Education */}
        {hasMissingEducation && (
          <div className="result-section">
            <h4 className="section-label">✖ Missing Education</h4>
            <div className="skill-list">
              {result.missing_education.map((edu, i) => (
                <span key={i} className="skill-badge missing">✖ {edu}</span>
              ))}
            </div>
          </div>
        )}

        {/* Matched Qualifications */}
        {hasMatchedQualifications && (
          <div className="result-section">
            <h4 className="section-label">✓ Matched Qualifications</h4>
            <div className="skill-list">
              {result.matched_qualifications.map((qual, i) => (
                <span key={i} className="skill-badge matched">✓ {qual}</span>
              ))}
            </div>
          </div>
        )}

        {/* Missing Qualifications */}
        {hasMissingQualifications && (
          <div className="result-section">
            <h4 className="section-label">~ Missing Qualifications</h4>
            <div className="skill-list">
              {result.missing_qualifications.map((qual, i) => (
                <span key={i} className="skill-badge preferred-missing">~ {qual}</span>
              ))}
            </div>
          </div>
        )}

        {/* Experience Gap */}
        {result.experience_gap > 0 && (
          <div className="result-section">
            <h4 className="section-label">⚠ Experience Gap</h4>
            <p className="gap-text">You have {resumeYoe} years, Job requires {resumeYoe + result.experience_gap} years (Missing {result.experience_gap} year{result.experience_gap !== 1 ? 's' : ''})</p>
          </div>
        )}

        {/* Experience Match */}
        {result.experience_gap === 0 && resumeYoe && (
          <div className="result-section">
            <h4 className="section-label">✓ Experience</h4>
            <p className="gap-text">You have {resumeYoe} years - matches requirement</p>
          </div>
        )}

        {/* AI Suggestions */}
        {result.suggestions && result.suggestions.length > 0 && (
          <div className="result-section suggestions-section">
            <h4 className="section-label">💡Suggestions to Improve Match (AI-assisted)</h4>
            <div className="suggestions-list">
              {result.suggestions.map((suggestion, i) => (
                <div key={i} className="suggestion-item">{suggestion}</div>
              ))}
            </div>
          </div>
        )}
      </div>

      {result.explanation && (
        <div className="result-footer">
          <p className="explanation-text">{result.explanation}</p>
        </div>
      )}
    </div>
  );
};

export default function ResultsTable({ results, resumeYoe, suggestions }) {
  if (!results || results.length === 0) {
    return (
      <div className="results-empty">
        <p>No results yet. Upload a resume and add job descriptions to get started.</p>
      </div>
    );
  }

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Match Results</h2>
        <p className="result-count">{results.length} job{results.length !== 1 ? 's' : ''} analyzed</p>
      </div>
      <div className="results-list">
        {results.map((result, index) => (
          <ResultCard 
            key={result.job_id || `${result.title}-${result.company}`} 
            result={{...result, suggestions: index === 0 ? suggestions : []}} 
            resumeYoe={resumeYoe} 
          />
        ))}
      </div>
    </div>
  );
}
