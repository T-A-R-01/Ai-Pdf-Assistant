export default function UploadSection({
  selectedFile,
  setSelectedFile,
}) {
  return (
    <div className="upload-card">

      <h3 className="upload-title">
        Upload PDF
      </h3>

      <label className="upload-zone">

        <input
          type="file"
          accept=".pdf"
          className="hidden-input"
          onChange={(e) =>
            setSelectedFile(e.target.files[0])
          }
        />

        <div className="upload-content">

          <div className="upload-icon">
            📄
          </div>

          <div>
            <div className="upload-main">
              Click to upload PDF
            </div>

            <div className="upload-sub">
              PDF files only
            </div>
          </div>

        </div>

      </label>

      {selectedFile && (
        <div className="selected-file">
          {selectedFile.name}
        </div>
      )}

    </div>
  );
}