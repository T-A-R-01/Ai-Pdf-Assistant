export default function Sidebar({ pdfs = [] }) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        📄 Documents
      </div>

      {pdfs.length === 0 ? (
        <div className="empty-state">
          No PDF uploaded yet
        </div>
      ) : (
        <div className="pdf-list">
          {pdfs.map((pdf, index) => (
            <div key={index} className="pdf-card">
              📄 {pdf}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}