import { useState } from "react";

export default function JDInput({ onSubmit }) {
  const [jds, setJds] = useState([
    { title: "", company: "", jd_text: "" }
  ]);

  const addJD = () =>
    setJds([...jds, { title: "", company: "", jd_text: "" }]);

  const update = (i, field, value) => {
    const copy = [...jds];
    copy[i][field] = value;
    setJds(copy);
  };

  return (
    <div>
      <h3>Paste Job Descriptions</h3>

      {jds.map((jd, i) => (
        <div key={i}>
          <input placeholder="Title"
            onChange={(e) => update(i, "title", e.target.value)} />
          <input placeholder="Company"
            onChange={(e) => update(i, "company", e.target.value)} />
          <textarea placeholder="Job Description"
            onChange={(e) => update(i, "jd_text", e.target.value)} />
        </div>
      ))}

      <button onClick={addJD}>+ Add JD</button>
      <button onClick={() => onSubmit(jds)}>Analyze</button>
    </div>
  );
}
