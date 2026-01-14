import './ResultsTable.css';

const ResultCard = ({ result }) => {
  const matchPercent = result.overall_match || 0;
  const isGoodMatch = matchPercent >= 75;
  const hasGaps = result.missing_preferred && result.missing_preferred.length > 0;

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
        {hasGaps && (
          <div className="result-section">
            <h4 className="section-label">Missing Skills</h4>
            <div className="skill-list">
              {result.missing_preferred.map((skill, i) => (
                <span key={i} className="skill-badge missing">✖ {skill}</span>
              ))}
            </div>
          </div>
        )}

        {result.experience_gap && (
          <div className="result-section">
            <h4 className="section-label">Experience Gap</h4>
            <p className="gap-text">⚠ {result.experience_gap}</p>
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

export default function ResultsTable({ results }) {
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
        {results.map(result => (
          <ResultCard key={result.job_id || `${result.title}-${result.company}`} result={result} />
        ))}
      </div>
    </div>
  );
}
