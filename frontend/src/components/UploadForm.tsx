// src/components/UploadForm.tsx
import React, { useState } from 'react';
import axios from 'axios';
import { useProjectContext } from '../context/ProjectContext';

const UploadForm: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState('');

  const { activeProjectId } = useProjectContext();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setMessage("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append('uploaded_file', file);
    formData.append('file_size_kb', Math.ceil(file.size / 1024).toString());
    formData.append('project_id', activeProjectId);

    try {
      const res = await axios.post(`${import.meta.env.VITE_API_URL}/files/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${localStorage.getItem('token')}`, // if using JWT
        },
      });

      setMessage(res.data.message);
    } catch (err: any) {
      console.error(err);
      setMessage("Upload failed");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 p-4 border rounded shadow">
      <input type="file" onChange={handleFileChange} />
      <button type="submit" className="bg-blue-600 text-white py-2 px-4 rounded">
        Upload
      </button>
      {message && <p>{message}</p>}
    </form>
  );
};

export default UploadForm;