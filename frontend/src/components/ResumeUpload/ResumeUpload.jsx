import { useState } from 'react';
import './ResumeUpload.css';

export const ResumeUpload = ({ onParsed }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleUpload = async (file) => {
    if (!file) return;

    setLoading(true);
    try {
      const res = await import("../../services/api")
        .then(api => api.parseResume(file));
      console.log('Upload response:', res);
      onParsed(res.data);
      setSelectedFile(file.name);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    console.log("file selected");
    const file = e.target.files?.[0];
    handleUpload(file);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const file = e.dataTransfer?.files?.[0];
    if (file?.type === 'application/pdf') {
      handleUpload(file);
    }
  };

  return (
    <div className="resume-upload-container">
      <h3>Upload Resume</h3>
      <div
        className={`upload-zone ${dragActive ? 'drag-active' : ''} ${selectedFile ? 'file-selected' : ''} ${loading ? 'loading' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <label className="upload-label">
          <span className="upload-icon">{loading ? <div className="spinner"></div> : '📄'}</span>
          <p className="upload-text">{loading ? 'Uploading...' : 'Drop your resume here'}</p>
          <p className="upload-hint">or click to browse</p>
         
          <input
            type="file"
            accept=".pdf"
            onChange={handleChange}
            className="file-input"
            disabled={loading}
          />
          {selectedFile && !loading && <p className="file-name">✓ {selectedFile}</p>}
        </label>
      </div>
    </div>
  );
}
