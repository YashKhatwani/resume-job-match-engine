export default function ResultsTable({ results }) {
  if (!results.length) return null;

  return (
    <table border="1" cellPadding="8">
      <thead>
        <tr>
          <th>Role</th>
          <th>Company</th>
          <th>Match %</th>
          <th>Missing Skills</th>
          <th>Experience Gap</th>
        </tr>
      </thead>
      <tbody>
        {results.map(r => (
          <tr key={r.job_id}>
            <td>{r.title}</td>
            <td>{r.company}</td>
            <td>{r.overall_match}%</td>
            <td>{r.missing_preferred.join(", ") || "None"}</td>
            <td>{r.experience_gap}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
