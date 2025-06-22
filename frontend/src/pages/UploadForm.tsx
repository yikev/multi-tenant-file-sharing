// src/pages/UploadPage.tsx
import UploadForm from '../components/UploadForm';

const UploadPage = () => (
  <div className="max-w-md mx-auto mt-10">
    <h1 className="text-2xl font-bold mb-4">Upload a File</h1>
    <UploadForm />
  </div>
);

export default UploadPage;