import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const parseResume = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return API.post("/resume/parse", formData);
};

export const parseJobs = (jobs) =>
  API.post("/jobs/parse", { jobs });

export const matchJobs = (payload) =>
  API.post("/match", payload);
