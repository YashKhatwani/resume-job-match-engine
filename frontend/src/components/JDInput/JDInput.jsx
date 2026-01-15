import React, { useState } from 'react';
import './JDInput.css';

const genId = () => `${Date.now().toString(36)}-${Math.random().toString(36).slice(2,8)}`;

export const JDInput = ({ initial = [], onChange }) => {
  const [jds, setJds] = useState(initial.length ? initial : [{ id: genId(), text: '' }]);

  const notify = (next) => { setJds(next); onChange?.(next); };

  const addJD = () => {
    const next = [...jds, { id: genId(), text: '' }];
    notify(next);
  };

  const removeJD = (id) => {
    const next = jds.filter(j => j.id !== id);
    notify(next.length ? next : [{ id: genId(), text: '' }]); // keep one empty card
  };

  const updateJD = (id, text) => {
    const next = jds.map(j => (j.id === id ? { ...j, text } : j));
    notify(next);
  };

  return (
    <div className="jd-input">
      <h3 className="jd-heading">Job Descriptions</h3>

      {jds.map((jd, idx) => (
        <div className="jd-card" key={jd.id}>
          <div className="jd-header">
            <span className="jd-number">JD {idx + 1}</span>
            <button
              type="button"
              className="remove-jd"
              aria-label={`Remove JD ${idx + 1}`}
              onClick={() => removeJD(jd.id)}
            >
              ✖
            </button>
          </div>

          <textarea
            className="jd-text"
            placeholder="Paste complete job description here..."
            value={jd.text}
            onChange={(e) => updateJD(jd.id, e.target.value)}
          />
        </div>
      ))}

      <div className="jd-controls">
        <button type="button" className="add-jd" onClick={addJD}>+ Add JD</button>
      </div>
    </div>
  );
};